"""
API endpoints для игры
"""
from fastapi import APIRouter, HTTPException, Request
import logging
import os
from app.game.logic import TicTacToe
from app.game.ai import AIPlayer
from app.game.promocode import generate_promocode
from app.telegram.notifier import notify_telegram
from app.models.schemas import MoveRequest, GameResponse
from app.storage.redis_client import get_storage
from app.core.limiter import limiter

router = APIRouter()
logger = logging.getLogger(__name__)

# Fallback хранилище в памяти (если Redis недоступен)
active_games_fallback = {}

# Флаг использования Redis
USE_REDIS = os.getenv("USE_REDIS", "true").lower() == "true"

async def _save_game(game: TicTacToe) -> bool:
    """Сохранить игру в хранилище"""
    if USE_REDIS:
        try:
            storage = await get_storage()
            result = await storage.save_game(game)
            if result:
                return True
            else:
                # Если сохранение не удалось, используем fallback
                logger.warning("Сохранение в Redis вернуло False, используем fallback")
                active_games_fallback[game.game_id] = game
                return True
        except Exception as e:
            logger.warning(f"Не удалось сохранить в Redis, используем fallback: {e}")
            # Fallback на память
            active_games_fallback[game.game_id] = game
            return True
    else:
        active_games_fallback[game.game_id] = game
        return True

async def _get_game(game_id: str) -> TicTacToe:
    """Получить игру из хранилища"""
    if USE_REDIS:
        try:
            storage = await get_storage()
            game = await storage.get_game(game_id)
            if game:
                return game
        except Exception as e:
            logger.warning(f"Не удалось получить из Redis, пробуем fallback: {e}")
    
    # Fallback на память
    if game_id in active_games_fallback:
        return active_games_fallback[game_id]
    
    return None

@router.post("/game/start", response_model=GameResponse)
@limiter.limit("20/minute")
async def start_game(request: Request):
    """Начать новую игру"""
    try:
        game = TicTacToe()
        await _save_game(game)
        logger.info(
            f"Новая игра создана: {game.game_id}",
            extra={"game_id": game.game_id}
        )
        
        return GameResponse(
            game_id=game.game_id,
            board=game.board,
            status=game.status
        )
    except Exception as e:
        logger.error(f"Ошибка при создании игры: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Не удалось создать новую игру. Попробуйте позже."
        )

@router.post("/game/move", response_model=GameResponse)
@limiter.limit("60/minute")
async def make_move(request: Request, move_request: MoveRequest):
    """Ход игрока"""
    try:
        # Валидация входных данных
        if not move_request.game_id:
            raise HTTPException(status_code=400, detail="game_id обязателен")
        
        if move_request.row is None or move_request.col is None:
            raise HTTPException(status_code=400, detail="row и col обязательны")
        
        if move_request.row < 0 or move_request.row >= 5 or move_request.col < 0 or move_request.col >= 5:
            raise HTTPException(status_code=400, detail="Неверные координаты. Допустимые значения: 0-4")
        
        game = await _get_game(move_request.game_id)
        if game is None:
            raise HTTPException(status_code=404, detail="Игра не найдена")
        
        # Проверка статуса игры
        if game.status != 'playing':
            raise HTTPException(status_code=400, detail="Игра уже завершена")
        
        # Ход игрока (X)
        result = game.make_move(move_request.row, move_request.col, 'X')
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['message'])
        
        # Сохраняем изменения
        await _save_game(game)
        
        logger.info(
            f"Ход игрока",
            extra={
                "game_id": move_request.game_id,
                "row": move_request.row,
                "col": move_request.col
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при обработке хода: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Не удалось обработать ход. Попробуйте позже."
        )
    
    try:
        # Проверка победы/ничьей после хода игрока
        winner = game.check_winner()
        if winner == 'X':  # Игрок выиграл
            game.status = 'finished'
            promocode = generate_promocode()
            await _save_game(game)  # Сохраняем финальное состояние
            
            # Отправка уведомления в Telegram при победе
            if move_request.chat_id:
                try:
                    await notify_telegram(move_request.chat_id, "victory", promocode)
                except Exception as e:
                    logger.warning(f"Не удалось отправить уведомление в Telegram: {e}")
                    # Не прерываем выполнение, если уведомление не отправилось
            
            logger.info(
                f"Игрок выиграл",
                extra={
                    "game_id": move_request.game_id,
                    "promocode": promocode
                }
            )
            return GameResponse(
                game_id=game.game_id,
                board=game.board,
                status='finished',
                winner='player',
                promocode=promocode,
                message="🎉 Поздравляем с победой!"
            )
    
        if game.is_draw():
            game.status = 'finished'
            await _save_game(game)  # Сохраняем финальное состояние
            
            # Отправка уведомления в Telegram при ничьей
            if move_request.chat_id:
                try:
                    await notify_telegram(move_request.chat_id, "draw")
                except Exception as e:
                    logger.warning(f"Не удалось отправить уведомление в Telegram: {e}")
            
            logger.info(
                f"Ничья",
                extra={"game_id": move_request.game_id}
            )
            return GameResponse(
                game_id=game.game_id,
                board=game.board,
                status='finished',
                winner='draw',
                message="🤝 Ничья!"
            )
        
        # Ход AI (O)
        try:
            ai = AIPlayer()
            ai_move = ai.get_best_move(game)
            if ai_move:
                # AI делает ход как 'O'
                game.make_move(ai_move[0], ai_move[1], 'O')
                await _save_game(game)  # Сохраняем состояние после хода AI
                
                logger.info(
                    f"Ход AI",
                    extra={
                        "game_id": move_request.game_id,
                        "row": ai_move[0],
                        "col": ai_move[1]
                    }
                )
                
                # Проверка победы/ничьей после хода AI
                winner = game.check_winner()
                if winner == 'O':  # AI выиграл
                    game.status = 'finished'
                    await _save_game(game)  # Сохраняем финальное состояние
                    
                    # Отправка уведомления в Telegram при проигрыше
                    if move_request.chat_id:
                        try:
                            await notify_telegram(move_request.chat_id, "defeat")
                        except Exception as e:
                            logger.warning(f"Не удалось отправить уведомление в Telegram: {e}")
                    
                    logger.info(
                        f"AI выиграл",
                        extra={"game_id": move_request.game_id}
                    )
                    return GameResponse(
                        game_id=game.game_id,
                        board=game.board,
                        status='finished',
                        winner='ai',
                        message="😔 Компьютер выиграл"
                    )
                
                if game.is_draw():
                    game.status = 'finished'
                    await _save_game(game)  # Сохраняем финальное состояние
                    
                    if move_request.chat_id:
                        try:
                            await notify_telegram(move_request.chat_id, "draw")
                        except Exception as e:
                            logger.warning(f"Не удалось отправить уведомление в Telegram: {e}")
                    
                    logger.info(
                        f"Ничья",
                        extra={"game_id": move_request.game_id}
                    )
                    return GameResponse(
                        game_id=game.game_id,
                        board=game.board,
                        status='finished',
                        winner='draw',
                        message="🤝 Ничья!"
                    )
        except Exception as e:
            logger.error(f"Ошибка при ходе AI: {e}", exc_info=True)
            # Продолжаем игру, даже если AI не смог сделать ход
        
        await _save_game(game)  # Сохраняем текущее состояние
        
        return GameResponse(
            game_id=game.game_id,
            board=game.board,
            status=game.status
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при обработке хода: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Не удалось обработать ход. Попробуйте позже."
        )

@router.get("/game/{game_id}", response_model=GameResponse)
@limiter.limit("100/minute")
async def get_game_status(request: Request, game_id: str):
    """Получить статус игры"""
    try:
        if not game_id:
            raise HTTPException(status_code=400, detail="game_id обязателен")
        
        game = await _get_game(game_id)
        if game is None:
            raise HTTPException(status_code=404, detail="Игра не найдена")
        
        return GameResponse(
            game_id=game.game_id,
            board=game.board,
            status=game.status
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Ошибка при получении статуса игры: {e}",
            extra={"game_id": game_id},
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Не удалось получить статус игры. Попробуйте позже."
        )


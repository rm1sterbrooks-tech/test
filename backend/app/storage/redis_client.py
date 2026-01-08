"""
Redis клиент для хранения игр
"""
import os
import json
import logging
from typing import Optional
from datetime import timedelta
from app.game.logic import TicTacToe

logger = logging.getLogger(__name__)

# Проверка доступности Redis
try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None
    logger.warning("Redis не установлен. Установите: pip install redis>=5.0.0")
    # Создаем заглушку для типов
    class Redis:
        pass

class RedisStorage:
    """Класс для работы с Redis хранилищем"""
    
    def __init__(self):
        if not REDIS_AVAILABLE:
            raise RuntimeError("Redis не установлен. Установите: pip install redis>=5.0.0")
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.redis_db = int(os.getenv("REDIS_DB", 0))
        self.game_ttl_hours = int(os.getenv("GAME_TTL_HOURS", 24))
        self._client = None
    
    async def _get_client(self) -> redis.Redis:
        """Получить или создать Redis клиент"""
        if self._client is None:
            try:
                self._client = redis.Redis(
                    host=self.redis_host,
                    port=self.redis_port,
                    db=self.redis_db,
                    decode_responses=False,  # Получаем байты для JSON
                    socket_connect_timeout=5,
                    socket_keepalive=True
                )
                # Проверка подключения
                await self._client.ping()
                logger.info(f"Подключено к Redis: {self.redis_host}:{self.redis_port}")
            except Exception as e:
                logger.error(f"Ошибка подключения к Redis: {e}")
                raise
        
        return self._client
    
    async def save_game(self, game: TicTacToe) -> bool:
        """Сохранить игру в Redis"""
        try:
            client = await self._get_client()
            game_data = {
                "game_id": game.game_id,
                "board": game.board,
                "status": game.status,
                "current_player": game.current_player
            }
            key = f"game:{game.game_id}"
            # Сохраняем с TTL
            await client.setex(
                key,
                timedelta(hours=self.game_ttl_hours),
                json.dumps(game_data).encode('utf-8')
            )
            logger.debug(f"Игра сохранена в Redis: {game.game_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения игры в Redis: {e}", exc_info=True)
            return False
    
    async def get_game(self, game_id: str) -> Optional[TicTacToe]:
        """Получить игру из Redis"""
        try:
            client = await self._get_client()
            key = f"game:{game_id}"
            data = await client.get(key)
            
            if data is None:
                logger.debug(f"Игра не найдена в Redis: {game_id}")
                return None
            
            game_data = json.loads(data.decode('utf-8'))
            # Восстанавливаем объект TicTacToe
            game = TicTacToe()
            game.game_id = game_data["game_id"]
            game.board = game_data["board"]
            game.status = game_data["status"]
            game.current_player = game_data.get("current_player", "X")
            
            logger.debug(f"Игра загружена из Redis: {game_id}")
            return game
        except Exception as e:
            logger.error(f"Ошибка получения игры из Redis: {e}", exc_info=True)
            return None
    
    async def delete_game(self, game_id: str) -> bool:
        """Удалить игру из Redis"""
        try:
            client = await self._get_client()
            key = f"game:{game_id}"
            await client.delete(key)
            logger.debug(f"Игра удалена из Redis: {game_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления игры из Redis: {e}", exc_info=True)
            return False
    
    async def close(self):
        """Закрыть соединение с Redis"""
        if self._client:
            await self._client.close()
            self._client = None
            logger.info("Соединение с Redis закрыто")


# Глобальный экземпляр хранилища
_storage_instance = None

async def get_storage() -> RedisStorage:
    """Получить экземпляр хранилища (singleton)"""
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = RedisStorage()
    return _storage_instance


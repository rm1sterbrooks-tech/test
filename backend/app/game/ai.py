"""
AI противника для игры "Крестики-нолики"
"""
from app.game.logic import TicTacToe
from typing import Optional, Tuple

class AIPlayer:
    """AI игрок с умным алгоритмом"""
    
    def __init__(self):
        self.symbol = 'O'  # AI всегда играет O
    
    def get_best_move(self, game: TicTacToe) -> Optional[Tuple[int, int]]:
        """Получить лучший ход для AI (для поля 5x5)"""
        size = game.BOARD_SIZE
        center = size // 2
        
        # Стратегия:
        # 1. Попытаться выиграть
        # 2. Блокировать победу игрока
        # 3. Занять центр
        # 4. Занять углы
        # 5. Любая доступная клетка
        
        # 1. Попытка выиграть
        move = self._try_win(game)
        if move:
            return move
        
        # 2. Блокировка игрока
        move = self._block_player(game)
        if move:
            return move
        
        # 3. Занять центр
        if game.board[center][center] == '':
            return (center, center)
        
        # 4. Занять углы
        corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
        for corner in corners:
            if game.board[corner[0]][corner[1]] == '':
                return corner
        
        # 5. Любая доступная клетка
        empty = game.get_empty_cells()
        if empty:
            return empty[0]
        
        return None
    
    def _try_win(self, game: TicTacToe) -> Optional[Tuple[int, int]]:
        """Попытаться выиграть"""
        return self._find_winning_move(game, self.symbol)
    
    def _block_player(self, game: TicTacToe) -> Optional[Tuple[int, int]]:
        """Блокировать победу игрока"""
        return self._find_winning_move(game, 'X')
    
    def _find_winning_move(self, game: TicTacToe, symbol: str) -> Optional[Tuple[int, int]]:
        """Найти ход, который приведет к победе (для поля 5x5)"""
        size = game.BOARD_SIZE
        for i in range(size):
            for j in range(size):
                if game.board[i][j] == '':
                    # Пробуем сделать ход
                    game.board[i][j] = symbol
                    winner = game.check_winner()
                    game.board[i][j] = ''  # Откатываем
                    
                    if winner == symbol:
                        return (i, j)
        
        return None


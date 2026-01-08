"""
Логика игры "Крестики-нолики"
"""
import uuid
from typing import Optional

class TicTacToe:
    """Класс для управления игрой"""
    
    BOARD_SIZE = 5  # Размер поля 5x5
    WIN_LENGTH = 3  # Для победы нужно 3 в ряд
    
    def __init__(self):
        self.board = [['' for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.current_player = 'X'  # Игрок всегда X
        self.game_id = str(uuid.uuid4())
        self.status = 'playing'
    
    def make_move(self, row: int, col: int, symbol: str = None) -> dict:
        """Сделать ход"""
        # Проверка валидности хода
        if row < 0 or row >= self.BOARD_SIZE or col < 0 or col >= self.BOARD_SIZE:
            return {'success': False, 'message': 'Неверные координаты'}
        
        if self.board[row][col] != '':
            return {'success': False, 'message': 'Клетка уже занята'}
        
        if self.status != 'playing':
            return {'success': False, 'message': 'Игра уже завершена'}
        
        # Используем переданный символ или текущего игрока
        move_symbol = symbol if symbol else self.current_player
        
        # Делаем ход
        self.board[row][col] = move_symbol
        
        return {'success': True, 'message': 'Ход выполнен'}
    
    def check_winner(self) -> Optional[str]:
        """Проверка победителя (3 в ряд для поля 5x5)"""
        size = self.BOARD_SIZE
        win_length = self.WIN_LENGTH
        
        # Проверка строк
        for row in range(size):
            for col in range(size - win_length + 1):
                if self.board[row][col] != '':
                    if all(self.board[row][col + i] == self.board[row][col] for i in range(win_length)):
                        return self.board[row][col]
        
        # Проверка столбцов
        for col in range(size):
            for row in range(size - win_length + 1):
                if self.board[row][col] != '':
                    if all(self.board[row + i][col] == self.board[row][col] for i in range(win_length)):
                        return self.board[row][col]
        
        # Проверка главной диагонали (слева направо)
        for row in range(size - win_length + 1):
            for col in range(size - win_length + 1):
                if self.board[row][col] != '':
                    if all(self.board[row + i][col + i] == self.board[row][col] for i in range(win_length)):
                        return self.board[row][col]
        
        # Проверка побочной диагонали (справа налево)
        for row in range(size - win_length + 1):
            for col in range(win_length - 1, size):
                if self.board[row][col] != '':
                    if all(self.board[row + i][col - i] == self.board[row][col] for i in range(win_length)):
                        return self.board[row][col]
        
        return None
    
    def is_draw(self) -> bool:
        """Проверка ничьей"""
        if self.check_winner():
            return False
        
        # Проверяем, есть ли свободные клетки
        for row in self.board:
            for cell in row:
                if cell == '':
                    return False
        
        return True
    
    def get_empty_cells(self) -> list:
        """Получить список пустых клеток"""
        empty = []
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == '':
                    empty.append((i, j))
        return empty


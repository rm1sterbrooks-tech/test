"""
Тесты для AI
"""
import pytest
from app.game.logic import TicTacToe
from app.game.ai import AIPlayer

def test_ai_tries_to_win():
    """Тест: AI пытается выиграть (для поля 5x5)"""
    game = TicTacToe()
    # Создаем ситуацию, где AI может выиграть на поле 5x5
    game.board = [
        ['O', 'O', '', '', ''],  # AI может завершить ряд здесь
        ['X', 'X', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', '']
    ]
    ai = AIPlayer()
    move = ai.get_best_move(game)
    assert move == (0, 2)  # AI должен завершить ряд

def test_ai_blocks_player():
    """Тест: AI блокирует игрока (для поля 5x5)"""
    game = TicTacToe()
    # Создаем ситуацию, где игрок может выиграть на поле 5x5
    game.board = [
        ['X', 'X', '', '', ''],  # Игрок близок к победе (нужен 3-й X)
        ['O', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', '']
    ]
    ai = AIPlayer()
    move = ai.get_best_move(game)
    assert move == (0, 2)  # AI должен заблокировать

def test_ai_takes_center():
    """Тест: AI занимает центр (для поля 5x5)"""
    game = TicTacToe()
    game.make_move(0, 0, 'X')
    ai = AIPlayer()
    move = ai.get_best_move(game)
    assert move == (2, 2)  # Центр для поля 5x5

def test_ai_takes_corner():
    """Тест: AI занимает угол (для поля 5x5)"""
    game = TicTacToe()
    game.make_move(2, 2, 'X')  # Игрок занял центр
    ai = AIPlayer()
    move = ai.get_best_move(game)
    # AI должен занять один из углов
    corners = [(0, 0), (0, 4), (4, 0), (4, 4)]
    assert move in corners


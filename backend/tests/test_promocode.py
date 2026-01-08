"""
Тесты для генерации промокодов
"""
import pytest
from app.game.promocode import generate_promocode

def test_promocode_length():
    """Тест: промокод имеет длину 5"""
    promocode = generate_promocode()
    assert len(promocode) == 5

def test_promocode_format():
    """Тест: промокод содержит только буквы и цифры"""
    promocode = generate_promocode()
    assert promocode.isalnum()
    assert promocode.isupper()  # Все буквы заглавные

def test_promocode_uniqueness():
    """Тест: промокоды уникальны (с высокой вероятностью)"""
    promocodes = [generate_promocode() for _ in range(100)]
    # Проверяем, что есть хотя бы несколько уникальных
    unique_count = len(set(promocodes))
    assert unique_count > 50  # С высокой вероятностью будут уникальные

def test_promocode_no_confusing_chars():
    """Тест: промокод не содержит похожие символы"""
    promocode = generate_promocode()
    # Проверяем, что нет похожих символов
    assert '0' not in promocode
    assert 'O' not in promocode
    assert 'I' not in promocode
    assert '1' not in promocode


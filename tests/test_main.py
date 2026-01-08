"""
Тесты для main.py
"""

import pytest
from src.main import main


def test_main_function():
    """Тест главной функции"""
    # Это базовый тест, который можно расширить
    assert callable(main)


if __name__ == "__main__":
    pytest.main([__file__])


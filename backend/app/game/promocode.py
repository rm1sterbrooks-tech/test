"""
Генерация промокодов
"""
import random
import string

def generate_promocode() -> str:
    """Генерирует случайный 5-значный промокод"""
    # Используем буквы и цифры
    characters = string.ascii_uppercase + string.digits
    # Исключаем похожие символы (0, O, I, 1)
    characters = characters.replace('0', '').replace('O', '').replace('I', '').replace('1', '')
    
    promocode = ''.join(random.choice(characters) for _ in range(5))
    return promocode


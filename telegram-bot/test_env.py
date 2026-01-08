"""Тест загрузки .env файла"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Пробуем несколько способов загрузки
env_path1 = Path(__file__).parent / '.env'
env_path2 = Path(__file__).parent.parent / 'telegram-bot' / '.env'

print(f"Проверка пути 1: {env_path1} - существует: {env_path1.exists()}")
print(f"Проверка пути 2: {env_path2} - существует: {env_path2.exists()}")

# Загружаем из правильного пути
if env_path1.exists():
    load_dotenv(dotenv_path=env_path1)
elif env_path2.exists():
    load_dotenv(dotenv_path=env_path2)
else:
    load_dotenv()  # Пробуем текущую директорию

token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

print(f"\nToken loaded: {'OK' if token and len(token) > 20 else 'NOT FOUND'}")
if token:
    print(f"Token (первые 20 символов): {token[:20]}...")
print(f"Chat ID: {chat_id}")


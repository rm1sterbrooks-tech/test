"""
Главный файл приложения
"""

import os
from dotenv import load_dotenv


def main():
    """Главная функция приложения"""
    # Загрузка переменных окружения
    load_dotenv()
    
    print("Привет! Это новый проект.")
    print(f"Версия: 0.1.0")
    
    # Пример использования переменных окружения
    api_key = os.getenv("API_KEY", "не установлен")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    print(f"API Key: {api_key}")
    print(f"Log Level: {log_level}")


if __name__ == "__main__":
    main()


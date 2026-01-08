"""
Скрипт для получения Chat ID для Telegram-бота
Инструкция:
1. Создайте бота через @BotFather и получите токен
2. Добавьте токен в .env как TELEGRAM_BOT_TOKEN
3. Отправьте вашему боту любое сообщение в Telegram
4. Запустите этот скрипт
"""
import os
import sys
from dotenv import load_dotenv
import requests

# Загружаем .env из telegram-bot директории
env_path = os.path.join(os.path.dirname(__file__), '..', 'telegram-bot', '.env')
load_dotenv(env_path)

def get_chat_id():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token:
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не найден в .env")
        print("Создайте бота через @BotFather и добавьте токен в telegram-bot/.env")
        return
    
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('result'):
            print("❌ Сообщений не найдено.")
            print("📱 Отправьте вашему боту любое сообщение в Telegram и запустите скрипт снова")
            return
        
        # Берем последнее сообщение
        last_update = data['result'][-1]
        if 'message' in last_update:
            chat_id = last_update['message']['chat']['id']
            username = last_update['message']['chat'].get('username', 'N/A')
            first_name = last_update['message']['chat'].get('first_name', 'N/A')
            
            print(f"✅ Chat ID найден!")
            print(f"   Chat ID: {chat_id}")
            print(f"   Имя: {first_name}")
            print(f"   Username: @{username}")
            print(f"\n📝 Добавьте в telegram-bot/.env:")
            print(f"   TELEGRAM_CHAT_ID={chat_id}")
        else:
            print("❌ Не удалось найти сообщение")
            
    except requests.RequestException as e:
        print(f"❌ Ошибка при запросе: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    get_chat_id()


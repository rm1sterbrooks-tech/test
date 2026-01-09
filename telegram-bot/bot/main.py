"""
Главный файл Telegram-бота
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.error import TelegramError
import os
import asyncio
from dotenv import load_dotenv
from pathlib import Path
import threading
import httpx

# Загружаем .env из директории telegram-bot
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Telegram Bot API")

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Логирование для отладки
print(f"[Telegram Bot] Token loaded: {'Yes' if bot_token and bot_token != 'your_bot_token_here' else 'No'}")
print(f"[Telegram Bot] Chat ID loaded: {chat_id if chat_id and chat_id != 'your_chat_id_here' else 'No'}")

bot = None
bot_application = None

if bot_token:
    bot = Bot(token=bot_token)
    # Создаем Application для обработки команд
    bot_application = Application.builder().token(bot_token).build()

class NotificationRequest(BaseModel):
    chat_id: str
    promocode: str = None

async def send_message(chat_id: str, message: str):
    """Отправка сообщения в Telegram"""
    if not bot or not chat_id:
        print(f"[Telegram] Не настроен: {message}")
        return
    
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        print(f"[Telegram] Ошибка отправки: {e}")

@app.get("/")
async def root():
    return {"status": "ok", "message": "TicTacToe Telegram Bot is running"}

@app.get("/health")
async def health():
    return {"status": "ok", "bot_configured": bot is not None}

@app.post("/notify/victory")
async def notify_victory(request: NotificationRequest):
    """Уведомление о победе"""
    if not request.promocode:
        raise HTTPException(status_code=400, detail="Промокод не указан")
    
    message = f"🎉 Победа! Промокод выдан: {request.promocode}"
    await send_message(request.chat_id, message)
    
    return {"status": "sent", "message": message}

@app.post("/notify/defeat")
async def notify_defeat(request: NotificationRequest):
    """Уведомление о проигрыше"""
    message = "😔 Проигрыш"
    await send_message(request.chat_id, message)
    
    return {"status": "sent", "message": message}

@app.post("/notify/draw")
async def notify_draw(request: NotificationRequest):
    """Уведомление о ничьей"""
    message = "🤝 Ничья"
    await send_message(request.chat_id, message)
    
    return {"status": "sent", "message": message}

# Обработчики команд Telegram
async def start_command(update, context):
    """Обработчик команды /start"""
    try:
        chat_id = str(update.effective_chat.id)
        user = update.effective_user
        username = user.first_name or "друг"
        
        # Получаем параметр из команды (если есть)
        start_param = context.args[0] if context.args else None
        
        linked_successfully = False
        if start_param:
            # Пытаемся привязать через Backend
            backend_url = os.getenv("BACKEND_URL", "https://tictactoe-backend-v2.onrender.com")
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.post(
                        f"{backend_url}/api/telegram/link",
                        json={"token": start_param, "chat_id": chat_id}
                    )
                    if response.status_code == 200:
                        linked_successfully = True
                        print(f"[Telegram] Успешно привязано: {start_param} -> {chat_id}")
                    else:
                        print(f"[Telegram] Ошибка привязки (статус {response.status_code}): {response.text}")
            except Exception as e:
                print(f"[Telegram] Ошибка при подключении к Backend: {e}")

        message = f"Привет, {username}! 👋\n\n"
        message += "🎮 Добро пожаловать в игру 'Крестики-нолики'!\n\n"
        
        if linked_successfully:
            message += "✅ *Аккаунт успешно привязан автоматически!*\n\n"
        
        message += f"📱 Твой Chat ID: `{chat_id}`\n\n"
        message += "💡 Не волнуйся, это нужно сделать только один раз! 😊\n\n"
        message += "📝 Что делать дальше:\n"
        message += "1. Если Chat ID не подставился в игре автоматически — скопируй его выше.\n"
        message += "2. Вставь Chat ID в поле ввода в игре.\n"
        message += "3. Начни играть и получай уведомления! 🎉\n\n"
        
        message += "✨ После первого ввода Chat ID сохранится автоматически, и больше не нужно будет его вводить! 🎊\n\n"
        message += "Удачи в игре! 🍀"
        
        await update.message.reply_text(
            message,
            parse_mode='Markdown'
        )
        print(f"[Telegram] Пользователь {username} (ID: {chat_id}) использовал команду /start" + (f" с параметром: {start_param}" if start_param else ""))
    except Exception as e:
        print(f"[Telegram] Критическая ошибка в start_command: {e}")
        # Пытаемся отправить хоть какое-то сообщение в случае ошибки
        try:
            await update.message.reply_text("Произошла ошибка при запуске бота. Пожалуйста, попробуйте позже.")
        except:
            pass

async def handle_message(update, context):
    """Обработчик обычных сообщений"""
    chat_id = str(update.effective_chat.id)
    user = update.effective_user
    username = user.first_name or "друг"
    
    message = f"Привет, {username}! 👋\n\n"
    message += f"📱 Твой Chat ID: `{chat_id}`\n\n"
    message += "💡 Не переживай, это нужно сделать только один раз! 😊\n\n"
    message += "📝 Скопируй Chat ID и вставь его в игру - после этого он сохранится автоматически! 🎉\n\n"
    message += "💬 Подсказка: используй команду /start для получения полной инструкции"
    
    await update.message.reply_text(
        message,
        parse_mode='Markdown'
    )
    print(f"[Telegram] Пользователь {username} (ID: {chat_id}) отправил сообщение")

def setup_bot_handlers():
    """Настройка обработчиков команд бота"""
    if not bot_application:
        print("[Telegram Bot] Бот не инициализирован, обработчики не добавлены")
        return
    
    # Добавляем обработчик команды /start
    bot_application.add_handler(CommandHandler("start", start_command))
    
    # Добавляем обработчик обычных сообщений
    bot_application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("[Telegram Bot] Обработчики команд добавлены")

def run_bot_polling():
    """Запуск бота в режиме polling"""
    if not bot_application:
        print("[Telegram Bot] Бот не инициализирован, polling не запущен")
        return
    
    print("[Telegram Bot] Запуск polling...")
    bot_application.run_polling(allowed_updates=["message", "callback_query"], stop_signals=False)

if __name__ == "__main__":
    import uvicorn
    
    # Настраиваем обработчики бота
    setup_bot_handlers()
    
    # Запускаем бота в отдельном потоке
    if bot_application:
        bot_thread = threading.Thread(target=run_bot_polling, daemon=True)
        bot_thread.start()
        print("[Telegram Bot] Бот запущен в фоновом режиме")
    
    # Запускаем FastAPI сервер
    port = int(os.getenv("PORT", 8001))
    print(f"[FastAPI] Запуск сервера на порту {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

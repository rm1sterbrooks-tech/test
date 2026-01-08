"""
Отправка уведомлений в Telegram-бот
"""
import os
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

async def notify_telegram(chat_id: str, message_type: str, promocode: str = None):
    """Отправка уведомления напрямую через Telegram Bot API"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token:
        logger.warning("TELEGRAM_BOT_TOKEN не настроен. Уведомление не отправлено.")
        return
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    if message_type == "victory":
        text = f"🎉 Победа! Промокод выдан: {promocode}"
    elif message_type == "defeat":
        text = "😔 Проигрыш"
    elif message_type == "draw":
        text = "🤝 Ничья"
    else:
        text = f"Уведомление: {message_type}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": "HTML"
                }
            )
            response.raise_for_status()
            logger.info(f"Отправлено уведомление в Telegram: {message_type}")
            
    except Exception as e:
        logger.error(f"Ошибка отправки уведомления в Telegram: {e}", exc_info=True)


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
    """Отправка уведомления через Telegram-бот API"""
    bot_url = os.getenv("TELEGRAM_BOT_URL", "http://localhost:8001")
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            if message_type == "victory":
                message = f"🎉 Победа! Промокод выдан: {promocode}"
                await client.post(
                    f"{bot_url}/notify/victory",
                    json={"chat_id": chat_id, "promocode": promocode}
                )
                logger.info(
                    f"Отправлено уведомление о победе",
                    extra={
                        "chat_id": chat_id,
                        "message_type": "victory",
                        "promocode": promocode
                    }
                )
            elif message_type == "defeat":
                message = "😔 Проигрыш"
                await client.post(
                    f"{bot_url}/notify/defeat",
                    json={"chat_id": chat_id}
                )
                logger.info(
                    f"Отправлено уведомление о проигрыше",
                    extra={
                        "chat_id": chat_id,
                        "message_type": "defeat"
                    }
                )
            elif message_type == "draw":
                message = "🤝 Ничья"
                await client.post(
                    f"{bot_url}/notify/draw",
                    json={"chat_id": chat_id}
                )
                logger.info(
                    f"Отправлено уведомление о ничьей",
                    extra={
                        "chat_id": chat_id,
                        "message_type": "draw"
                    }
                )
    except httpx.TimeoutException as e:
        logger.warning(
            f"Таймаут при отправке уведомления в Telegram",
            extra={
                "chat_id": chat_id,
                "message_type": message_type,
                "error": "timeout",
                "error_message": str(e)
            }
        )
    except httpx.RequestError as e:
        logger.error(
            f"Ошибка подключения к Telegram боту",
            extra={
                "chat_id": chat_id,
                "message_type": message_type,
                "error": "request_error",
                "error_message": str(e),
                "bot_url": bot_url
            },
            exc_info=True
        )
    except Exception as e:
        logger.error(
            f"Ошибка отправки уведомления в Telegram",
            extra={
                "chat_id": chat_id,
                "message_type": message_type,
                "error": "unknown_error",
                "error_message": str(e)
            },
            exc_info=True
        )


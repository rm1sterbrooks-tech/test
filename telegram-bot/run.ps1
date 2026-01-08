# Скрипт для запуска Telegram-бота
Write-Host "Запуск Telegram-бота..." -ForegroundColor Green
Write-Host "Убедитесь, что установлены зависимости: py -m pip install -r requirements.txt" -ForegroundColor Yellow
Write-Host "Убедитесь, что настроен .env файл с TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID" -ForegroundColor Yellow

cd telegram-bot
py bot\main.py


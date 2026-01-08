# Скрипт для установки зависимостей проекта
Write-Host "Установка зависимостей проекта..." -ForegroundColor Green
py -m pip install -r requirements.txt
Write-Host "Зависимости установлены!" -ForegroundColor Green


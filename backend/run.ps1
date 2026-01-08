# Скрипт для запуска Backend API
Write-Host "Запуск Backend API..." -ForegroundColor Green
Write-Host "Убедитесь, что установлены зависимости: py -m pip install -r requirements.txt" -ForegroundColor Yellow

cd backend
py -m uvicorn app.main:app --reload --port 8000


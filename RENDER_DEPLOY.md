# Деплой на Render.com

## Шаг 1: Создание GitHub репозитория
1. Зайдите на https://github.com
2. Нажмите "New repository".
3. Название: `tictactoe-app`.
4. Выберите "Private".
5. Нажмите "Create repository".

## Шаг 2: Загрузка кода на GitHub
Выполните в PowerShell:
```powershell
cd d:\test
git init
git add .
git commit -m "Deploy with automatic bot linking"
git remote add origin https://github.com/YOUR_USERNAME/tictactoe-app.git
git push -u origin main
```

## Шаг 3: Создание сервисов на Render

### 1. Backend Service (tictactoe-backend)
- **Type**: Web Service
- **Environment**: Python 3
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `TELEGRAM_BOT_TOKEN`: (ваш токен)
  - `CORS_ORIGINS`: `https://ваша-ссылка-на-фронтенд.onrender.com`

### 2. Frontend Service (tictactoe-frontend)
- **Type**: Web Service
- **Environment**: Node
- **Root Directory**: `frontend`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npx serve -s dist -l $PORT`

### 3. Telegram Bot Service (tictactoe-bot)
- **Type**: Web Service
- **Environment**: Python 3
- **Root Directory**: `telegram-bot`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python bot/main.py`
- **Environment Variables**:
  - `TELEGRAM_BOT_TOKEN`: (ваш токен)
  - `BACKEND_URL`: `https://tictactoe-backend-v2.onrender.com`

---

## Как работает автоматическая привязка
1. Откройте игру.
2. Нажмите кнопку **"✨ Активировать Telegram-бота ✨"**.
3. В Telegram нажмите **"Start"**.
4. Вернитесь в игру — Chat ID подставится автоматически! 🎉

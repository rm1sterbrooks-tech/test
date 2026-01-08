# Деплой на Render.com

## Шаг 1: Создание GitHub репозитория
1. Зайдите на https://github.com
2. Нажмите "New repository" (зеленая кнопка справа)
3. Название: `tictactoe-app` (или любое другое)
4. Выберите "Private" (приватный репозиторий)
5. Нажмите "Create repository"

## Шаг 2: Загрузка кода на GitHub
Выполните в PowerShell:
```powershell
cd d:\test

# Инициализация Git (если еще не сделано)
git init

# Добавление всех файлов
git add .

# Коммит
git commit -m "Initial commit"

# Подключение к GitHub (замените YOUR_USERNAME на ваш логин)
git remote add origin https://github.com/YOUR_USERNAME/tictactoe-app.git

# Отправка кода
git push -u origin main
```

## Шаг 3: Создание сервисов на Render
1. Зайдите на https://dashboard.render.com
2. Нажмите "New +" -> "Web Service"
3. Подключите свой GitHub репозиторий

### Backend Service
- **Name**: `tictactoe-backend`
- **Environment**: Python 3
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Plan**: Free

### Frontend Service
# Деплой на Render.com

## Шаг 1: Создание GitHub репозитория
1. Зайдите на https://github.com
2. Нажмите "New repository" (зеленая кнопка справа)
3. Название: `tictactoe-app` (или любое другое)
4. Выберите "Private" (приватный репозиторий)
5. Нажмите "Create repository"

## Шаг 2: Загрузка кода на GitHub
Выполните в PowerShell:
```powershell
cd d:\test

# Инициализация Git (если еще не сделано)
git init

# Добавление всех файлов
git add .

# Коммит
git commit -m "Initial commit"

# Подключение к GitHub (замените YOUR_USERNAME на ваш логин)
git remote add origin https://github.com/YOUR_USERNAME/tictactoe-app.git

# Отправка кода
git push -u origin main
```

## Шаг 3: Создание сервисов на Render
1. Зайдите на https://dashboard.render.com
2. Нажмите "New +" -> "Web Service"
3. Подключите свой GitHub репозиторий

### Backend Service
- **Name**: `tictactoe-backend`
- **Environment**: Python 3
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Plan**: Free

### Frontend Service
- **Name**: `tictactoe-frontend`
- **Environment**: Node
- **Build Command**: `cd frontend && npm install && npm run build`
- **Start Command**: `cd frontend && npx serve -s dist -l $PORT`
- **Plan**: Free

### 3. Настройка уведомлений Telegram

Чтобы уведомления о победах и проигрышах приходили в Telegram, выполните следующие шаги:

#### В Backend (tictactoe-backend):
1. Перейдите в раздел **Environment**.
2. Добавьте переменную:
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `ваш_токен_бота` (от @BotFather)
3. Нажмите **Save Changes**.

#### Получение Chat ID:
Чтобы игра знала, куда отправлять уведомления, вам нужен ваш **Chat ID**.
1. Вы можете узнать его через бота `@userinfobot` в Telegram.
2. Или запустите нашего бота локально:
   - Откройте терминал в папке проекта.
   - Установите зависимости: `pip install -r telegram-bot/requirements.txt`
   - Создайте файл `telegram-bot/.env` с вашим токеном.
   - Запустите бота: `python telegram-bot/bot/main.py`
   - Напишите боту `/start`, и он пришлет вам ваш Chat ID.

3. Вставьте полученный **Chat ID** в поле ввода в самой игре. Он сохранится автоматически!

---

### Финальная проверка
1. Откройте Frontend URL.
2. Введите Chat ID.
3. Сыграйте партию.
4. После окончания игры вам должно прийти сообщение в Telegram! 🎉

### Bot Service (Background Worker)
- **Name**: `tictactoe-bot`
- **Environment**: Python 3
- **Build Command**: `cd telegram-bot && pip install -r requirements.txt`
- **Start Command**: `cd telegram-bot && python bot/main.py`
- **Plan**: Free
- **Environment Variables**:
  - `TELEGRAM_BOT_TOKEN`: (ваш токен)
  - `TELEGRAM_CHAT_ID`: (ваш chat ID)

## Шаг 4: Проверка
После развертывания Render даст вам публичный URL вида `https://tictactoe-frontend.onrender.com`

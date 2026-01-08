#!/bin/bash

# Настройки (замените на свои данные)
USER="root"
HOST="185.167.58.68"
DIR="/opt/tictactoe"

echo "🚀 Начинаем деплой на $HOST..."

# 1. Создаем директорию на сервере
ssh $USER@$HOST "mkdir -p $DIR"

# 2. Копируем файлы проекта
echo "📦 Копирование файлов..."
scp -r docker-compose.yml backend frontend telegram-bot $USER@$HOST:$DIR

# 3. Запускаем Docker Compose на сервере
echo "🔄 Пересборка и запуск контейнеров..."
ssh $USER@$HOST "cd $DIR && docker-compose down && docker-compose up -d --build"

echo "✅ Деплой завершен!"

# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаем пользователя без привилегий root
RUN adduser --disabled-password --gecos '' botuser && chown -R botuser:botuser /app
USER botuser

# Команда запуска
CMD ["python", "bot/main.py"]

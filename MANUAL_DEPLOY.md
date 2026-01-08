# Альтернативная инструкция: Деплой через Web Console

Если SSH не работает, можно развернуть проект вручную через Web Console.

## Шаг 1: Подключение к серверу
1. В панели управления вашего хостинга нажмите **ПОДКЛЮЧИТЬ** (CONNECT).
2. Нажмите кнопку **Открыть консоль** (Open Remote Console).
3. Войдите под пользователем `root` (пароль должен был прийти на почту).

## Шаг 2: Установка Docker (если не установлен)
Выполните в консоли:
```bash
# Обновление системы
apt update && apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Проверка
docker --version
```

## Шаг 3: Загрузка файлов проекта
Есть два варианта:

### Вариант A: Через Git (если проект в репозитории)
```bash
cd /opt
git clone https://github.com/ваш-username/ваш-репозиторий.git tictactoe
cd tictactoe
```

### Вариант Б: Ручная загрузка
1. Запакуйте проект на локальном компьютере:
   ```powershell
   Compress-Archive -Path docker-compose.yml,backend,frontend,telegram-bot -DestinationPath deploy.zip
   ```
2. Загрузите `deploy.zip` через SFTP/панель хостинга в `/opt/tictactoe`.
3. Распакуйте на сервере:
   ```bash
   cd /opt/tictactoe
   unzip deploy.zip
   ```

## Шаг 4: Запуск проекта
```bash
cd /opt/tictactoe
docker-compose up -d --build
```

## Шаг 5: Проверка
Откройте в браузере: `http://185.167.58.68:3000`

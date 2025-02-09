# Проект Alita

## Описание

Этот проект представляет собой Telegram-бот, который работает внутри Docker-контейнера. В проекте используется SQLite для хранения данных и Docker Compose для управления контейнерами.

## Структура проекта

- `main.py`: основной файл проекта.
- `Dockerfile`: файл конфигурации для сборки Docker-образа.
- `docker-compose.prod.yml` и `docker-compose.test.yml`: файлы конфигурации Docker Compose для продакшн и тестового окружений.
- `.github/workflows/deploy.yml`: файл конфигурации GitHub Actions для автоматической сборки и деплоя проекта.

## Требования

- Docker
- Docker Compose

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/yourusername/alita.git
    cd alita
    ```

## Запуск проекта локально
1. Установка необходимых зависимостей
   ```sh
    RUN pip install --user --no-cache-dir -r requirements.txt
    sudo apt install docker-ce
    sudo apt-get install docker-compose
    ```

2. Постройте и запустите контейнеры с помощью Docker Compose:
    ```sh
    docker-compose -f docker-compose.test.yml up -d --build

    docker-compose -f docker-compose.prod.yml up -d --build
    ```

3. Остановите контейнеры:
    ```sh
    docker-compose -f docker-compose.test.yml down

    docker-compose -f docker-compose.prod.yml down
    ```

## Автоматическое развертывание с помощью GitHub Actions

1. В файле `.github/workflows/deploy.yml` настроены шаги для автоматической сборки и деплоя проекта.
2. Добавьте секреты в настройки репозитория на GitHub (`Settings > Secrets and variables > Actions`):
    - `SERVER_PRIVATE_KEY`

3. Каждый раз при пуше в ветку `main` | `test` GitHub Actions автоматически выполнит сборку и деплой проекта на указанный сервер.


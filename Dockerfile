# Stage 1: Build
FROM python:3.9-slim as builder

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --user --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: Run
FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

# Создаем папку для базы данных
RUN mkdir -p /app/db

# Копируем существующую базу данных в контейнер
COPY messages.db /app/db/messages.db


# Создаем директорию для базы данных
#RUN mkdir -p /app/db
# Создаем символическую ссылку на файл базы данных
#RUN ln -s /app/db/messages.db /app/messages.db
#RUN mkdir -p /app/db && touch /app/db/messages.db && ln -sf /app/db/messages.db /app/messages.db
# Создаем символическую ссылку, если она не существует
#RUN ln -sf /app/db/messages.db /app/messages.db


EXPOSE 8000

CMD ["python", "main.py"]









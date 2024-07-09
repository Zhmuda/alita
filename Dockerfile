FROM python:3.9-slim as builder

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --user --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

# Создаем папку для базы данных
RUN mkdir -p /app/db

# Копируем существующую базу данных в контейнер
COPY messages.db /app/db/messages.db

CMD ["python", "main.py"]









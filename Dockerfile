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

# Создаем директорию для базы данных
RUN mkdir -p /app/db
# Создаем символическую ссылку на файл базы данных
RUN ln -s /app/db/messages.db /app/messages.db

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

CMD ["python", "main.py"]

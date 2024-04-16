# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем компилятор GCC
RUN apt-get update && \
    apt-get install -y build-essential

# Копируем исходный код в контейнер
COPY app /app
COPY req.txt req.txt

# Копируем файл .env в контейнер
COPY .env .env

# Устанавливаем зависимости
RUN pip install -r req.txt

# Переменные окружения для базы данных
ENV DATABASE_URL="postgresql://user:password@localhost/dbname"

# Задаем рабочую директорию
WORKDIR /app

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

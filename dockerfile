# Базовый образ Python
FROM python:3.12-slim

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Копирование файла requirements.txt в рабочую директорию
COPY requirements.txt .

# Установка зависимостей из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего содержимого текущей папки в рабочую директорию контейнера
COPY . .

# Команда для запуска бота (server.py)
CMD ["python", "server.py"]

# Используем базовый образ Python 3.10
FROM python:3.10-buster

# Устанавливаем переменную окружения PYTHONUNBUFFERED для лучшей работы с выводом
ENV PYTHONUNBUFFERED=1

# Копируем все файлы из текущего каталога в /app/ внутри контейнера
COPY . /app

# Устанавливаем рабочую директорию /app
WORKDIR /app

# Устанавливаем зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 8000
EXPOSE 8000

# Запускаем uvicorn для запуска вашего приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
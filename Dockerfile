# Используем официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт (если потребуется)
EXPOSE 8000

# Запускаем сервер
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]

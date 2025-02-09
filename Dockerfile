## Используем Python 3.12
#FROM python:3.12
#
## Устанавливаем рабочую директорию
#WORKDIR /app
#
## Копируем файлы проекта
#COPY . .
#
## Устанавливаем зависимости
#RUN pip install --no-cache-dir -r requirements.txt
#
## Запускаем сервер Django
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . .

# Указываем порт, который будет использовать приложение
EXPOSE 8000

# Команда для запуска приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
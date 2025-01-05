# Трекер Привычек

Проект представляет собой бэкенд-часть веб-приложения для отслеживания полезных привычек, с интеграцией с Telegram для отправки напоминаний. Приложение позволяет пользователю создавать, редактировать и удалять свои привычки, а также получать уведомления о их выполнении.

## Описание

Проект состоит из следующих ключевых компонентов:
- **Модели привычек** — пользователи могут создавать полезные и приятные привычки.
- **API для работы с привычками** — позволяет выполнять CRUD операции с привычками.
- **Пагинация** — выводит привычки по 5 на страницу.
- **Интеграция с Telegram** — для отправки напоминаний о привычках.
- **Тестирование и покрытие** — проект покрыт тестами на 80% и проверен с использованием Flake8.

## Требования

Перед запуском убедитесь, что у вас установлены следующие инструменты:
- Python 3.12+
- Redis (для работы с Celery)
- Telegram API Token (для интеграции с Telegram)

## Установка и настройка

1. Клонируйте репозиторий:
git clone https://github.com/your-repo-name.git
cd your-repo-name

2. Создайте и активируйте виртуальное окружение:
python3 -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows

3. Установите зависимости:
pip install -r requirements.txt

4. Создайте файл .env и добавьте необходимые переменные окружения:
TELEGRAM_API_TOKEN=your_telegram_api_token
CELERY_BROKER_URL=redis://localhost:6379/0
SECRET_KEY=your_django_secret_key
DEBUG=True

5. Примените миграции базы данных:
python manage.py migrate

6. Запустите сервер Django:
python manage.py runserver

# тестирование

coverage report

Name                                                         Stmts   Miss  Cover
--------------------------------------------------------------------------------
config/__init__.py                                               2      0   100%
config/celery.py                                                 6      0   100%
config/settings.py                                              44      0   100%
config/urls.py                                                  11      0   100%
habits/__init__.py                                               0      0   100%
habits/admin.py                                                  7      0   100%
habits/apps.py                                                   6      0   100%
habits/migrations/0001_initial.py                                8      0   100%
habits/migrations/0002_alter_profile_user.py                     6      0   100%
habits/migrations/__init__.py                                    0      0   100%
habits/models.py                                                34      4    88%
habits/permissions.py                                            6      3    50%
habits/serializers.py                                           14      2    86%
habits/signals.py                                                9      3    67%
habits/tests.py                                                 88      4    95%
habits/validators.py                                            16     10    38%
habits/views.py                                                 56     13    77%
manage.py                                                       11      2    82%
users/__init__.py                                                0      0   100%
users/admin.py                                                  14      0   100%
users/apps.py                                                    4      0   100%
users/migrations/0001_initial.py                                 5      0   100%
users/migrations/0002_alter_customuser_options_and_more.py       4      0   100%
users/migrations/__init__.py                                     0      0   100%
users/models.py                                                 43     11    74%
users/serializers.py                                            13      1    92%
users/tests.py                                                   1      0   100%
users/urls.py                                                    3      0   100%
users/views.py                                                  36     17    53%
--------------------------------------------------------------------------------
TOTAL                                                          447     70    84%

import logging
from celery import shared_task
from django.conf import settings
from django.utils import timezone
import telegram
from time import sleep
from .models import Habit


# Настройка логирования
logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_habit_reminders(self):
    """Отправка уведомлений о привычках через Telegram с повторными попытками."""
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    current_time = timezone.now().time()

    habits = Habit.objects.filter(time=current_time)
    for habit in habits:
        if habit.user.profile.telegram_chat_id:
            try:
                message = f"Напоминание: {habit.action} в {habit.place}."
                bot.send_message(
                    chat_id=habit.user.profile.telegram_chat_id, text=message
                )
            except telegram.error.TelegramError as e:
                # Логируем ошибку, если произошла ошибка Telegram API
                logger.error(f"Ошибка отправки уведомления для {habit.user.username}: {e}")
                # Пробуем снова через несколько секунд
                self.retry(countdown=60)
            except Exception as e:
                # Логируем все остальные ошибки
                logger.error(f"Ошибка при отправке уведомления для {habit.user.username}: {e}")
                # В случае другого исключения, мы не пытаемся повторить, а продолжаем цикл
                continue

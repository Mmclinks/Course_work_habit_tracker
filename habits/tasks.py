import telegram
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import Habit


@shared_task
def send_habit_reminders():
    """Отправка уведомлений о привычках через Telegram."""
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
            except Exception as e:
                print(f"Ошибка отправки уведомления: {e}")

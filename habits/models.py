from django.contrib.auth import get_user_model
from django.db import models

from .validators import (
    validate_execution_time,
    validate_periodicity,
    validate_pleasant_habit,
    validate_related_habit_is_pleasant,
    validate_reward_and_related_habit,
)

User = get_user_model()


class Habit(models.Model):
    """Модель привычки."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="related_to",
        verbose_name="Связанная привычка",
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        validators=[validate_periodicity],
        verbose_name="Периодичность (в днях)",
    )
    reward = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Вознаграждение"
    )
    execution_time = models.PositiveIntegerField(
        validators=[validate_execution_time],
        verbose_name="Время на выполнение (в секундах)",
    )
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]

    def clean(self):
        """Дополнительные валидации модели."""
        validate_reward_and_related_habit(self.reward, self.related_habit)
        validate_related_habit_is_pleasant(self.related_habit)
        validate_pleasant_habit(self.reward, self.related_habit, self.is_pleasant)

    def __str__(self):
        return f"{self.user.username} - {self.action} в {self.time}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_chat_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Telegram Chat ID"
    )

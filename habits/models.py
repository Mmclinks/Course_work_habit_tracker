from django.contrib.auth import get_user_model
from django.db import models
from .validators import (
    validate_execution_time,
    validate_periodicity,
    validate_pleasant_habit,
    validate_related_habit_is_pleasant,
    validate_reward_and_related_habit,
)
from django.core.exceptions import ValidationError

User = get_user_model()


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits", verbose_name="Пользователь")
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="related_to",
        verbose_name="Связанная привычка"
    )
    periodicity = models.PositiveIntegerField(default=1, verbose_name="Периодичность (в днях)")
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name="Вознаграждение")
    execution_time = models.PositiveIntegerField(verbose_name="Время на выполнение (в секундах)")
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]

    def clean(self):
        # Проверка, что приятная привычка не может иметь вознаграждение или связанную привычку
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")

        # Проверка на совместное использование reward и related_habit
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя указывать одновременно вознаграждение и связанную привычку.")

        # Проверка, что связанная привычка должна быть приятной
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной привычкой.")

    def __str__(self):
        return f"{self.user.email} - {self.action} в {self.time}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    telegram_chat_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Telegram Chat ID"
    )

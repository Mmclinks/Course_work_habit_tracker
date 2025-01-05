from django.core.exceptions import ValidationError


def validate_execution_time(value):
    """Проверка, что время выполнения <= 120 секунд."""
    if value > 120:
        raise ValidationError("Время выполнения не может превышать 120 секунд.")


def validate_periodicity(value):
    """Проверка, что периодичность от 1 до 7 дней."""
    if value < 1 or value > 7:
        raise ValidationError("Периодичность должна быть от 1 до 7 дней.")


def validate_reward_and_related_habit(reward, related_habit):
    """Исключаем одновременное указание вознаграждения и связанной привычки."""
    if reward and related_habit:
        raise ValidationError(
            "Нельзя указывать одновременно вознаграждение и связанную привычку."
        )


def validate_related_habit_is_pleasant(related_habit):
    """Связанная привычка должна быть приятной."""
    if related_habit and not related_habit.is_pleasant:
        raise ValidationError("Связанная привычка должна быть приятной привычкой.")


def validate_pleasant_habit(reward, related_habit, is_pleasant):
    """Приятная привычка не может иметь вознаграждение или связанную привычку."""
    if is_pleasant and (reward or related_habit):
        raise ValidationError(
            "Приятная привычка не может иметь вознаграждение или связанную привычку."
        )

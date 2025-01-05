from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        # Проверка на приятную привычку с вознаграждением или связанной привычкой
        if data.get('is_pleasant') and (data.get('reward') or data.get('related_habit')):
            raise serializers.ValidationError(
                "Приятная привычка не может иметь вознаграждение или связанную привычку."
            )

        # Проверка на совместное использование reward и related_habit
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError(
                "Нельзя указывать одновременно вознаграждение и связанную привычку."
            )

        # Проверка, что связанная привычка должна быть приятной
        if data.get('related_habit') and not data['related_habit'].is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной привычкой.")

        return data

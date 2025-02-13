import logging
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .permissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Habit
from .serializers import HabitSerializer

# Инициализируем логгер
logger = logging.getLogger(__name__)

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def public(self, request):
        public_habits = Habit.objects.filter(is_pleasant=True)  # Пример публичных привычек
        serializer = HabitSerializer(public_habits, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def private(self, request):
        private_habits = Habit.objects.filter(is_pleasant=False)  # Пример приватных привычек
        serializer = HabitSerializer(private_habits, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        if self.action == 'public_habits':
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)

        # Дополнительная проверка для приятных привычек
        if habit.is_pleasant and (habit.reward or habit.related_habit):
            raise serializers.ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")

        logger.info(f"Новая привычка создана пользователем {self.request.user.email}: {habit.action}")

    def perform_update(self, serializer):
        """Автоматически обновляем привычку и логируем изменения."""
        habit = serializer.save()
        logger.info(f"Привычка обновлена: {habit.action}")

    def perform_destroy(self, instance):
        """Автоматически удаляем привычку и логируем удаление."""
        logger.info(f"Привычка удалена пользователем {self.request.user.email}: {instance.action}")
        instance.delete()

    def handle_exception(self, exc):
        """Обработка исключений с логированием."""
        logger.error(f"Ошибка в HabitViewSet: {exc}")
        return super().handle_exception(exc)


class HabitCreateView(APIView):
    def post(self, request):
        serializer = HabitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublicHabitView(APIView):
    def get(self, request):
        """Получение публичных привычек."""
        habits = Habit.objects.filter(is_public=True)
        logger.info(f"Найдено публичных привычек: {habits.count()}")  # Логируем количество
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

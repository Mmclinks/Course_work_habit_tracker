from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Habit
from .permissions import IsOwnerOrReadOnly
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления привычками."""

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "time"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Возвращает набор данных в зависимости от действия."""
        if self.action == "public":
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Автоматически присваиваем пользователя при создании привычки."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="public")
    def public(self, request):
        """Список публичных привычек."""
        habits = Habit.objects.filter(is_public=True)
        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)


class HabitListCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = HabitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user
            )  # Предполагаем, что привычка привязана к пользователю
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HabitDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            habit = Habit.objects.get(pk=pk, user=request.user)
        except Habit.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = HabitSerializer(habit)
        return Response(serializer.data)


class HabitPublicListView(APIView):
    def get(self, request, format=None):
        habits = Habit.objects.filter(is_public=True)
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

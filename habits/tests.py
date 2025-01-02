from datetime import time

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit


class HabitModelTest(TestCase):
    """Тесты для модели Habit."""

    def setUp(self):
        """Создание пользователей и тестовых данных."""
        self.user = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass456")
        self.client.login(username="user1", password="pass123")

        # Привычки для user1
        Habit.objects.create(
            user=self.user,
            place="Парк",
            time=time(7, 0),
            action="Медитация",
            is_pleasant=False,
            periodicity=1,
            execution_time=60,
        )
        Habit.objects.create(
            user=self.user,
            place="Кафе",
            time=time(8, 0),
            action="Чтение",
            is_pleasant=True,
            periodicity=1,
            execution_time=45,
        )
        Habit.objects.create(
            user=self.user,
            place="Гора",
            time=time(9, 0),
            action="Прогулка",
            is_pleasant=True,
            periodicity=2,
            execution_time=120,
        )
        Habit.objects.create(
            user=self.user,
            place="Дерево",
            time=time(10, 0),
            action="Плавание",
            is_pleasant=False,
            periodicity=1,
            execution_time=30,
        )

        # Привычки для user2 (для проверки фильтрации)
        Habit.objects.create(
            user=self.user2,
            place="Сад",
            time=time(8, 0),
            action="Чтение",
            is_pleasant=True,
            periodicity=1,
            execution_time=30,
        )

    def test_habit_creation(self):
        """Тест создания привычки."""
        habit = Habit.objects.create(
            user=self.user,
            place="Парковка",
            time=time(18, 30),
            action="Прогулка",
            is_pleasant=False,
            periodicity=1,
            reward="Чашка кофе",
            execution_time=90,
            is_public=True,
        )
        self.assertEqual(habit.user.username, "user1")
        self.assertEqual(habit.place, "Парковка")
        self.assertEqual(habit.execution_time, 90)

    def test_habit_execution_time_validation(self):
        """Тест валидации времени выполнения привычки."""
        habit = Habit(
            user=self.user,
            place="Двор",
            time=time(19, 0),
            action="Бег",
            execution_time=150,  # Неверное время
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_habit_reward_and_related_validation(self):
        """Тест валидации одновременного использования reward и related_habit."""
        habit1 = Habit.objects.create(
            user=self.user,
            place="Сад",
            time=time(8, 0),
            action="Чтение",
            is_pleasant=True,
            execution_time=30,
        )
        habit2 = Habit(
            user=self.user,
            place="Комната",
            time=time(9, 0),
            action="Упражнения",
            reward="Шоколад",
            related_habit=habit1,
        )
        with self.assertRaises(ValidationError):
            habit2.full_clean()


class HabitAPITest(APITestCase):
    """Тесты для API привычек."""

    def setUp(self):
        """Создание пользователей и тестовых данных."""
        self.user = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass456")
        self.client.login(username="user1", password="pass123")

        self.habit = Habit.objects.create(
            user=self.user,
            place="Парк",
            time=time(7, 0),
            action="Медитация",
            is_pleasant=False,
            periodicity=1,
            execution_time=60,
        )
        # Добавляем дополнительные привычки для user1
        Habit.objects.create(
            user=self.user,
            place="Кафе",
            time=time(8, 0),
            action="Чтение",
            is_pleasant=True,
            periodicity=1,
            execution_time=45,
        )
        Habit.objects.create(
            user=self.user,
            place="Гора",
            time=time(9, 0),
            action="Прогулка",
            is_pleasant=True,
            periodicity=2,
            execution_time=120,
        )
        Habit.objects.create(
            user=self.user,
            place="Дерево",
            time=time(10, 0),
            action="Плавание",
            is_pleasant=False,
            periodicity=1,
            execution_time=30,
        )

    def test_get_user_habits(self):
        """Тест получения списка привычек пользователя."""
        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), Habit.objects.filter(user=self.user).count()
        )

    def test_create_habit(self):
        """Тест создания привычки."""
        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get("/api/habits/public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "place": "Кухня",
            "time": "08:00:00",
            "action": "Готовка завтрака",
            "is_pleasant": False,
            "periodicity": 1,
            "execution_time": 30,
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_access_others_habit(self):
        """Тест, что пользователь не может получить привычку другого пользователя."""
        self.client.logout()
        self.client.login(username="user2", password="pass456")
        response = self.client.get(f"/api/habits/{self.habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_public_habits(self):
        """Тест получения публичных привычек."""
        self.habit.is_public = True
        self.habit.save()
        response = self.client.get("/api/habits/public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.utils import timezone
from .models import Habit
from .serializers import HabitSerializer



User = get_user_model()

class HabitModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="password")
        self.related_habit = Habit.objects.create(
            user=self.user,
            action="Read",
            place="Home",
            reward=None,
            related_habit=None,
            time="08:00:00",  # Пример времени в правильном формате
            execution_time=30,
            periodicity=1,
            is_pleasant=False
        )

    def test_valid_habit_creation(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Home",
            time="08:00:00",
            action="Exercise",
            is_pleasant=True,
            periodicity=1,
            execution_time=60
        )
        self.assertEqual(habit.user, self.user)
        self.assertEqual(habit.place, "Home")
        self.assertEqual(habit.time, "08:00:00")
        self.assertEqual(habit.action, "Exercise")

    def test_invalid_related_habit_and_reward(self):
        habit = Habit(
            user=self.user,
            action="Test action",
            place="Test place",
            reward="Reward",  # Вознаграждение
            related_habit=self.related_habit,  # Связанная привычка
            time="08:00:00",  # Время в правильном формате
            execution_time=30,
            periodicity=1,
            is_pleasant=False
        )
        with self.assertRaises(ValidationError) as context:
            habit.full_clean()
        self.assertIn("Нельзя указывать одновременно вознаграждение и связанную привычку.",
                      context.exception.message_dict["__all__"])

    # def test_valid_habit(self):
    #     habit = Habit(
    #         user=self.user,
    #         place="Test Place",
    #         time="08:00:00",
    #         action="Test Action",
    #           # Без вознаграждения
    #           # Без связанной привычки
    #         is_pleasant=True,  # Приятная привычка
    #         periodicity=1,
    #         execution_time=60
    #     )
    #     try:
    #         habit.full_clean()  # Должно пройти без ошибок
    #     except ValidationError as e:
    #         self.fail(f"ValidationError was raised unexpectedly: {e}")

    def test_invalid_reward_and_related_habit(self):
        habit = Habit(
            user=self.user,
            action="Test action",
            place="Test place",
            reward="Reward",  # Вознаграждение
            related_habit=self.related_habit,  # Связанная привычка
            time="08:00:00",  # Время в правильном формате
            execution_time=30,
            periodicity=1,
            is_pleasant=False
        )
        try:
            habit.full_clean()  # Проверка валидации
            self.fail("ValidationError not raised")
        except ValidationError as e:
            self.assertIn("Нельзя указывать одновременно вознаграждение и связанную привычку.", e.message_dict["__all__"])

    def test_invalid_related_habit(self):
        habit = Habit(
            user=self.user,
            action="Test action",
            place="Test place",
            reward="Test reward",  # Вознаграждение
            related_habit=self.related_habit,  # Связанная привычка
            time="08:00:00",
            execution_time=30,
            periodicity=1,
            is_pleasant=False
        )
        try:
            habit.full_clean()  # Проверка валидации
            self.fail("ValidationError not raised")
        except ValidationError as e:
            self.assertIn("Нельзя указывать одновременно вознаграждение и связанную привычку.",
                          e.message_dict["__all__"])


class HabitSerializerTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="password")

    def test_valid_habit_serializer(self):
        data = {
            "user": self.user.id,
            "place": "Home",
            "time": "08:00:00",
            "action": "Exercise",
            "is_pleasant": True,
            "periodicity": 1,
            "execution_time": 60
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_habit_serializer_with_reward_and_related_habit(self):
        related_habit = Habit.objects.create(
            user=self.user,
            place="Home",
            time="08:00:00",
            action="Read",
            is_pleasant=False,
            reward=None,
            related_habit=None,
            periodicity=1,
            execution_time=60
        )

        data = {
            "user": self.user.id,
            "place": "Home",
            "time": "08:00:00",
            "action": "Exercise",
            "is_pleasant": False,
            "reward": "Reward",
            "related_habit": related_habit.id,
            "periodicity": 1,
            "execution_time": 60
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)


class HabitViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="password")
        self.client.login(email="testuser@example.com", password="password")

    def test_create_habit(self):
        url = '/api/habits/'
        data = {
            'user': self.user.id,
            'action': 'Test Habit',
            'place': 'Test Place',
            'reward': 'Test Reward',
            'related_habit': '',  # Пустое значение, если оно не обязательно
            'time': '08:00:00',
            'execution_time': 30,
            'periodicity': 1,
            'is_pleasant': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_get_public_habits(self):
        url = '/api/habits/public/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_private_habits(self):
        url = '/api/habits/private/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            action="Test action",
            place="Test place",
            reward="Test reward",  # Вознаграждение
            related_habit=None,  # Связанной привычки нет
            time="08:00:00",
            execution_time=30,
            periodicity=1,
            is_pleasant=False
        )
        url = f'/api/habits/{habit.id}/'

        # Обновляем привычку, сделав ее приятной
        # Но теперь не передаем поля reward и related_habit
        data = {
            'user': self.user.id,
            'action': 'Updated Habit',
            'place': 'Updated Place',
            'time': '08:00:00',
            'execution_time': 45,
            'periodicity': 1,
            'is_pleasant': True  # Обновляем на приятную привычку
        }

        response = self.client.put(url, data)

        # Ожидаем успешный ответ, так как не передаем запрещенные поля для приятной привычки
        self.assertEqual(response.status_code, 200)  # Ожидаем успешный ответ (200)

    def test_delete_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Home",
            action="Read",
            time="08:00:00",
            execution_time=60,
            is_pleasant=True,
            periodicity=1
        )
        url = f'/api/habits/{habit.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


    def test_create_useful_habit_with_reward(self):
        # Создание полезной привычки с вознаграждением
        response = self.client.post('/api/habits/', {
            'user': self.user.id,
            'action': 'Test Useful Habit',
            'place': 'Home',  # Обязательно указывать место
            'time': '12:00:00',  # Обязательно указывать время
            'reward': 'Dessert',
            'execution_time': 600,
        })
        self.assertEqual(response.status_code, 201)  # Полезная привычка может иметь вознаграждение

    def test_create_useful_habit_with_related_habit(self):
        # Создаем связанную привычку
        related_habit = Habit.objects.create(
            user=self.user,
            action='Related Habit',
            place='Gym',
            time='07:00:00',
            execution_time=600,
            is_pleasant=True,  # Связанная привычка должна быть приятной
        )

        # Теперь создаем полезную привычку с правильным ID related_habit
        response = self.client.post('/api/habits/', {
            'user': self.user.id,
            'action': 'Test Useful Habit',
            'place': 'Office',
            'time': '09:00:00',
            'related_habit': related_habit.id,  # Используем правильный ID для связанной привычки
            'execution_time': 600,
        })
        self.assertEqual(response.status_code, 201)  # Ожидаем успешный ответ


def test_create_pleasant_habit_without_related_or_reward(self):
    # Попытка создать приятную привычку без вознаграждения и связанной привычки
    response = self.client.post('/api/habits/', {
        'user': self.user.id,
        'action': 'Test Pleasant Habit',
        'place': 'Home',
        'time': '20:00:00',
        'is_pleasant': True,  # Приятная привычка
        'execution_time': 600,
    })
    self.assertEqual(response.status_code, 201)

from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "time", "is_pleasant", "is_public")
    list_filter = ("is_pleasant", "is_public", "periodicity")

    # Добавляем поиск по полям модели и связанным данным
    search_fields = (
        "action",  # Поиск по действию
        "user__username",  # Поиск по имени пользователя
        "user__first_name",  # Поиск по имени пользователя
        "user__last_name",  # Поиск по фамилии пользователя
        "place",  # Поиск по месту
        "reward",  # Поиск по вознаграждению
    )

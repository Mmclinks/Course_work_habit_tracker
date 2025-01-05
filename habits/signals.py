from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля пользователя, если он не существует."""
    if created:
        # Проверяем, существует ли уже профиль для этого пользователя
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)

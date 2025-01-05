from django.urls import path, include
from config.urls import router
from .views import HabitViewSet, PublicHabitView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

urlpatterns = [
    path("api/", include("rest_framework.urls")),
    path('api/habits/', include(router.urls)),
    path('api/habits/public/', HabitViewSet.as_view({'get': 'public'}), name='public_habits'),
    path('api/habits/private/', HabitViewSet.as_view({'get': 'private'}), name='private_habits'),
]

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoginSerializer

# Инициализируем логгер
logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        """Добавляем логирование успешной регистрации."""
        user = serializer.save()
        logger.info(f"Новый пользователь зарегистрирован: {user.email}")
        return user

    def handle_exception(self, exc):
        """Обработка исключений для улучшенного логирования."""
        if isinstance(exc, ValidationError):
            logger.error(f"Ошибка регистрации: {exc}")
        return super().handle_exception(exc)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                logger.info(f"Успешная авторизация: {user.email}")
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                logger.warning(f"Неудачная попытка входа: {serializer.validated_data['email']}")
                return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            logger.error(f"Ошибка авторизации: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

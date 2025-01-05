from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только владельцу объекта для модификации,
    для других методов разрешает доступ всем.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ для чтения (GET, HEAD, OPTIONS) всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешаем доступ на изменение (POST, PUT, PATCH, DELETE) только владельцу
        return obj.user == request.user

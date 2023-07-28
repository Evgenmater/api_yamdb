from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешние для Администратора и Суперпользователя."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.is_admin

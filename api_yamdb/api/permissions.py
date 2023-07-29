from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешние для Администратора и Суперпользователя."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Read for all user, other only Admin of super."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))

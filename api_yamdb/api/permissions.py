"""Permissions for API YAMDB."""
from rest_framework import permissions


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для автора/модератора/админа/суперпользователя
    или только чтение."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
                or request.user.is_superuser)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

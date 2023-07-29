"""Permissions for API YAMDB."""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Read for all user, other only Admin of super."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))

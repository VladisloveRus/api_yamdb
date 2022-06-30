from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or (
                request.user.is_authenticated and request.user.is_admin
        )


class ProfilePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method not in ("GET", "PATCH"):
            raise MethodNotAllowed(request.method)
        return request.user.is_authenticated

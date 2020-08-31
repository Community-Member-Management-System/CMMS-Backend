from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.related_community.admins.filter(id=request.user.id).exists() or request.user.is_superuser


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.related_community.admins.filter(id=request.user.id).exists() or request.user.is_superuser

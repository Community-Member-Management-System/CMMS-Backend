from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        found = obj.admins.filter(user_id=request.user.pk)

        return found

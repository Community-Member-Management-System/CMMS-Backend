from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user and obj.valid is True


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user and obj.valid is True


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        found = obj.admins.filter(id=request.user.pk)

        return found and obj.valid is True


class IsValidClubMember(permissions.BasePermission):
    # this permission does not include admins with valid=False
    def has_object_permission(self, request, view, obj):
        found = obj.members.filter(id=request.user.pk, membership__valid=True)

        return found and obj.valid is True

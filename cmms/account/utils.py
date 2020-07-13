from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from .models import User


def is_new_user(user: User):
    return not user.nick_name and not user.real_name


def valid_user_check(user: User):
    """
    Use with user_passes_test() or UserPassesTestMixin.
    It is extendable, as it's possible that a user may accept ToS to continue using our service in the future.
    See https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.decorators.user_passes_test
    """
    return not is_new_user(user)


class ValidUserPermission(permissions.BasePermission):
    """
    A DRF permission, functioning same as valid_user_check()
    See https://www.django-rest-framework.org/api-guide/permissions/
    """
    message = '需要补充用户信息（昵称与真实姓名）以使用剩余的功能。'

    def has_permission(self, request, view):
        return valid_user_check(request.user)


class ValidUserOrReadOnlyPermission(permissions.BasePermission):
    message = '需要补充用户信息（昵称与真实姓名）以进行修改。'

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            valid_user_check(request.user)
        )

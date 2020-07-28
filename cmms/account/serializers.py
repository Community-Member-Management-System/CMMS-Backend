from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import User


class PublicUserInfoSerializer(serializers.ModelSerializer):
    """
    Get information about a user that everyone could see
    """
    class Meta:
        model = User
        fields = ('pk', 'nick_name', 'avatar', 'profile')


class CurrentUserInfoSerializer(serializers.ModelSerializer):
    """
    Get current user information
    """
    class Meta:
        model = User
        exclude = ('gid', 'date_joined', 'last_login', 'is_staff', 'password',
                   'is_superuser', 'groups', 'user_permissions')
        read_only_fields = ('student_id',)
        required = ('real_name', 'nick_name')

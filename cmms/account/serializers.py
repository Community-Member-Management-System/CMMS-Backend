from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import SerializerMethodField

from .models import User
from communities.models import Community
from communities.serializers import CommunitySimpleSerializer


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
    communities = SerializerMethodField()

    def get_communities(self, user: User):
        user_communities_list = Community.objects.filter(membership__user=user).filter(valid=True)
        serializer = CommunitySimpleSerializer(user_communities_list, many=True)
        return serializer.data

    class Meta:
        model = User
        exclude = ('gid', 'date_joined', 'last_login', 'is_staff', 'password',
                   'is_superuser', 'groups', 'user_permissions')
        read_only_fields = ('student_id',)
        required = ('real_name', 'nick_name')


class NewUserSerializer(serializers.Serializer):
    new = serializers.BooleanField(label='是否为新用户')


class UserCheckSerializer(NewUserSerializer, serializers.Serializer):
    login = serializers.BooleanField(label='是否已经登录')
    userid = serializers.IntegerField(label='用户 ID')
    superuser = serializers.BooleanField(label='是否为超级用户')


class DetailSerializer(serializers.Serializer):
    detail = serializers.CharField(label='提示信息', allow_blank=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label='用户名')
    password = serializers.CharField(label='密码')


class LoginResponseSerializer(NewUserSerializer, DetailSerializer):
    pass


class LimitedFilterResponseSerializer(serializers.Serializer):
    student_id = serializers.CharField(label='学号')
    real_name = serializers.CharField(label='真实姓名', allow_blank=True)

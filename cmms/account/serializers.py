from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import User


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    """
    Get information about a user that everyone could see
    """
    class Meta:
        model = User
        fields = ('url', 'nick_name', 'avatar_url', 'profile')

    def validate(self, data):
        pass

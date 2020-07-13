from rest_framework.serializers import ModelSerializer, BooleanField, Serializer
from rest_framework.exceptions import ValidationError

from .models import Community


class CommunitySerializer(ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'
        read_only_fields = ['creator', 'owner', 'date_created', 'members', 'admins']


class OwnershipTransferSerializer(ModelSerializer):
    def validate_owner(self, value):
        if value not in self.instance.membership_set.all():
            raise ValidationError('Specified user is not a member of the community')

    class Meta:
        model = Community
        fields = ['owner']


class CommunityDetailSerializer(ModelSerializer):
    class Meta:
        model = Community
        fields = ('name', 'profile')


class CommunityJoinSerializer(Serializer):
    join = BooleanField(label='加入', required=True, read_only=False)

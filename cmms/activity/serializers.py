from typing import Union

from .models import Activity
from rest_framework import serializers
from django.utils import timezone
from communities.serializers import MemberSerializer, CommunitySimpleSerializer
from communities.models import Community


class BaseActivitySerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')
    signed_in_users = serializers.SerializerMethodField('get_signed_in_users')
    related_community: 'Union[CommunitySimpleSerializer, serializers.PrimaryKeyRelatedField]' \
        = CommunitySimpleSerializer()

    def get_status(self, activity: Activity):
        now = timezone.now()
        if now >= activity.end_time:
            return '已结束'
        elif now > activity.start_time:
            return '进行中'
        else:
            return '未开始'

    def get_signed_in_users(self, activity: Activity):
        signed_in_users = activity.signed_in_users
        serializer = MemberSerializer(
            instance=signed_in_users,
            context={
                'community': activity.related_community,
                'admin': activity.related_community.is_admin(self.context.get('user')),
            },
            many=True
        )
        return serializer.data


class ActivitySerializer(BaseActivitySerializer):
    class Meta:
        model = Activity

        fields = [
            'id',
            'related_community',
            'location',
            'title',
            'description',
            'start_time',
            'end_time',
            'signed_in_users',
            'created_date',
            'status',
            'longitude',
            'latitude'
        ]

        read_only_fields = ['created_date', 'status', 'signed_in_users']


class PostVerActivitySerializer(ActivitySerializer):
    related_community = serializers.PrimaryKeyRelatedField(queryset=Community.objects.all())


class ActivityUpdateSerializer(BaseActivitySerializer):
    class Meta:
        model = Activity

        fields = [
            'id',
            'related_community',
            'location',
            'title',
            'description',
            'start_time',
            'end_time',
            'signed_in_users',  # TODO: Do we need another API to sign in users incrementally? E.g., sign in users [1,2]
            'created_date',
            'status',
            'longitude',
            'latitude'
        ]

        read_only_fields = ['created_date', 'status', 'related_community']


class PostVerActivityUpdateSerializer(ActivityUpdateSerializer):
    related_community = serializers.PrimaryKeyRelatedField(read_only=True)


class ActivitySecretKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity

        fields = ['secret_key']


class ActivityOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()


class ActivitySignedInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity

        fields = ['signed_in_users']

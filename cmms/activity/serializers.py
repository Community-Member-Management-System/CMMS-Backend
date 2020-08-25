from .models import Activity
from rest_framework import serializers
from django.utils import timezone


class BaseActivitySerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        now = timezone.now()
        if now >= obj.end_time:
            return '已结束'
        elif now > obj.start_time:
            return '进行中'
        else:
            return '未开始'


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
        ]

        read_only_fields = ['created_date', 'status', 'signed_in_users']


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
        ]

        read_only_fields = ['created_date', 'status', 'related_community']


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

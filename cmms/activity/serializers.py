from .models import Activity
from rest_framework import serializers
from django.utils import timezone


class ActivitySerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        now = timezone.now()
        if now >= obj.end_time:
            return '已结束'
        elif now > obj.start_time:
            return '进行中'
        else:
            return '未开始'

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

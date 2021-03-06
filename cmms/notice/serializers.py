from rest_framework import serializers
from .models import Notice, NoticeBox


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            'date', 'type', 'related_user', 'related_community',
            'related_comment', 'related_activity', 'subtype', 'description'
        ]


class NoticeBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeBox
        fields = ['pk', 'read', 'administrative']


class NoticeViewSerializer(serializers.Serializer):
    pk = serializers.IntegerField(label='Notice ID')
    method = serializers.CharField(label='read, unread, delete, or others')

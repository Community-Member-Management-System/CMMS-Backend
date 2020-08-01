from account.utils import ValidUserPermission
from .serializers import NoticeSerializer, NoticeBoxSerializer
from .models import Notice, NoticeBox
from .utils import NoticeManager
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.utils import timezone


class NoticeView(APIView):
    permission_classes = [ValidUserPermission]

    def get(self, request, format=None):
        user = request.user
        notice_list = NoticeManager.fetch(user)
        serializer = NoticeBoxSerializer(notice_list, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user
        pk = request.data.get('pk')
        method = request.data.get('method')
        if method == 'read':
            NoticeManager.read(user, pk)
        elif method == 'unread':
            NoticeManager.unread(user, pk)
        elif method == 'delete':
            NoticeManager.delete(user, pk)
        else:
            notice = NoticeManager.access(user, pk)
            serializer = NoticeSerializer(notice)
            return Response(serializer.data)
        return Response(status=status.HTTP_200_OK)

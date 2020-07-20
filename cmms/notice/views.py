from .serializers import NoticeSerializer, NoticeBoxSerializer
from .models import Notice, NoticeBox
from .utils import NoticeManager
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.utils import timezone


class NoticeView(APIView):
    def get(self, request, format=None):
        user = request.user
        if user.is_authenticated:
            notice_list = NoticeManager.fetch(user)
            serializer = NoticeBoxSerializer(notice_list, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        user = request.user
        pk = request.data.get('notice')
        if user.is_authenticated:
            notice = NoticeManager.access(user, pk)
            serializer = NoticeSerializer(notice)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# class Test(APIView):
#     def get(self, request, format=None):
#         notice = Notice.objects.create(type='B', related_user=request.user)
#         NoticeBox.objects.create(user=request.user, notice=notice, read=False, deleted=False)
#         return Response(status=status.HTTP_200_OK)

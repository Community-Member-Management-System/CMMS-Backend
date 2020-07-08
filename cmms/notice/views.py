from .serializers import NoticeSerializer, NoticeBoxSerializer
from .models import Notice, NoticeBox
from .utils import notice_namager
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required


class NoticeList(APIView):
    def get(self, request, format=None):
        user = request.user
        if user.is_authenticated:
            notice_list = notice_namager.fetch(user)
            serializer = NoticeBoxSerializer(notice_list, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class NoticeDetail(APIView):
    def post(self, request, format=None):
        user = request.user
        pk = request.data.get('notice')
        if user.is_authenticated:
            notice = notice_namager.access(user, pk)
            serializer = NoticeSerializer(notice)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

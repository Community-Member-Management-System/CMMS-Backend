from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .serializers import ActivitySerializer
from .permissions import IsAdminOrReadOnly
from .models import Activity
from account.utils import ValidUserOrReadOnlyPermission


# Create your views here.
class ActivityListView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAdminOrReadOnly,
                          ValidUserOrReadOnlyPermission]

    def get_queryset(self):
        community = self.request.query_params.get('community', None)
        if community is None:
            return Activity.objects.all()
        return Activity.objects.filter(related_community__pk=community).all()

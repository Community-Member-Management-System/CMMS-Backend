from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from django.db import transaction

from account.utils import ValidUserOrReadOnlyPermission

from .serializers import CommunitySerializer, OwnershipTransferSerializer, CommunityDetailSerializer
from .permissions import IsOwnerOrReadOnly
from .models import Community


# Create your views here.
class CommunityListView(generics.ListCreateAPIView):
    permission_classes = [ValidUserOrReadOnlyPermission]
    serializer_class = CommunitySerializer
    queryset = Community.objects.all()

    def perform_create(self, serializer):
        with transaction.atomic():
            community = serializer.save(creator=self.request.user,
                                        owner=self.request.user)
            community.admins.add(self.request.user)
            community.members.add(self.request.user, through_defaults={'valid': True})


class CommunityTransferView(generics.UpdateAPIView):
    permission_classes = [ValidUserOrReadOnlyPermission,
                          IsOwnerOrReadOnly]
    serializer_class = OwnershipTransferSerializer
    queryset = Community.objects.all()


class CommunityRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [ValidUserOrReadOnlyPermission,
                          IsOwnerOrReadOnly]
    serializer_class = CommunityDetailSerializer
    queryset = Community.objects.all()

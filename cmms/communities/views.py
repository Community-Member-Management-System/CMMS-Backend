from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from .serializers import CommunitySerializer, OwnershipTransferSerializer
from .permissions import IsOwnerOrReadOnly
from .models import Community


# Create your views here.
class CommunityListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommunitySerializer
    queryset = Community.objects.all()

    def perform_create(self, serializer):
        community = serializer.save(creator=self.request.user,
                                    owner=self.request.user)
        community.admins.add(self.request.user)
        community.members.add(self.request.user)


class CommunityTransferView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    serializer_class = OwnershipTransferSerializer
    queryset = Community.objects.all()

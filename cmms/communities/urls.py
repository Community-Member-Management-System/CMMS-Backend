from django.urls import path
from . import views

app_name = 'communities'
urlpatterns = [
    path('', views.CommunityListView.as_view(), name='list_create'),
    path('transfer/<int:pk>', views.CommunityTransferView.as_view(), name='transfer'),
    path('<int:pk>', views.CommunityRetrieveUpdateView.as_view(), name='retrieve_update'),
]

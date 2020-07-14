from django.urls import path
from . import views

app_name = 'communities'
urlpatterns = [
    path('', views.CommunityListView.as_view(), name='list_create'),
    path('<int:pk>/transfer', views.CommunityTransferView.as_view(), name='transfer'),
    path('<int:pk>', views.CommunityRetrieveUpdateView.as_view(), name='retrieve_update'),
    path('<int:pk>/delete', views.CommunityDestroyView.as_view(), name='delete'),
    path('<int:pk>/join', views.CommunityJoinView.as_view(), name='join'),
    path('<int:pk>/audit', views.CommunityNewMemberAuditView.as_view(), name='new_member'),
    path('<int:pk>/audit/<int:user_id>/<str:action>',
         views.CommunityNewMemberAuditActionView.as_view(), name='new_member_action')
]

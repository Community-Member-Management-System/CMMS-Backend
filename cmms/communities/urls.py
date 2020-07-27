from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'audit', views.CommunitySysAdminAuditViewSet)
router.register(r'invitation', views.CommunityUserInvitationViewSet, 'Invitation')


app_name = 'communities'
urlpatterns = [
    path('', views.CommunityListView.as_view(), name='list_create'),
    path('<int:pk>/transfer', views.CommunityTransferView.as_view(), name='transfer'),
    path('<int:pk>', views.CommunityRetrieveView.as_view(), name='retrieve'),
    path('<int:pk>/update', views.CommunityInfoRetrieveUpdateView.as_view(), name='retrieve_update_info'),
    path('<int:pk>/delete', views.CommunityDestroyView.as_view(), name='delete'),
    path('<int:pk>/join', views.CommunityJoinView.as_view(), name='join'),
    path('<int:pk>/audit', views.CommunityNewMemberAuditView.as_view(), name='new_member'),
    path('<int:pk>/audit/<int:user_id>/<str:action>',
         views.CommunityNewMemberAuditActionView.as_view(), name='new_member_action'),
    path('<int:pk>/invite', views.CommunityAdminInviteView.as_view(), name='invite'),
    path('<int:pk>/invite/<int:user_id>', views.CommunityAdminSendInvitationView.as_view(), name='send_invitation')
]

urlpatterns += router.urls

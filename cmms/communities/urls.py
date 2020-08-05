from django.urls import path
from . import views, feed
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'audit', views.CommunitySysAdminAuditViewSet)
router.register(r'invitation', views.CommunityUserInvitationViewSet, 'Invitation')


app_name = 'communities'
urlpatterns = [
    path('', views.CommunityListView.as_view(), name='list_create'),
    path('<int:pk>/transfer', views.CommunityTransferView.as_view(), name='transfer'),
    path('<int:pk>', views.CommunityRetrieveUpdateView.as_view(), name='retrieve_update'),
    path('<int:pk>/join', views.CommunityJoinView.as_view(), name='join'),
    path('<int:pk>/audit', views.CommunityNewMemberAuditView.as_view(), name='new_member'),
    path('<int:pk>/audit/<int:user_id>/<str:action>',
         views.CommunityNewMemberAuditActionView.as_view(), name='new_member_action'),
    path('<int:pk>/invite', views.CommunityAdminInviteView.as_view(), name='invite'),
    path('<int:pk>/invite/<int:user_id>', views.CommunityAdminSendInvitationView.as_view(), name='send_invitation'),
    path('<int:pk>/members/<int:user_id>', views.CommunityUserRemoveView.as_view(), name='member_delete'),
    path('<int:pk>/members/<int:user_id>/admin/<str:action>',
         views.CommunityAdminSetView.as_view(), name='admin_action'),
    path('<int:pk>/feed.ics', feed.CommunityEventCalendarFeed(), name='ics_feed'),
    path('<int:pk>/atom.xml', feed.CommunityEventRSSFeed(), name='rss_feed'),
    path('<int:pk>/checklist', views.CommunityCheckListViewSet.as_view({
        'get': 'retrieve',
    }), name='checklist_retrieve'),
    path('<int:pk>/checklist/create', views.CommunityCheckListViewSet.as_view({
        'post': 'create_item',
    }), name='checklist_create_item'),
    path('<int:pk>/checklist/remove', views.CommunityCheckListViewSet.as_view({
        'post': 'remove_item',
    }), name='checklist_remove_item'),
    path('<int:pk>/checklist/set', views.CommunityCheckListViewSet.as_view({
        'post': 'set_item',
    }), name='checklist_set_item'),
]

urlpatterns += router.urls

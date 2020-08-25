from django.urls import path
from . import views

app_name = 'activity'

urlpatterns = [
    path('', views.ActivityListView.as_view(), name='list_create'),
    path('<int:pk>', views.ActivityDetailUpdateDestroyView.as_view(), name='detail_update_destroy'),
    path('<int:pk>/sign_in', views.ActivitySignInView.as_view(), name='sign_in'),
    path('<int:pk>/secret_key', views.ActivitySecretKeyView.as_view(), name='secret_key'),
    path('<int:pk>/signed_in_list', views.ActivitySignedInViewSet.as_view({
        'get': 'retrieve'
    }), name='retrieve_signed_in_list'),
    path('<int:pk>/signed_in_list/add/<int:user_id>', views.ActivitySignedInViewSet.as_view({
        'post': 'add'
    }), name='signed_in_list_add'),
    path('<int:pk>/signed_in_list/remove/<int:user_id>', views.ActivitySignedInViewSet.as_view({
        'post': 'remove'
    }), name='signed_in_list_remove'),
]

from django.urls import path
from . import views

app_name = 'activity'

urlpatterns = [
    path('', views.ActivityListView.as_view(), name='list_create'),
    path('<int:pk>', views.ActivityDetailUpdateDestroyView.as_view(), name='detail_update_destroy'),
    path('<int:pk>/sign_in', views.ActivitySignInView.as_view(), name='sign_in'),
    path('<int:pk>/secret_key', views.ActivitySecretKeyView.as_view(), name='secret_key'),
]

from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'users/public', views.ReadOnlyUserViewSet)

urlpatterns = [
    # path('auth/', include('rest_framework.urls')),
    path('auth/traditional_login', views.BaseLoginView.as_view(), name='traditional_login'),
    path('auth/cas_login', views.CASLoginView.as_view(), name='cas_login'),
    path('auth/logout', views.LogoutView.as_view(), name='logout'),
    path('users/current', views.CurrentUserInfoView.as_view(), name='self_profile'),
]

urlpatterns += router.urls

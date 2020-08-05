from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)

app_name = 'account'
urlpatterns = [
    # path('auth/', include('rest_framework.urls')),
    path('auth/traditional_login', views.BaseLoginView.as_view(), name='traditional_login'),
    path('auth/cas_login', views.CASLoginView.as_view(), name='cas_login'),
    path('auth/logout', views.LogoutView.as_view(), name='logout'),
    path('auth/check', views.LoginCheckView.as_view(), name='check'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += router.urls

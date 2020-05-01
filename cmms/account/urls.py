from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
]

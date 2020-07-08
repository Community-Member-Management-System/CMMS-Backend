from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('', views.NoticeList.as_view()),
    path('access', views.NoticeDetail.as_view()),
]

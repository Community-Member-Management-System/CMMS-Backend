from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('', views.NoticeView.as_view()),
    # path('test', views.Test.as_view()),
]

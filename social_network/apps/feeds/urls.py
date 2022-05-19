from django.urls import path

from . import views


urlpatterns = [
    path('feed/get', views.GetFeed.as_view()),
]
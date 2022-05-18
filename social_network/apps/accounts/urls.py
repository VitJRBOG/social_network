from django.urls import path

from . import views


urlpatterns = [
    path('profile/add', views.AddProfile.as_view())
]
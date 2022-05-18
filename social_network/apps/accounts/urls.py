from django.urls import path

from . import views


urlpatterns = [
    path('profile/add', views.AddProfile.as_view()),
    path('profile/get', views.GetProfileInfo.as_view()),
    path('profile/delete', views.DeleteProfile.as_view()),
]
from django.urls import path

from . import views


urlpatterns = [
    path('blog/add', views.AddBlog.as_view()),
    path('blog/get', views.GetBlog.as_view()),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("like", views.like, name='like'),
    path ("profile/<str:author>", views.profile, name='profile'),
    path("following", views.follower, name='following'),
    path ("following_page", views.following_page, name='following_page'),
    path ("search_page", views.search_page, name= 'search_page')
]

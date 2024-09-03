
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name = 'create'),
    path("post/<int:id>", views.post_view , name = 'post_view'),
    path("like/<int:id>", views.like_view, name="like_view"),
    path("count/<int:id>", views.like_count, name="like_count"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("follow/<int:id>", views.follow_count, name = 'follow_view'),
    path("following", views.following, name="following"),
    path("edit/<int:id>", views.edit, name = "edit")
]

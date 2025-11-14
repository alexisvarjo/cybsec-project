from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin/", views.admin_panel, name="admin_panel"),
    path("register/", views.register, name="register"),
    path("users_public/", views.users_public, name="users_public"),
]

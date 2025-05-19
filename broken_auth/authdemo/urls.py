from django.urls import path
from .views import register, login, password_reset, index, dashboard, user_detail

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("password_reset/", password_reset, name="password_reset"),
    path("dashboard/<int:user_id>/", dashboard, name="dashboard"),
    path("user/<int:user_id>/", user_detail, name="user_detail"),
]

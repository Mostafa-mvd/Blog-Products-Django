from django.urls import path
from django.urls.conf import include
from . import views


app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("edit/", views.EditUserProfile.as_view(), name='edit_profile'),
]

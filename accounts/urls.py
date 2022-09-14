from django.urls import path
from django.contrib.auth import views

from accounts.views import UserCreateView, UpdateUserView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name='register'),
    path("login/", views.LoginView.as_view(), name='login'),
    path("logout/", views.LogoutView.as_view(), name='logout'),
    path("update/profile/<slug>", UpdateUserView.as_view(), name="update_profile"),

]


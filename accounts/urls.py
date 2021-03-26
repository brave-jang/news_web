from django.urls import path
from . import views

app_name = "accounts"


urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("profile_update/", views.UpdateProfileView.as_view(), name="profile_update"),
    path("change_password/", views.ChangePassword.as_view(), name="change_password"),
]
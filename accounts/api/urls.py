from django.urls import path
from .views import RegisterView, LoginView, ListUserView
from .views import (
    RegisterView,
    LoginView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutView,
    BlacklistTokenView,
    PasswordResetView,
    # PasswordResetConfirmView,
    CustomPasswordResetConfirmView,
)
from django.contrib.auth.views import PasswordResetConfirmView


urlpatterns = [
    #
    # account
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("users/", ListUserView.as_view(), name="list-user"),
    path("logout/", LogoutView.as_view(), name="logout"),
    #
    # token
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/blacklist/", BlacklistTokenView.as_view(), name="token_blacklist"),
    #
    # password
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    # path(
    #     "password-reset-confirm/",
    #     PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    #
    # reset
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]

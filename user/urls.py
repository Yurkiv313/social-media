from user.views import LogoutView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from accounts.views import PublicProfileView
from user.views import (
    CreateUserView,
    UserListView,
)

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/profile/", PublicProfileView.as_view(), name="public_profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

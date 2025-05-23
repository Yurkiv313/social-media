from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from user.serializers import (
    UserCreateSerializer,
    UserReadSerializer,
    UserUpdateSerializer,
)

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserReadSerializer
        return UserUpdateSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    filter_backends = [SearchFilter]
    search_fields = ["email", "first_name", "last_name"]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserReadSerializer

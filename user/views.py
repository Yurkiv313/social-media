from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import Follow
from user.serializers import (
    UserCreateSerializer,
    UserReadSerializer, FollowingListSerializer, FollowersListSerializer,
)
from drf_spectacular.utils import extend_schema
from user.schema_descriptions import (
    register_schema,
    logout_schema,
    user_list_schema,
    follow_schema,
    following_list_schema,
    followers_list_schema,
)

User = get_user_model()


@extend_schema(**register_schema)
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


@extend_schema(**user_list_schema)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    filter_backends = [SearchFilter]
    search_fields = ["email", "first_name", "last_name"]

@extend_schema(**logout_schema)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema(**follow_schema)
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return Response({
            "message": f"This endpoint is for following and unfollowing user {pk}."
                       f" Send a POST request to follow."
                       f" Send a DELETE request to unfollow."
        })

    def post(self, request, pk):
        follow_user = User.objects.get(pk=pk)
        current_user = request.user

        if follow_user == current_user:
            return Response({"detail": "You cannot follow yourself."}, status=400)

        if Follow.objects.filter(follower=current_user, following=follow_user).exists():
            return Response({"detail": "Already following."}, status=400)

        Follow.objects.create(follower=current_user, following=follow_user)
        return Response({"detail": f"You are now following user {follow_user.id}."}, status=201)

    def delete(self, request, pk):
        try:
            follow_user = User.objects.get(pk=pk)
        except get_user_model().DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        follow = Follow.objects.filter(follower=request.user, following=follow_user)
        if follow.exists():
            follow.delete()
            return Response({"detail": "Unfollowed successfully."}, status=204)
        return Response({"detail": "You are not following this user."}, status=400)


@extend_schema(**following_list_schema)
class FollowingListView(generics.ListAPIView):
    serializer_class = FollowingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.select_related("following").filter(follower=self.request.user)


@extend_schema(**followers_list_schema)
class FollowersListView(generics.ListAPIView):
    serializer_class = FollowersListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.select_related("follower").filter(following=self.request.user)

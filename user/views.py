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

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    filter_backends = [SearchFilter]
    search_fields = ["email", "first_name", "last_name"]


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


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return Response({
            "message": f"This endpoint is for following and unfollowing user {pk}.\n"
                       f" Send a POST request to follow.\n"
                       f" Send a DELETE request to unfollow."
        })

    def post(self, request, pk):
        follow_user = get_user_model().objects.get(pk=pk)
        current_user = request.user

        if follow_user == current_user:
            return Response({"detail": "You cannot follow yourself."}, status=400)

        if Follow.objects.filter(follower=current_user, following=follow_user).exists():
            return Response({"detail": "Already following."}, status=400)

        Follow.objects.create(follower=current_user, following=follow_user)
        return Response({"detail": f"You are now following user {follow_user.id}."}, status=201)

    def delete(self, request, pk):
        try:
            follow_user = get_user_model().objects.get(pk=pk)
        except get_user_model().DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        follow = Follow.objects.filter(follower=request.user, following=follow_user)
        if follow.exists():
            follow.delete()
            return Response({"detail": "Unfollowed successfully."}, status=204)
        return Response({"detail": "You are not following this user."}, status=400)


class FollowingListView(generics.ListAPIView):
    serializer_class = FollowingListSerializer

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)


class FollowersListView(generics.ListAPIView):
    serializer_class = FollowersListSerializer

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user)

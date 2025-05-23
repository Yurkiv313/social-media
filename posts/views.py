from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Post
from posts.permissions import IsAuthorOrReadOnly
from posts.serializers import PostListSerializer, PostRetrieveSerializer
from user.models import Follow


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author")
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        following_users = Follow.objects.filter(
            follower=self.request.user
        ).values_list("following", flat=True)

        queryset = Post.objects.filter(
            Q(author=self.request.user) | Q(author__in=following_users)
        ).select_related("author")

        hashtag = self.request.query_params.get("hashtag")
        if hashtag:
            queryset = queryset.filter(hashtags__icontains=hashtag)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostRetrieveSerializer




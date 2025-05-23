from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Post
from posts.permissions import IsAuthorOrReadOnly
from posts.serializers import PostListSerializer, PostRetrieveSerializer
from user.models import Follow

from drf_spectacular.utils import extend_schema
from posts.schema_descriptions import (
    post_list_schema,
    post_create_schema,
    post_detail_schema,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author")
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        following_users = Follow.objects.filter(
            follower=self.request.user
        ).values_list(
            "following", flat=True
        )

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

    @extend_schema(**post_list_schema)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(**post_create_schema)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(**post_detail_schema)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(**post_detail_schema)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(**post_detail_schema)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(**post_detail_schema)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

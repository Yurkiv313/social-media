from rest_framework import serializers

from posts.models import Post


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "author", "content", "hashtags")

    def get_author(self, obj):
        return {
            "id": obj.author.id,
            "email": obj.author.email,
            "first_name": obj.author.first_name,
        }


class PostRetrieveSerializer(PostListSerializer):
    class Meta:
        model = Post
        fields = ("id", "author", "content", "created_at", "image", "hashtags")
        read_only_fields = ("author", "created_at")

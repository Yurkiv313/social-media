from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import Follow

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff")
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "is_staff")
        read_only_fields = fields


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("id", "follower", "following", "created_at")


class FollowingListSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="following.email", read_only=True)
    first_name = serializers.CharField(source="following.first_name", read_only=True)

    class Meta:
        model = Follow
        fields = ("email", "first_name", "created_at")
        read_only_fields = fields


class FollowersListSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="follower.email", read_only=True)
    first_name = serializers.CharField(source="follower.first_name", read_only=True)

    class Meta:
        model = Follow
        fields = ("email", "first_name", "created_at")
        read_only_fields = fields

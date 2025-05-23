from rest_framework import serializers
from accounts.models import Profile


class PublicProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="user.email")
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")

    class Meta:
        model = Profile
        fields = (
            "id", "email", "first_name", "last_name",
            "bio", "location", "image", "created_at", "updated_at"
        )


class FullProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Profile
        fields = (
            "id", "email", "first_name", "last_name",
            "bio", "location", "image", "created_at", "updated_at"
        )
        read_only_fields = ("id", "email", "created_at", "updated_at")

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        return super().update(instance, validated_data)

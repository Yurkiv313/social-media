from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.models import Profile
from accounts.permissions import IsOwnerProfile
from accounts.serializers import PublicProfileSerializer, FullProfileSerializer

from drf_spectacular.utils import extend_schema
from accounts.schema_descriptions import (
    own_profile_schema,
    public_profile_schema
)


@extend_schema(**own_profile_schema)
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = FullProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfile]

    def get_object(self):
        return self.request.user.profile


@extend_schema(**public_profile_schema)
class PublicProfileView(generics.RetrieveAPIView):
    serializer_class = PublicProfileSerializer

    def get_object(self):
        user_id = self.kwargs["pk"]
        user = get_user_model().objects.get(pk=user_id)
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile

from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.models import Profile
from accounts.permissions import IsOwnerProfile
from accounts.serializers import PublicProfileSerializer, FullProfileSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = FullProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfile]

    def get_object(self):
        return self.request.user.profile


class PublicProfileView(generics.RetrieveAPIView):
    serializer_class = PublicProfileSerializer

    def get_object(self):
        user_id = self.kwargs["pk"]
        user = get_user_model().objects.get(pk=user_id)
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile

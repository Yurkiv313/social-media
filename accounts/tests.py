from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.models import User


class ProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="me@example.com", password="testpass",
            first_name="Me", last_name="Now"
        )
        self.client.force_authenticate(user=self.user)
        self.profile_url = reverse("accounts:profile")

    def test_retrieve_own_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_own_profile(self):
        response = self.client.patch(self.profile_url, {
            "first_name": "Updated",
            "last_name": "Name",
            "bio": "Updated bio"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")
        self.assertEqual(response.data["bio"], "Updated bio")

    def test_update_profile_location_and_image(self):
        response = self.client.patch(self.profile_url, {
            "location": "Lviv",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["location"], "Lviv")

    def test_retrieve_public_profile(self):
        other = User.objects.create_user(email="other@example.com", password="123456", first_name="Other", last_name="User")
        url = reverse("user:public_profile", kwargs={"pk": other.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "other@example.com")

    def test_cannot_patch_public_profile(self):
        other = User.objects.create_user(email="other@example.com", password="123456", first_name="O", last_name="X")
        url = reverse("user:public_profile", kwargs={"pk": other.pk})

        response = self.client.patch(url, {"bio": "hacked!"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthenticated_user_cannot_access_profile(self):
        self.client.logout()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_update_profile(self):
        self.client.logout()
        response = self.client.patch(self.profile_url, {"first_name": "Hacked"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

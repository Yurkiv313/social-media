from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.models import User


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("user:create")
        self.login_url = reverse("user:token_obtain_pair")

    def test_user_can_register(self):
        data = {
            "email": "newuser@example.com",
            "password": "strongpass123",
            "first_name": "New",
            "last_name": "User"
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_registration_requires_password(self):
        data = {
            "email": "no_pass@example.com",
            "first_name": "No",
            "last_name": "Pass"
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_rejects_weak_password(self):
        data = {
            "email": "weak@example.com",
            "password": "123",
            "first_name": "Weak",
            "last_name": "Pass"
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_user_can_login(self):
        User.objects.create_user(
            email="test@example.com", password="testpass",
            first_name="Test", last_name="User"
        )

        response = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "testpass"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_wrong_password(self):
        User.objects.create_user(
            email="wrongpass@example.com", password="correctpass",
            first_name="Wrong", last_name="Pass"
        )

        response = self.client.post(self.login_url, {
            "email": "wrongpass@example.com",
            "password": "incorrect"
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_logout(self):
        user = User.objects.create_user(
            email="logout@example.com", password="pass123",
            first_name="Out", last_name="User"
        )

        login_response = self.client.post(self.login_url, {
            "email": "logout@example.com",
            "password": "pass123"
        })
        refresh = login_response.data["refresh"]

        self.client.force_authenticate(user=user)
        response = self.client.post(reverse("user:logout"), {"refresh": refresh})

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_user_search(self):
        User.objects.create_user(email="alice@example.com", password="12345", first_name="Alice", last_name="A")
        User.objects.create_user(email="bob@example.com", password="12345", first_name="Bob", last_name="B")
        searcher = User.objects.create_user(email="search@example.com", password="12345")

        self.client.force_authenticate(user=searcher)
        response = self.client.get(reverse("user:user_list"), {"search": "alice"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("alice" in user["email"] for user in response.data))

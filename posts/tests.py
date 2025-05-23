from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from posts.models import Post
from user.models import User


class PostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="poster@example.com",
            password="testpass",
            first_name="Poster",
            last_name="User"
        )
        self.client.force_authenticate(user=self.user)
        self.post_url = reverse("posts:post-list")

    def test_create_post(self):
        data = {
            "content": "This is a test post",
            "hashtags": "#test"
        }
        response = self.client.post(self.post_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().content, "This is a test post")

    def test_create_post_without_content(self):
        response = self.client.post(self.post_url, {"content": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.data)

    def test_list_own_posts(self):
        Post.objects.create(author=self.user, content="Visible post")
        response = self.client.get(self.post_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Visible post" in p["content"] for p in response.data))

    def test_followed_users_posts_are_visible(self):
        other_user = User.objects.create_user(email="followed@example.com", password="test123")
        Post.objects.create(author=other_user, content="Post from followed")

        self.user.following_set.create(following=other_user)

        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Post from followed" in p["content"] for p in response.data))

    def test_unauthenticated_user_cannot_create_post(self):
        self.client.logout()
        response = self.client.post(self.post_url, {"content": "Not allowed"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_can_update_own_post(self):
        post = Post.objects.create(author=self.user, content="Initial")
        url = reverse("posts:post-detail", kwargs={"pk": post.id})

        response = self.client.patch(url, {"content": "Updated content"})
        post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.content, "Updated content")

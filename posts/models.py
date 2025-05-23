from django.contrib.auth import get_user_model
from django.db import models

from posts.helpers import post_image_path

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, upload_to=post_image_path)
    hashtags = models.TextField(blank=True, null=True)

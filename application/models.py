from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=30)
    text = models.CharField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


class Comment(models.Model):
    text = models.CharField(max_length=200, default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)


from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=30)
    text = models.CharField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    liked_users = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    disliked_users = models.ManyToManyField(User, related_name='disliked_posts', blank=True)


class Comment(models.Model):
    text = models.CharField(max_length=200, default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

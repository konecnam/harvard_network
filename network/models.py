from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False)

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(auto_now=True)
    information = models.CharField(max_length=1024)  
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(User)


# class Like(models.Model):
#     id = models.IntegerField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
#     date = models.DateTimeField(auto_now=True)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
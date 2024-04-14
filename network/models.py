from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(auto_now=True)
    information = models.CharField(max_length=1024)  
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

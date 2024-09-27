from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    message = models.TextField()

    def __str__(self):
        return self.title

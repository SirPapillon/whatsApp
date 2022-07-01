from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class usersContent(models.Model):
    username = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=250)
    user_id = models.IntegerField()
    image_url = models.CharField(max_length=250)
    messages = models.TextField()
    class Meta:
        ordering=("username",)
    def __str__(self):
        return self.username
import os

from django.db import models
from django.contrib.auth.models import User

class UserExtraInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')

    user_picture = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username

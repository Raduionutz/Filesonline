from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    filename = models.CharField(max_length=256)
    upload_time = models.DateTimeField(default=timezone.now)
    shared = models.BooleanField(default=False)
    encrypted = models.BooleanField(default=False)
    is_directory = models.BooleanField(default=False)
    path = models.CharField(max_length=265, default='/')

    def __str__(self):
        return self.filename

class SharedFileWith(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='instances')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_with')

    def __str__(self):
        return self.file.filename

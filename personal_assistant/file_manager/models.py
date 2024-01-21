from django.db import models
from django.contrib.auth.models import User
import os


def get_upload_path(instance, filename):
    folder = instance.folder
    if folder:
        return os.path.join(folder, filename)
    else:
        return filename


class UploadedFile(models.Model):
    FILE_CATEGORIES = [
        ('VIDEO', 'Video'),
        ('MUSIC', 'Music'),
        ('IMAGE', 'Image'),
        ('OTHER', 'Other'),
    ]
    folder = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to=get_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=5, choices=FILE_CATEGORIES, default='OTHER')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

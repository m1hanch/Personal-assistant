from django.db import models
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

    # ніби повинно так бути, але пише, що не може додати non-nullable field до uploadedfile, мабуть потрібно почистити aws
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return self.name

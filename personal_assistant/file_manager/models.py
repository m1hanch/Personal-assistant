from django.db import models
import os


def get_upload_path(instance, filename):
    folder = instance.folder
    if folder:
        return os.path.join(folder, filename)
    else:
        return filename


class UploadedFile(models.Model):
    folder = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to=get_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

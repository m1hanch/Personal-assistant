from django.contrib.auth.models import User
from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=150, null=True)
    birthday = models.DateField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

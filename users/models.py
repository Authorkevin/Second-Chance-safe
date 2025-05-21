from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any custom fields here
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=75, blank=False)

    def __str__(self):
        return self.username

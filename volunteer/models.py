from django.db import models
from django.conf import settings

class Volunteer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)  # Basic validation can be added in forms
    address = models.TextField()
    capacity_to_volunteer = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Submitted on {self.submission_date.strftime('%Y-%m-%d %H:%M')}"

# Create your models here.

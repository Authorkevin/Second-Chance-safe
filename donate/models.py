from django.db import models
from django.conf import settings
import decimal

class Donation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    first_name = models.CharField(max_length=100, help_text="Donor's first name")
    last_name = models.CharField(max_length=100, help_text="Donor's last name")
    email = models.EmailField(help_text="Donor's email address for receipt (optional)", blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Donation amount")
    timestamp = models.DateTimeField(auto_now_add=True)
    stripe_checkout_id = models.CharField(max_length=255, blank=True, null=True, help_text="Stripe Checkout Session ID")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # Optional: Link to a user if the donor is logged in
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"Donation by {self.first_name} {self.last_name} for ${self.amount} ({self.status})"

    class Meta:
        ordering = ['-timestamp']



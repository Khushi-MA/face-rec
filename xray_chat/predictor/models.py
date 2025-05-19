from django.db import models
from django.contrib.auth.models import AbstractUser

class NewUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    )
    user_type = models.CharField(max_length=300, choices=USER_TYPE_CHOICES, default='admin')
    current_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

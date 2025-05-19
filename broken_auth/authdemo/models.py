from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Stored in plain text (vulnerable)
    session_id = models.CharField(max_length=100, blank=True, null=True)  # Weak session tracking

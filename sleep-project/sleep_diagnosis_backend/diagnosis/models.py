from django.db import models
from django.contrib.auth.models import User
from datetime import time

class SleepDiagnosis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sleep_duration = models.FloatField()
    sleep_quality = models.IntegerField()
    snoring = models.BooleanField(default=False)
    insomnia = models.BooleanField(default=False)
    daytime_fatigue = models.BooleanField(default=False)
    sleep_time = models.TimeField(default=time(22, 0))  # Set default to 10:00 PM
    wake_up_time = models.TimeField(default=time(6, 0))  # Set default to 6:00 AM
    diagnosis_result = models.CharField(max_length=100, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

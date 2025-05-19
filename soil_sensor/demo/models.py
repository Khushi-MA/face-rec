from django.db import models
from django.utils.timezone import make_naive
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta
from django.db import models
import random
import string



class NewUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=15, unique=True)
    place = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email', 'full_name', 'contact_no', 'place']

    def __str__(self):
        return self.username


class Device(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='devices')
    device_name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True) 

    def days_remaining(self):
        if self.subscription_end_date:
            remaining_days = (self.subscription_end_date - now()).days
            return max(0, remaining_days)
        return 0

    def __str__(self):
        return f"{self.device_name} ({self.user.username})"
    

class Plot(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    device = models.OneToOneField(Device, on_delete=models.CASCADE)  
    plot_name = models.CharField(max_length=100)
    plot_number = models.IntegerField()  
    crop_name = models.CharField(max_length=100, null=True, blank=True) 

    def __str__(self):
        return f"{self.plot_name} - {self.device.device_name}"





class SensorData(models.Model):
    sensor_id = models.IntegerField()
    device_name = models.CharField(max_length=300,default='MyDevice')
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField(default=0)
    moisture = models.FloatField()
    conductivity = models.FloatField()
    pH = models.FloatField()  
    led_status = models.CharField(max_length=100, default="OFF")
    overall_moisture = models.FloatField()
    status = models.CharField(max_length = 100, default='offline')
    last_seen = models.DateTimeField(default=timezone.now)  # Add this field


    def get_localized_timestamp(self):
        timestamp = self.timestamp
        if timestamp and timestamp.tzinfo:
            timestamp = make_naive(timestamp)
        return timestamp

    def __str__(self):
        return f"{self.device_name} - {self.temperature}"
    


class Crop(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=150, blank=True, null=True)
    crop_type = models.CharField(
        max_length=100, 
        choices=[('Cereal', 'Cereal'), ('Pulse', 'Pulse'), ('Vegetable', 'Vegetable'), ('Fruit', 'Fruit')]
    )
    
    general_information = models.TextField()
    growth_duration = models.CharField(max_length=50)

    temperature = models.CharField(max_length=100)
    rainfall = models.CharField(max_length=100)
    sowing_temperature = models.CharField(max_length=100)
    harvesting_temperature = models.CharField(max_length=100)

    season = models.CharField(max_length=50)
    soil = models.TextField()
    land_preparation = models.TextField()
    
    # Changed to TextField to avoid data length issues
    seed_rate = models.TextField()
    seed_treatment = models.TextField()
    insecticide_name = models.TextField()
    quantity = models.TextField()
    time_of_sowing = models.TextField()
    spacing = models.TextField()
    method_of_sowing = models.TextField()
    sowing_depth = models.TextField()
    weed_control = models.TextField()
    irrigation = models.TextField()
    ph_level = models.TextField()
    harvesting_time = models.TextField()
    yield_per_hectare = models.TextField()
    post_harvest_handling = models.TextField()

    image = models.ImageField(upload_to='crop_images/', blank=True, null=True)

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name
    

class Disease(models.Model):
    crop = models.ForeignKey(Crop, related_name='diseases', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField()
    control_methods = models.TextField()
    image = models.ImageField(upload_to='disease_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.crop.name})"
    
class Pest(models.Model):
    crop = models.ForeignKey(Crop, related_name='pests', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField()
    control_methods = models.TextField()
    image = models.ImageField(upload_to='pest_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.crop.name})"

class FertilizerRequirement(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='fertilizer_requirements')
    name = models.CharField(max_length=100)  # e.g., Urea, Nitrogen, Phosphorus, Potash, etc.
    value = models.CharField(max_length=100)  # e.g., 110 kg/acre, 50 kg/acre, etc.

    def __str__(self):
        return f"{self.name} - {self.value} for {self.crop.name}"


class LEDControl(models.Model):
    user = models.ForeignKey('NewUser', on_delete=models.CASCADE, related_name='led_controls')  # Link to user
    device = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='led_controls')  # Link to device
    relay_status = models.CharField(max_length=10)  # "ON" or "OFF" (your status)
    timer_duration = models.IntegerField(default=0)  # Duration in seconds
    start_time = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    end_time = models.DateTimeField(blank=True, null=True)  # Calculated based on timer_duration

    def save(self, *args, **kwargs):
        if not self.start_time:
            self.start_time = timezone.now()

        if self.timer_duration > 0 and self.relay_status == "ON":
            self.end_time = self.start_time + timezone.timedelta(seconds=self.timer_duration)
        else:
            self.end_time = None  

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.device.device_name} ({self.user.username}) - Relay: {self.relay_status} (Timer: {self.timer_duration}s)"
    
    
class Contact(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()


class PasswordResetOTP(models.Model):
    user = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    @classmethod
    def generate_otp(cls):
        return ''.join(random.choices(string.digits, k=6))

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    def mark_as_used(self):
        self.is_used = True
        self.save()

    class Meta:
        verbose_name = 'Password Reset OTP'
        verbose_name_plural = 'Password Reset OTPs'


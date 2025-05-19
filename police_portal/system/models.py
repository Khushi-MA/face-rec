from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = [
        ('User', 'User'),
        ('Admin', 'Admin'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='User')  # default USER
    created_at = models.DateTimeField(auto_now_add=True)  # auto timestamp on create

    def __str__(self):
        return f"{self.username} ({self.role})"

from django.contrib.auth import get_user_model

User = get_user_model()  # This ensures it uses your custom User model

class Incident(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    incident_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_incidents')  # Creator of the incident
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    location = models.CharField(max_length=255, null=True, blank=True)
    date_occurred = models.DateField(null=True, blank=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    assessors = models.ManyToManyField(User, related_name='assessing_incidents', blank=True)  # Users assessing the incident

    def __str__(self):
        return f"{self.title} ({self.status})"

class Evidence(models.Model):
    evidence_id = models.AutoField(primary_key=True)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='evidences')
    file = models.FileField(upload_to='evidence/')  # Store files in media/evidence/
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_evidences')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evidence {self.evidence_id} for Incident {self.incident.incident_id}"

from django.db import models
from .models import Incident  # Ensure this is correctly importing your Incident model

class Suspect(models.Model):
    suspect_id = models.AutoField(primary_key=True)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='suspects')  # Link to related incident
    name = models.CharField(max_length=255, null=True, blank=True)  # Allow aliases or unknown names
    email = models.EmailField(null=True, blank=True)  # Optional, if known
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # Accepts IPv4 and IPv6
    risk_score = models.FloatField(default=0.0)  # To be assigned via ML or heuristics
    notes = models.TextField(null=True, blank=True)  # Analyst notes or behavioral patterns

    def __str__(self):
        return f"Suspect {self.name or self.suspect_id} for Incident {self.incident.incident_id}"

class JoinRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='join_requests')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_join_requests')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_join_requests')  # Admin to approve/decline
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined')], default='Pending')
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"JoinRequest by {self.requested_by.username} for Incident {self.incident.title}"

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='messages')  # Link to the related incident
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()  # Message content
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in Incident {self.incident.title} at {self.timestamp}"

class Threat(models.Model):
    THREAT_LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    threat_id = models.AutoField(primary_key=True)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='threats')
    threat_type = models.CharField(max_length=100)  # e.g., Malware, Phishing
    confidence_score = models.FloatField()  # e.g., 0.87
    threat_level = models.CharField(max_length=20, choices=THREAT_LEVEL_CHOICES)
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.threat_type} Threat (ID: {self.threat_id})"

class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('Summary', 'Summary'),
        ('Final', 'Final'),
        ('Threat Brief', 'Threat Brief'),
    ]

    report_id = models.AutoField(primary_key=True)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='reports')  # Link to incident
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='generated_reports')  # Creator
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    file_path = models.FileField(upload_to='reports/')  # e.g., media/reports/report_123.pdf
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return f"{self.report_type} Report for Incident {self.incident.incident_id}"

    class Meta:
        ordering = ['-created_at']
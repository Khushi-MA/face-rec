# Generated by Django 5.1.6 on 2025-04-22 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_patientscan_prediction_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientreport',
            name='doctor_approved',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]

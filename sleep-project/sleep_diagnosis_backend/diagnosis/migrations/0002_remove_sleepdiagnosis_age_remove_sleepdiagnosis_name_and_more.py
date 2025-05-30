# Generated by Django 5.1.6 on 2025-04-22 08:23

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sleepdiagnosis',
            name='age',
        ),
        migrations.RemoveField(
            model_name='sleepdiagnosis',
            name='name',
        ),
        migrations.RemoveField(
            model_name='sleepdiagnosis',
            name='symptoms',
        ),
        migrations.AddField(
            model_name='sleepdiagnosis',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sleepdiagnosis',
            name='daytime_fatigue',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sleepdiagnosis',
            name='insomnia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sleepdiagnosis',
            name='sleep_duration',
            field=models.FloatField(default=7.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sleepdiagnosis',
            name='sleep_quality',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sleepdiagnosis',
            name='sleep_time',
            field=models.TimeField(default=datetime.time(22, 0)),
        ),
        migrations.AddField(
            model_name='sleepdiagnosis',
            name='snoring',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sleepdiagnosis',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sleepdiagnosis',
            name='wake_up_time',
            field=models.TimeField(default=datetime.time(6, 0)),
        ),
        migrations.AlterField(
            model_name='sleepdiagnosis',
            name='diagnosis_result',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

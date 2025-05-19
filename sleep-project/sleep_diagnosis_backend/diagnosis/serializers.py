from rest_framework import serializers
from .models import SleepDiagnosis

class SleepDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleepDiagnosis
        fields = ['id', 'user', 'sleep_duration', 'sleep_quality', 'snoring', 'insomnia', 
                  'daytime_fatigue', 'sleep_time', 'wake_up_time', 'diagnosis_result', 'date']

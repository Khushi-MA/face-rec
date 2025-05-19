# serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import LEDControl, SensorData

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = [
            'id', 'sensor_id','device_name', 'temperature', 'moisture', 'conductivity','pH', 'overall_moisture','status'
        ]
        extra_kwargs = {
            'timestamp': {'required': True, 'format': '%Y-%m-%dT%H:%M:%S%z'},  
            }

    def to_internal_value(self, data): 
        internal_value = super().to_internal_value(data)
        timestamp = data.get('timestamp')
        if timestamp:
            try:
                timestamp = timezone.parse_datetime(timestamp)
                if timezone.is_naive(timestamp):
                    timestamp = timezone.make_aware(timestamp, timezone.get_current_timezone())
                internal_value['timestamp'] = timestamp
            except ValueError:
                raise serializers.ValidationError({'timestamp': 'Invalid datetime format'})
        return internal_value

class LEDControlSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.device_name', read_only=True)

    class Meta:
        model = LEDControl
        fields = [
            'id', 'user', 'device', 'device_name', 'relay_status', 'timer_duration', 'start_time', 'end_time'
        ]
        read_only_fields = ['user', 'start_time', 'end_time', 'device_name']
        
    def validate_relay_status(self, value):
        valid_values = ["ON", "OFF"]
        if value not in valid_values:
            raise serializers.ValidationError(f"relay_status must be one of {valid_values}.")
        return value

    def validate_timer_duration(self, value):
        if not isinstance(value, int) or value < 0:
            raise serializers.ValidationError("timer_duration must be a non-negative integer.")
        return value

    def validate(self, data):
        if 'device' not in data and not self.instance:  # Check on create
            raise serializers.ValidationError({"device": "This field is required."})
        return data



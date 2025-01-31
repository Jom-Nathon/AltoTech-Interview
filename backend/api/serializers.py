from rest_framework import serializers
from .models import Hotel, Room, Sensor, NewestData, RawData

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class NewestDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewestData
        fields = '__all__'

class RawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawData
        fields = '__all__'



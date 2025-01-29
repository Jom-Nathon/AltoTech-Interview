
from rest_framework import serializers
from .models import Hotel, Floor, Room


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['hotel_id', 'name']


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['floor_id', 'hotel_id']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_id', 'floor_id', 'hotel_id']
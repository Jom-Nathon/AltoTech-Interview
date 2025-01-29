from django.db import models

# Create your models here.

class Hotel(models.Model):
    hotel_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

class Floor(models.Model):
    floor_id = models.IntegerField(primary_key=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)

class Room(models.Model):
    room_id = models.IntegerField(primary_key=True)
    floor_id = models.ForeignKey(Floor, on_delete=models.CASCADE)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    
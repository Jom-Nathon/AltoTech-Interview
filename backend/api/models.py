from django.db import models

class Hotel(models.Model):
    hotel_id = models.CharField(primary_key=True, max_length=50)
    hotel_name = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'hotel'
        app_label = 'postgres'

    def __str__(self):
        return self.hotel_name
    
        
class Room(models.Model):
    room_id = models.CharField(max_length=50, primary_key=True)
    floor_id = models.CharField(max_length=50)
    hotel = models.ForeignKey(
        Hotel, 
        db_column='hotel_id',
        to_field='hotel_id',
        on_delete=models.CASCADE
    )
    class Meta:
        managed = False
        db_table = 'room'
        app_label = 'postgres'
        unique_together = (('room_id', 'floor_id'),)

    def __str__(self):
        return self.room_id
    
    
class Sensor(models.Model):
    device_id = models.CharField(max_length=50, primary_key=True)
    room = models.ForeignKey(
        Room, 
        db_column='room_id',
        to_field='room_id',
        on_delete=models.CASCADE
    )
    device_type = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'sensor'
        app_label = 'postgres'

    def __str__(self):
        return self.device_id
    

class NewestData(models.Model):
    timestamp = models.IntegerField()
    date_time = models.DateTimeField()
    device_id = models.CharField(max_length=50, primary_key=True)
    datapoint = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    
    class Meta:
        managed = False
        db_table = 'newest_data'
        app_label = 'supabase'
        unique_together = (('device_id', 'datapoint'),)

    def __str__(self):
        return f"{self.device_id} - {self.datapoint}"
    

class RawData(models.Model):
    id = models.IntegerField(primary_key=True)
    timestamp = models.IntegerField()
    date_time = models.DateTimeField()
    device_id = models.CharField(max_length=50)
    datapoint = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'raw_data'
        app_label = 'timescaledb'

    def __str__(self):
        return self.device_id


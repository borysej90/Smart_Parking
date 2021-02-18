from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class VideoProcessorType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)


class ParkingSite(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100)
    lots_number = models.IntegerField()
    cameras_number = models.IntegerField()
    is_free = models.BooleanField()


class VideoProcessor(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(VideoProcessorType, on_delete=models.CASCADE)
    parking_site = models.ForeignKey(ParkingSite, on_delete=models.CASCADE)
    stream_url = models.CharField(max_length=100)


class ParkingLot(models.Model):
    id = models.AutoField(primary_key=True)
    coordinates = ArrayField(models.IntegerField())
    parking_site = models.ForeignKey(ParkingSite, on_delete=models.CASCADE)
    is_occupied = models.BooleanField()
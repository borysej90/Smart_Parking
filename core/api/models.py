from django.contrib.postgres.fields import ArrayField
from django.db import models


class VideoProcessorType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)


class ParkingSite(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    lots_number = models.IntegerField(blank=True)
    cameras_number = models.IntegerField(blank=True)
    is_free = models.BooleanField()
    latitude = models.FloatField()
    longitude = models.FloatField()


class VideoProcessor(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(VideoProcessorType, on_delete=models.CASCADE)
    parking_site = models.ForeignKey(ParkingSite, on_delete=models.CASCADE)
    stream_url = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)


class ParkingLot(models.Model):
    id = models.AutoField(primary_key=True)
    position_on_board = ArrayField(models.IntegerField())
    shape_on_board = ArrayField(models.IntegerField())
    coordinates = ArrayField(models.IntegerField())
    parking_site = models.ForeignKey(ParkingSite, on_delete=models.CASCADE, related_name='lots')
    video_processor = models.ForeignKey(VideoProcessor, on_delete=models.CASCADE, related_name='lots')
    is_occupied = models.BooleanField()
    is_for_disabled = models.BooleanField()

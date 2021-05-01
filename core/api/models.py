from django.core.validators import MaxValueValidator, MinValueValidator
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
    description = models.TextField(max_length=150)
    address = models.CharField(max_length=100)
    lots_number = models.IntegerField(blank=True)
    cameras_number = models.IntegerField(blank=True)
    is_free = models.BooleanField()
    latitude = models.FloatField(validators=[MinValueValidator(-90, "Limit error"),
                                             MaxValueValidator(90, "Limit error")])
    longitude = models.FloatField(validators=[MinValueValidator(-180, "Limit error"),
                                              MaxValueValidator(180, "Limit error")])


class Citizen(models.Model):
    number_plate = models.CharField(max_length=18)
    last_seen = models.DateField(blank=True, null=True)
    is_on_parking = models.BooleanField(blank=True, default=False)
    total_paid_time = models.IntegerField(blank=True, default=0)


class Acab(models.Model):
    head = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    price_per_hour = models.FloatField(validators=[
        MinValueValidator(0, "Minimal price error"),
    ])
    free_threshold = models.IntegerField()


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
    acab_id = models.ForeignKey(Acab, on_delete=models.CASCADE, blank=True, null=True)

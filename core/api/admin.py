# from django.contrib import admin
from django.contrib import admin
from .models import VideoProcessor, VideoProcessorType, ParkingSite, ParkingLot

admin.site.register(VideoProcessor)
admin.site.register(ParkingSite)
admin.site.register(ParkingLot)
admin.site.register(VideoProcessorType)
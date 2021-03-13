from rest_framework import serializers

from .models import ParkingLot, ParkingSite, VideoProcessor


class ParkingLotSerializer(serializers.ModelSerializer):
    parking_site_id = serializers.PrimaryKeyRelatedField(source='parking_site', queryset=ParkingSite.objects.all())
    video_processor_id = serializers.PrimaryKeyRelatedField(source='video_processor', queryset=VideoProcessor.objects.all())

    class Meta:
        model = ParkingLot
        fields = ['id', 'coordinates', 'is_occupied', 'parking_site_id', 'video_processor_id', 'is_for_disabled']

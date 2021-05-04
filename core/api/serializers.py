from rest_framework import serializers

from .models import ParkingLot, ParkingSite, VideoProcessor


class ParkingLotSerializer(serializers.ModelSerializer):
    parking_site_id = serializers.PrimaryKeyRelatedField(
        source='parking_site',
        queryset=ParkingSite.objects.all(),
    )
    video_processor_id = serializers.PrimaryKeyRelatedField(
        source='video_processor',
        queryset=VideoProcessor.objects.all(),
    )

    class Meta:
        model = ParkingLot
        fields = [
            'id',
            'position_on_board',
            'shape_on_board',
            'coordinates',
            'is_occupied',
            'parking_site_id',
            'video_processor_id',
            'is_for_disabled',
        ]


class ParkingSiteSerializer(serializers.ModelSerializer):
    lots_number = serializers.IntegerField(read_only=True)
    cameras_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = ParkingSite
        fields = '__all__'

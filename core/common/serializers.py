from rest_framework import serializers

from .models import ParkingLot, ParkingSite


class ParkingLotSerializer(serializers.ModelSerializer):
    parking_site_id = serializers.PrimaryKeyRelatedField(source='parking_site', queryset=ParkingSite.objects.all())

    class Meta:
        model = ParkingLot
        fields = ['id', 'coordinates', 'is_occupied', 'parking_site_id']

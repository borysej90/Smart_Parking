from rest_framework import serializers
from .models import ParkingLot


class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = '__all__'

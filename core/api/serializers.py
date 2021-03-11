from rest_framework import serializers

from .models import ParkingLot, ParkingSite


class PointSerializer(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()


class ParkingLotSerializer(serializers.ModelSerializer):
    parking_site_id = serializers.PrimaryKeyRelatedField(source='parking_site', queryset=ParkingSite.objects.all())
    coordinates = PointSerializer(many=True)

    def create(self, validated_data):
        parking_lot = ParkingLot.objects.create(**validated_data)
        return parking_lot

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)

        if validated_data.get('coordinates'):
            coordinates = []
            for points in validated_data['coordinates']:
                coordinates.extend(list(points.values()))

            validated_data['coordinates'] = coordinates

        return validated_data

    def to_representation(self, instance):
        coordinates = []
        for x, y in zip(instance.coordinates[0::2], instance.coordinates[1::2]):
            coordinates.append({'x': x, 'y': y})

        instance.coordinates = coordinates

        validated_data = super().to_representation(instance)

        return validated_data

    class Meta:
        model = ParkingLot
        fields = ['id', 'coordinates', 'is_occupied', 'parking_site_id', 'is_for_disabled']

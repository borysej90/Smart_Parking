from django.shortcuts import get_object_or_404

from ..models import VideoProcessor
from ..serializers import ParkingLotSerializer


def get_parking_map_by_processor_id(processor_id):
    """
    Gets map of all Parking lots related to specific Video processor
    by passed Video processor ID.

    Args:
        processor_id (int): Video processor ID by which to get Parking lots map.

    Returns:
        List of objects which contains ID of the Parking site and its coordinates.
    """
    processor = get_object_or_404(VideoProcessor, pk=processor_id)
    lots = processor.parking_site.lots.all()

    serializer = ParkingLotSerializer(lots, many=True)
    parking_lots_map = []
    for lot in serializer.data:
        obj = {
            'id': lot.get('id'),
            'coordinates': lot.get('coordinates')
        }
        parking_lots_map.append(obj)

    return parking_lots_map

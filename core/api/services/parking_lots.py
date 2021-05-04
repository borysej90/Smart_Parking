from ..models import ParkingLot


def get_parking_map_by_processor_id(processor_id):
    """
    Gets map of all Parking lots related to specific Video processor
    by passed Video processor ID.

    Args:
        processor_id (int): Video processor ID by which to get Parking lots map.

    Returns:
        List of objects which contains ID of the Parking site and its coordinates.
    """
    lots = ParkingLot.objects.filter(video_processor_id=processor_id).only('id', 'coordinates')
    parking_lots_map = []
    for lot in lots:
        obj = {
            'id': lot.id,
            'coordinates': lot.coordinates,
        }
        parking_lots_map.append(obj)
    return parking_lots_map

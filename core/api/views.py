import json

from django.db.models import Count
from django.http.response import HttpResponseServerError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from events.publisher import Publisher
from .models import ParkingLot, ParkingSite, VideoProcessor
from .serializers import ParkingLotSerializer, ParkingSiteSerializer
from .services.parking_lots import get_parking_map_by_processor_id
from .services.video_processors import get_rtsp_url_by_processor_id


class ParkingSiteViewSet(viewsets.ModelViewSet):
    serializer_class = ParkingSiteSerializer
    queryset = ParkingSite.objects.annotate(lots_number=Count('lots'), cameras_number=Count('processors'))
    lookup_field = 'id'


class ParkingLotViewSet(viewsets.ModelViewSet):
    serializer_class = ParkingLotSerializer

    def get_queryset(self):
        queryset = ParkingLot.objects.filter(parking_site_id=self.kwargs['site_id'])
        return queryset


@api_view(['GET'])
def get_parking_lots_map(request, processor_id):
    parking_lots_map = get_parking_map_by_processor_id(processor_id)
    if len(parking_lots_map) < 1:
        return Response(
            {'message': 'no such video processor or parking map is empty'},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(parking_lots_map)


@api_view(['GET'])
def get_camera_stream_url(request, processor_id):
    url = get_rtsp_url_by_processor_id(processor_id)
    if url == '':
        return HttpResponseServerError()

    return Response({'url': url})


@api_view(['POST'])
def update_processors_parking_lots(request, processor_id):
    lots = []
    try:
        for obj in json.loads(request.data):
            lot = get_object_or_404(ParkingLot, pk=obj['id'])
            lot.is_occupied = obj['is_occupied']
            lot.save()
            lots.append(lot)
    except KeyError as err:
        return Response({err.args[0]: 'missing value'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ParkingLotSerializer(lots, many=True)

    video_processor = VideoProcessor.objects.select_related('parking_site').values('parking_site__address').get(id=processor_id)
    address = video_processor.parking_site.address

    pub = Publisher()
    pub.send_parking_lots(address, serializer.data)

    return Response(serializer.data)

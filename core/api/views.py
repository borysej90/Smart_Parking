from django.http.response import HttpResponseServerError
from django.shortcuts import get_object_or_404
import json
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ParkingLot, ParkingSite, VideoProcessor
from .serializers import ParkingLotSerializer, ParkingSiteSerializer
from .services.parking_lots import get_parking_map_by_processor_id
from .services.video_processors import get_rtsp_url_by_processor_id

from events.publisher import Publisher


class ParkingSiteViewSet(viewsets.ModelViewSet):
    serializer_class = ParkingSiteSerializer
    queryset = ParkingSite.objects.all()


class ParkingList(APIView):
    def get(self, request, site_id, format=None):
        _ = get_object_or_404(ParkingSite, pk=site_id)
        lots = ParkingLot.objects.filter(parking_site=site_id)
        serializer = ParkingLotSerializer(lots, many=True)
        return Response(serializer.data)

    def post(self, request, site_id, format=None):
        serializer = ParkingLotSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParkingDetail(APIView):
    def get(self, request, site_id, pk, format=None):
        lot = get_object_or_404(ParkingLot, pk=pk)

        if lot.parking_site.id != site_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ParkingLotSerializer(lot)
        return Response(serializer.data)

    def put(self, request, site_id, pk, format=None):
        lot = get_object_or_404(ParkingLot, pk=pk)

        if lot.parking_site.id != site_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ParkingLotSerializer(lot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, site_id, pk, format=None):
        lot = get_object_or_404(ParkingLot, pk=pk)

        if lot.parking_site.id != site_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ParkingLotSerializer(lot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, site_id, pk, format=None):
        lot = get_object_or_404(ParkingLot, pk=pk)

        if lot.parking_site.id != site_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        lot.delete()
        return Response("Parking lot has been deleted!")


@api_view(['GET'])
def get_parking_lots_map(request, processor_id):
    parking_lots_map = get_parking_map_by_processor_id(processor_id)

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

    video_processor = VideoProcessor.objects.get(id=processor_id)
    site = ParkingSite.objects.get(id=video_processor.parking_site.id)
    address = site.address

    pub = Publisher()
    pub.send_parking_lots(address, serializer.data)

    return Response(serializer.data)

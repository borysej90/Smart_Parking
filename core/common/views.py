from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ParkingLot
from .serializers import ParkingLotSerializer


class ParkingList(APIView):

    def get(self, request, site_id, format=None):
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
            return Response(status=status.HTTP_404_NOT_FOUND)

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

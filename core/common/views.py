from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import ParkingLotSerializer
from .models import ParkingLot


@api_view(['GET', 'POST'])
def process_parking_lots(request):
    if request.method == 'GET':
        lots = ParkingLot.objects.all()
        serializer = ParkingLotSerializer(lots, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ParkingLotSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def process_parking_lot(request, pk):
    try:
        lot = ParkingLot.objects.get(id=pk)
    except ParkingLot.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ParkingLotSerializer(lot)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ParkingLotSerializer(lot, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    if request.method == 'PATCH':
        serializer = ParkingLotSerializer(lot, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    if request.method == 'DELETE':
        lot.delete()

        return Response("Parking lot has been deleted!", status=status.HTTP_200_OK)

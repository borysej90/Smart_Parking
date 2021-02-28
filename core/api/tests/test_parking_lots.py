import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import ParkingLot, ParkingSite
from api.serializers import ParkingLotSerializer


class ParkingLotsTestCase(APITestCase):
    def test_get(self):
        site = ParkingSite.objects.create(address='parking-site-1', lots_number=10, cameras_number=1, is_free=True)
        lot1 = ParkingLot.objects.create(coordinates=[1, 1], parking_site=site, is_occupied=False)
        lot2 = ParkingLot.objects.create(coordinates=[2, 2], parking_site=site, is_occupied=True)

        url = reverse('parking-lots', args=[site.id])
        response = self.client.get(url)

        serializer_data = ParkingLotSerializer([lot1, lot2], many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status code is not 200.')
        self.assertEqual(response.data, serializer_data, 'Expected objects are not equal to those created.')

    def test_post(self):
        site = ParkingSite.objects.create(address='parking-site-1', lots_number=10, cameras_number=1, is_free=True)

        lots = [
            {
                'coordinates': [1, 1],
                'is_occupied': 'false',
                'parking_site_id': site.id
            },
            {
                'coordinates': [2, 2],
                'is_occupied': 'true',
                'parking_site_id': site.id
            }
        ]

        url = reverse('parking-lots', args=[site.id])
        response = self.client.post(url, json.dumps(lots), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status code is not 200.')
        self.assertEqual(len(response.data), len(lots), "Got different quantity of requested items in response")

    def test_post_with_invalid_data(self):
        site = ParkingSite.objects.create(address='parking-site-1', lots_number=10, cameras_number=1, is_free=True)

        lots = [
            {
                'coordinates': 5,
                'is_occupied': 'false'
            },
            {
                'coordinates': [2, 2],
                'is_occupied': 'invalid boolean',
                'parking_site_id': 5
            }
        ]

        url = reverse('parking-lots', args=[site.id])
        response = self.client.post(url, json.dumps(lots), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Status code is not 400.')

    def test_detail_get(self):
        site = ParkingSite.objects.create(address='parking-site-1', lots_number=10, cameras_number=1, is_free=True)
        lot = ParkingLot.objects.create(coordinates=[1, 1], parking_site=site, is_occupied=False)

        url = reverse('parking-lot', args=[site.id, lot.id])
        response = self.client.get(url)

        serializer_data = ParkingLotSerializer(lot).data

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status code is not 200.')
        self.assertEqual(response.data, serializer_data, 'Expected object is not equal to the created one.')

    def test_detail_get_with_another_parking_site(self):
        site1 = ParkingSite.objects.create(address='parking-site-1', lots_number=10, cameras_number=1, is_free=True)
        site2 = ParkingSite.objects.create(address='parking-site-2', lots_number=20, cameras_number=2, is_free=False)
        lot = ParkingLot.objects.create(coordinates=[1, 1], parking_site=site1, is_occupied=False)

        url = reverse('parking-lot', args=[site2.id, lot.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         'Status code is not 404. Given lot was found on improper parking site.')

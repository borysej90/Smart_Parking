import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import ParkingLot, ParkingSite, VideoProcessor, VideoProcessorType
from ..serializers import ParkingLotSerializer


def init_video_processor(site: ParkingSite):
    processor_type = VideoProcessorType.objects.create(
        type_name='some_type',
        image_url='https://example.com/image/',
        tag="v1.0.0",
    )
    processor = VideoProcessor.objects.create(
        type=processor_type,
        parking_site=site,
        stream_url='rtsp://example.com/some_rtsp_stream/',
        is_active=True,
    )

    return processor_type, processor


class ParkingLotsTestCase(APITestCase):
    def test_get(self):
        site = ParkingSite.objects.create(
            name='parking-site-1',
            address='parking-site-1',
            lots_number=10,
            cameras_number=1,
            is_free=True,
            latitude=25.2,
            longitude=100.4,

        )
        _, proc = init_video_processor(site)
        lot1 = ParkingLot.objects.create(
            position_on_board=[1, 1],
            shape_on_board=[1, 1],
            coordinates=[1, 1],
            parking_site=site,
            video_processor=proc,
            is_occupied=False,
            is_for_disabled=False,
        )
        lot2 = ParkingLot.objects.create(
            position_on_board=[2, 2],
            shape_on_board=[2, 2],
            coordinates=[2, 2],
            parking_site=site,
            video_processor=proc,
            is_occupied=True,
            is_for_disabled=True,
        )

        url = reverse('parking-lots', args=[site.id])
        response = self.client.get(url)

        serializer_data = ParkingLotSerializer([lot1, lot2], many=True).data

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, 'Status code is not 200.'
        )
        self.assertEqual(
            response.data,
            serializer_data,
            'Expected objects are not equal to those created.',
        )

    def test_post(self):
        site = ParkingSite.objects.create(
            name='parking-site-1', address='parking-site-1', lots_number=10, cameras_number=1, is_free=True,
            latitude=25.2, longitude=100.4
        )
        _, proc = init_video_processor(site)

        lots = [
            {
                'position_on_board': [1, 1],
                'shape_on_board': [1, 1],
                'coordinates': [1, 1],
                'is_occupied': False,
                'parking_site_id': site.id,
                'video_processor_id': proc.id,
                'is_for_disabled': False,
            },
            {
                'position_on_board': [2, 2],
                'shape_on_board': [2, 2],
                'coordinates': [2, 2],
                'is_occupied': True,
                'parking_site_id': site.id,
                'video_processor_id': proc.id,
                'is_for_disabled': True,
            },
        ]

        url = reverse('parking-lots', args=[site.id])
        response = self.client.post(
            url, json.dumps(lots), content_type='application/json'
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, 'Status code is not 200.'
        )
        self.assertEqual(
            len(response.data),
            len(lots),
            "Got different quantity of requested items in response",
        )

    def test_post_with_invalid_data(self):
        site = ParkingSite.objects.create(
            name='parking-site-1', address='parking-site-1', lots_number=10, cameras_number=1, is_free=True,
            latitude=25.2, longitude=100.4
        )

        lots = [
            {'coordinates': 5, 'is_occupied': False},
            {
                'coordinates': [2, 2],
                'is_occupied': 'invalid boolean',
                'parking_site_id': 5,
            },
        ]

        url = reverse('parking-lots', args=[site.id])
        response = self.client.post(
            url, json.dumps(lots), content_type='application/json'
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, 'Status code is not 400.'
        )

    def test_detail_get(self):
        site = ParkingSite.objects.create(
            name='parking-site-1', address='parking-site-1', lots_number=10, cameras_number=1, is_free=True,
            latitude=25.2, longitude=100.4
        )
        _, proc = init_video_processor(site)
        lot = ParkingLot.objects.create(
            position_on_board=[1, 1],
            shape_on_board=[1, 1],
            coordinates=[1, 1],
            parking_site=site,
            video_processor=proc,
            is_occupied=False,
            is_for_disabled=False,
        )

        url = reverse('parking-lot', args=[site.id, lot.id])
        response = self.client.get(url)

        serializer_data = ParkingLotSerializer(lot).data

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, 'Status code is not 200.'
        )
        self.assertEqual(
            response.data,
            serializer_data,
            'Expected object is not equal to the created one.',
        )

    def test_detail_get_with_another_parking_site(self):
        site1 = ParkingSite.objects.create(
            name='parking-site-1',
            address='parking-site-1',
            lots_number=10,
            cameras_number=1,
            is_free=True,
            latitude=25.2,
            longitude=100.4,

        )
        site2 = ParkingSite.objects.create(
            name='parking-site-2',
            address='parking-site-2',
            lots_number=20,
            cameras_number=2,
            is_free=False,
            latitude = 76.2,
            longitude = 132.4,
        )
        _, proc1 = init_video_processor(site1)
        lot = ParkingLot.objects.create(
            position_on_board=[1, 1],
            shape_on_board=[1, 1],
            coordinates=[1, 1],
            parking_site=site1,
            video_processor=proc1,
            is_occupied=False,
            is_for_disabled=False,
        )

        url = reverse('parking-lot', args=[site2.id, lot.id])
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            'Status code is not 400. Given lot was found on improper parking site.',
        )

    def test_detail_put(self):
        site = ParkingSite.objects.create(
            name='parking-site',
            address='parking-site',
            lots_number=10,
            cameras_number=1,
            is_free=True,
            latitude=21.2,
            longitude=10.4,
        )
        _, proc = init_video_processor(site)
        lot = ParkingLot.objects.create(
            position_on_board=[1, 1],
            shape_on_board=[1, 1],
            coordinates=[1, 1],
            parking_site=site,
            video_processor=proc,
            is_occupied=False,
            is_for_disabled=False,
        )
        new_lot = {
            'position_on_board': [2, 2],
            'shape_on_board': [2, 2],
            'coordinates': [2, 2],
            'is_occupied': True,
            'parking_site_id': site.id,
            'video_processor_id': proc.id,
            'is_for_disabled': True,
        }

        url = reverse('parking-lot', args=[site.id, lot.id])
        response = self.client.put(url, new_lot)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, 'Status code is not 200.'
        )
        self.assertEqual(
            response.data['coordinates'],
            new_lot['coordinates'],
            'Updated "coordinates" field is not equal to the requested one.',
        )
        self.assertEqual(
            response.data['is_occupied'],
            new_lot['is_occupied'],
            'Updated "is_occupied" field is not equal to the requested ones.',
        )
        self.assertEqual(
            response.data['parking_site_id'],
            new_lot['parking_site_id'],
            'Updated "parking_site_id" field, is not equal to the requested ones.',
        )

    def test_detail_put_with_another_parking_site(self):
        site1 = ParkingSite.objects.create(
            name='parking-site-1',
            address='parking-site-1',
            lots_number=10,
            cameras_number=1,
            is_free=True,
            latitude=25.2,
            longitude=100.4,
        )
        site2 = ParkingSite.objects.create(
            name='parking-site-2',
            address='parking-site-2',
            lots_number=20,
            cameras_number=2,
            is_free=False,
            latitude=76.2,
            longitude=132.4,
        )
        _, proc1 = init_video_processor(site1)
        lot = ParkingLot.objects.create(
            position_on_board=[1, 1],
            shape_on_board=[1, 1],
            coordinates=[1, 1],
            parking_site=site1,
            video_processor=proc1,
            is_occupied=False,
            is_for_disabled=False,
        )
        new_lot = {
            'coordinates': [2, 2],
            'is_occupied': True,
            'parking_site_id': site1.id,
            'is_for_disabled': True,
        }

        url = reverse('parking-lot', args=[site2.id, lot.id])
        response = self.client.put(url, new_lot)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            'Status code is not 400. Given lot was found on improper parking site.',
        )

    def test_put_with_invalid_data(self):
        site = ParkingSite.objects.create(
            name='parking-site',
            address='parking-site',
            lots_number=10,
            cameras_number=1,
            is_free=True,
            latitude=21.2,
            longitude=10.4,
        )
        _, proc = init_video_processor(site)
        lot = ParkingLot.objects.create(
            position_on_board=[1, 1],
            shape_on_board=[1, 1],
            coordinates=[1, 1],
            parking_site=site,
            video_processor=proc,
            is_occupied=False,
            is_for_disabled=False,
        )
        new_lot = {
            'coordinates': 5,
            'is_occupied': 'invalid boolean',
            'parking_site_id': site.id,
            'is_for_disabled': 123,
        }

        url = reverse('parking-lot', args=[site.id, lot.id])
        response = self.client.put(url, new_lot)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, 'Status code is not 400.'
        )

    def test_detail_patch(self):
        site = ParkingSite.objects.create(
            name='parking-site',
            address='parking-site',
            lots_number=10,
            cameras_number=1,
            is_free=True,
            latitude=21.2,
            longitude=10.4,
        )
        _, proc = init_video_processor(site)
        lot = ParkingLot.objects.create(
            position_on_board=[1, 1],
            shape_on_board=[1, 1],
            coordinates=[1, 1],
            parking_site=site,
            video_processor=proc,
            is_occupied=False,
            is_for_disabled=False,
        )
        new_lot = {'coordinates': [2, 2]}

        url = reverse('parking-lot', args=[site.id, lot.id])
        response = self.client.patch(url, new_lot)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, 'Status code is not 200.'
        )
        self.assertEqual(
            response.data['coordinates'],
            new_lot['coordinates'],
            'Patched "coordinates" field is not equal to the requested one.',
        )

    def test_detail_patch_with_another_parking_site(self):
        site1 = ParkingSite.objects.create(
            name='parking-site-1',
            address='parking-site-1',
            lots_number=10,
            cameras_number=1,
            is_free=True,
            latitude=25.2,
            longitude=100.4,
        )
        site2 = ParkingSite.objects.create(
            name='parking-site-2',
            address='parking-site-2',
            lots_number=20,
            cameras_number=2,
            is_free=False,
            latitude=76.2,
            longitude=132.4,
        )
        _, proc1 = init_video_processor(site1)
        lot = ParkingLot.objects.create(
            position_on_board=[1, 1],
            shape_on_board=[1, 1],
            coordinates=[1, 1],
            parking_site=site1,
            video_processor=proc1,
            is_occupied=False,
            is_for_disabled=False,
        )
        new_lot = {'coordinates': [2, 2]}

        url = reverse('parking-lot', args=[site2.id, lot.id])
        response = self.client.patch(url, new_lot)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            'Status code is not 400. Given lot was found on improper parking site.',
        )

    def test_patch_with_invalid_data(self):
        site = ParkingSite.objects.create(
            name='parking-site',
            address='parking-site',
            lots_number=10,
            cameras_number=1,
            is_free=True,
            latitude=21.2,
            longitude=10.4,
        )
        _, proc = init_video_processor(site)
        lot = ParkingLot.objects.create(
            position_on_board=[1, 1],
            shape_on_board=[1, 1],
            coordinates=[1, 1],
            parking_site=site,
            video_processor=proc,
            is_occupied=False,
            is_for_disabled=True,
        )
        new_lot = {'coordinates': True, 'something': [1, 2, 3]}

        url = reverse('parking-lot', args=[site.id, lot.id])
        response = self.client.patch(url, new_lot)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, 'Status code is not 400.'
        )

    def test_detail_delete(self):
        site = ParkingSite.objects.create(
            name='parking-site',
            address='parking-site',
            lots_number=10,
            cameras_number=1,
            is_free=True,
            latitude=21.2,
            longitude=10.4,
        )
        _, proc = init_video_processor(site)
        lot = ParkingLot.objects.create(
            position_on_board=[1, 1],
            shape_on_board=[1, 1],
            coordinates=[1, 1],
            parking_site=site,
            video_processor=proc,
            is_occupied=False,
            is_for_disabled=False,
        )

        url = reverse('parking-lot', args=[site.id, lot.id])
        response = self.client.delete(url)
        deleted_lot = self.client.get(url)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, 'Status code is not 200.'
        )
        self.assertEqual(
            deleted_lot.status_code,
            status.HTTP_404_NOT_FOUND,
            'Parking lot wasn\'t deleted.',
        )

    def test_detail_delete_with_another_parking_site(self):
        site1 = ParkingSite.objects.create(
            name='parking-site-1',
            address='parking-site-1',
            lots_number=10,
            cameras_number=1,
            is_free=True,
            latitude=25.2,
            longitude=100.4,
        )
        site2 = ParkingSite.objects.create(
            name='parking-site-2',
            address='parking-site-2',
            lots_number=20,
            cameras_number=2,
            is_free=False,
            latitude=76.2,
            longitude=132.4,
        )
        _, proc1 = init_video_processor(site1)
        lot = ParkingLot.objects.create(
            position_on_board=[1, 1],
            shape_on_board=[1, 1],
            coordinates=[1, 1],
            parking_site=site1,
            video_processor=proc1,
            is_occupied=False,
            is_for_disabled=False,
        )

        url = reverse('parking-lot', args=[site2.id, lot.id])
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            'Status code is not 400. Given lot was found on improper parking site.',
        )

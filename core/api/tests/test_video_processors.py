from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from ..models import VideoProcessorType, VideoProcessor, ParkingSite, ParkingLot

INCORRECT_STATUS = 'Expected status code {} but got {}'


def init_models():
    site = ParkingSite.objects.create(
        address="Some street",
        lots_number=20,
        cameras_number=2,
        is_free=True,
    )
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

    return site, processor_type, processor


class GetParkingLotsMapTests(APITestCase):
    def test_empty_parking_lots(self):
        site, proc_type, proc = init_models()

        url = reverse('get-parking-lots-map', args=[proc.id])
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            INCORRECT_STATUS.format(status.HTTP_200_OK, response.status_code)
        )

        self.assertEqual(
            response.data,
            [],
            f'Expected empty list but got {response.data}'
        )

    def test_not_found(self):
        url = reverse('get-parking-lots-map', args=['1'])
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            INCORRECT_STATUS.format(status.HTTP_404_NOT_FOUND, response.status_code)
        )

    def test_valid_response(self):
        site, proc_type, proc = init_models()
        lot = ParkingLot.objects.create(
            coordinates=[1, 2, 3, 4],
            parking_site=site,
            video_processor=proc,
            is_occupied=True,
            is_for_disabled=False,
        )

        url = reverse('get-parking-lots-map', args=[proc.id])
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            INCORRECT_STATUS.format(status.HTTP_200_OK, response.status_code)
        )

        expected = [{'id': lot.id, 'coordinates': lot.coordinates}]
        self.assertEqual(
            response.data,
            expected,
            f'Expected response {expected} but got {response.data}'
        )


class GetRTSPTests(APITestCase):
    def test_not_found(self):
        url = reverse('get-camera-stream-url', args=['1'])
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            INCORRECT_STATUS.format(status.HTTP_404_NOT_FOUND, response.status_code)
        )

    def test_valid_rtsp(self):
        site, proc_type, proc = init_models()
        url = reverse('get-camera-stream-url', args=[proc.id])
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            INCORRECT_STATUS.format(status.HTTP_200_OK, response.status_code)
        )

        expected = {'url': proc.stream_url}
        self.assertEqual(
            response.data,
            expected,
            f'Expected response {expected} but got {response.data}'
        )

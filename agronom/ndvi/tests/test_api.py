from django.urls import reverse
from rest_framework import status
from datetime import date
from django.contrib.gis.geos import Point, MultiPoint

from core.tests.base_test_case import APITestCase
from fields.tests.helpers import setup_cadastral_info, setup_field
from ndvi.models import NDVI


class TestNDVIAPI(APITestCase):
    def setUp(self):
        super().setUp()

        self.cad = setup_cadastral_info(self.user)
        self.field = setup_field(self.cad)

        for i in range(3):
            NDVI.objects.create(
                field=self.field,
                product_id='00ae448d-6466-47a4-8237-56c0aa05cffb%s' % i,
                date=date(2019, 3, 1 + i),
                img='/tmp/some_img_%s.png' % i,
                mean='0.%s' % i,
                boundary=MultiPoint([Point(0, 0), Point(0, i), Point(i, 0), Point(i, i)])
            )

    def test_get_ndvi(self):
        response = self.api_client.get(reverse('api_ndvi'), {'field_id': self.field.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {'boundary': {'coordinates': [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], 'type': 'MultiPoint'},
             'date': '2019-03-01', 'img': 'http://testserver/media/tmp/some_img_0.png', 'mean': '0.00'},
            {'boundary': {'coordinates': [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]], 'type': 'MultiPoint'},
             'date': '2019-03-02', 'img': 'http://testserver/media/tmp/some_img_1.png', 'mean': '0.10'},
            {'boundary': {'coordinates': [[0.0, 0.0], [0.0, 2.0], [2.0, 0.0], [2.0, 2.0]], 'type': 'MultiPoint'},
             'date': '2019-03-03', 'img': 'http://testserver/media/tmp/some_img_2.png', 'mean': '0.20'}])

    def test_pagination(self):
        response = self.api_client.get(reverse('api_ndvi'), {'field_id': self.field.id, 'limit': 1, 'offset': 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'count': 3,
            'next': 'http://testserver/api/v0_1/ndvi/?field_id=%s&limit=1&offset=2' % self.field.id,
            'previous': 'http://testserver/api/v0_1/ndvi/?field_id=%s&limit=1' % self.field.id,
            'results': [
                {'boundary': {'coordinates': [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]], 'type': 'MultiPoint'},
                 'date': '2019-03-02', 'img': 'http://testserver/media/tmp/some_img_1.png', 'mean': '0.10'}]
        })

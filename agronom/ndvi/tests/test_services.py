import os
import responses
import tempfile
import numpy as np
from PIL import Image
from decimal import Decimal
from datetime import datetime, date
from freezegun import freeze_time
from django.test import override_settings
from django.contrib.gis.geos import Point, MultiPoint
from unittest import mock
from model_mommy import mommy

from core.tests.base_test_case import BaseTestCase
from ndvi.services import GetFieldProducts, LoadNDVI
from ndvi.models import NDVI


class TestGetFieldProducts(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.cad_info = mommy.make('cadastral.CadastralInfo')
        self.field1 = mommy.make(
            'fields.Field',
            cadastral=self.cad_info,
            polygon='POLYGON((39.09 47.78, 39.09 47.77, 39.10 47.77, 39.09 47.78))')
        self.field2 = mommy.make(
            'fields.Field',
            cadastral=self.cad_info,
            polygon='POLYGON((39.12 47.83, 39.12 47.82, 39.13 47.83, 39.12 47.83))')

    @responses.activate
    @freeze_time('2019-04-09')
    def test_two_fields_in_one_product(self):
        responses.add(
            method=responses.POST,
            url='https://scihub.copernicus.eu/dhus/search?format=json&rows=100&start=0',
            body=self.load_fixture('sentinel_query_api_response.json')
        )

        result = GetFieldProducts()(self.cad_info.field_set.order_by('id'), datetime.now())
        self.assertEqual(result, {
            '00ae448d-6466-47a4-8237-56c0aa05cffb': [self.field1.id, self.field2.id],
            '69b20381-a696-4d89-b03f-2fc3f982b37d': [self.field1.id, self.field2.id]
        })
        self.assertEqual(responses.calls[0].request.body, (
            'q=beginPosition%3A%5B2019-04-04T00%3A00%3A00Z+TO+2019-04-09T00%3A00%3A00Z%5D+cloudcoverpercentage%3A%5B0'
            '+TO+30%5D+platformname%3ASentinel-2+producttype%3AS2MSI1C+footprint%3A%22Contains%28POLYGON+%28%2839.09'
            '+47.78%2C+39.09+47.77%2C+39.1+47.77%2C+39.09+47.78%29%29%29%22'))
        self.assertEqual(responses.calls[1].request.body, (
            'q=beginPosition%3A%5B2019-04-04T00%3A00%3A00Z+TO+2019-04-09T00%3A00%3A00Z%5D+cloudcoverpercentage%3A%5B0'
            '+TO+30%5D+platformname%3ASentinel-2+producttype%3AS2MSI1C+footprint%3A%22Contains%28POLYGON+%28%2839.12'
            '+47.83%2C+39.12+47.82%2C+39.13+47.83%2C+39.12+47.83%29%29%29%22'))

    @responses.activate
    @freeze_time('2019-04-09')
    def test_loaded_ndvi(self):
        NDVI.objects.create(
            field=self.field1,
            product_id='00ae448d-6466-47a4-8237-56c0aa05cffb',
            date=datetime.now(),
            img='/tmp/tmp.png',
            mean=0,
            boundary=MultiPoint(Point(0, 0), Point(1, 1)))
        responses.add(
            method=responses.POST,
            url='https://scihub.copernicus.eu/dhus/search?format=json&rows=100&start=0',
            body=self.load_fixture('sentinel_query_api_response.json')
        )

        result = GetFieldProducts()(self.cad_info.field_set.order_by('id'), datetime.now())
        self.assertEqual(result, {
            '00ae448d-6466-47a4-8237-56c0aa05cffb': [self.field2.id],
            '69b20381-a696-4d89-b03f-2fc3f982b37d': [self.field1.id, self.field2.id]
        })


class TestLoadNDVI(BaseTestCase):
    test_media_root = '/tmp/agronom_test_media_root/'

    @property
    def fixtures_path(self):
        script_dir = os.path.dirname(__file__)

        return os.path.join(script_dir, 'fixtures')

    def setUp(self):
        super().setUp()

        self.field = mommy.make(
            'fields.Field',
            polygon='POLYGON((39.08 47.77, 39.10 47.77, 39.109 47.775, 39.088 47.775, 39.08 47.77))')

    @responses.activate
    def test_successful_load(self):
        product_id = '7320f6d7-c1fe-4723-8704-90231881dd34'
        url = "https://scihub.copernicus.eu/dhus/odata/v1/Products('%s')?$format=json" % product_id
        responses.add(
            method=responses.GET,
            url=url,
            body=self.load_fixture('sentinel_get_odata_api_response.json')
        )

        with tempfile.TemporaryDirectory() as tempdir, \
            override_settings(SENTINEL_PRODUCTS_DOWNLOAD_PATH=self.fixtures_path, MEDIA_ROOT=tempdir), \
                mock.patch('shutil.rmtree') as rmtree:
            result = LoadNDVI().load.run(
                product_id=product_id,
                field_ids=[self.field.id],
                cleanup=True,
            )
            self.assertTrue(result.is_success)

            ndvi_qs = self.field.ndvi_set
            self.assertEqual(ndvi_qs.count(), 1)

            ndvi = ndvi_qs.first()
            self.assertEqual(ndvi.product_id, product_id)
            self.assertEqual(ndvi.date, date(2019, 4, 1))
            self.assertEqual(ndvi.img.path, '%s/%s_%s.png' % (tempdir, self.field.id, product_id))
            self.assertEqual(ndvi.mean, Decimal('0.04'))
            self.assertEqual(ndvi.boundary.wkt, (
                'MULTIPOINT (39.07995277241874 47.77503602474064, 39.10905072921727 47.7750120679121, '
                '39.07994504955796 47.76999740415842, 39.10904019571561 47.76997345153469)'))

            actual_img_arr = np.array(Image.open(ndvi.img.path).convert('RGBA'))
            expected_img_arr = np.load(os.path.join(self.fixtures_path, 'expected_image_array.npy'))
            self.assertTrue(np.array_equal(actual_img_arr, expected_img_arr))

            rmtree.assert_called_once_with(
                '%s/%s' % (self.fixtures_path, 'S2A_MSIL1C_20190401T081601_N0207_R121_T37TEN_20190401T094937.zip'))

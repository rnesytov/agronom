import json
from django.urls import reverse
from rest_framework import status

from fields.models import Field
from core.tests.base_test_case import APITestCase
from .helpers import setup_cadastral_info


class TestFieldsAPI(APITestCase):
    FIELD_POLYGON_JSON = ('{ "type": "Polygon", "coordinates": [ [ [ 38.206071853637688, 53.970072576021586 ], '
                          '[ 38.210020065307617, 53.970552192883133 ], [ 38.206243515014648, 53.972849228691111 ], '
                          '[ 38.206071853637688, 53.970072576021586 ] ] ] }')
    FIELD_CENTROID_JSON = '{ "type": "Point", "coordinates": [ 38.20744514465332, 53.971157999198617 ] }'

    def test_field_craetion(self):
        cad_info = setup_cadastral_info(self.user)

        response = self.api_client.post(
            reverse('api_fields', kwargs={'cadastral_id': cad_info.id}),
            data={
                'name': 'Test field',
                'polygon': self.FIELD_POLYGON_JSON
            })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        field = Field.objects.last()
        self.assertEqual(field.cadastral, cad_info)

        self.assertEqual(field.polygon.geojson, self.FIELD_POLYGON_JSON)
        self.assertEqual(field.centroid.geojson, self.FIELD_CENTROID_JSON)
        self.assertEqual(field.name, 'Test field')

        self.assertEqual(response.json(), {
            'id': field.id,
            'centroid': json.loads(self.FIELD_CENTROID_JSON),
            'polygon': json.loads(self.FIELD_POLYGON_JSON),
            'color': '#333777',
            'crop_type': 'Wheat',
            'name': 'Test field'}
            )

    def test_invalid_cadastral_user(self):
        new_user = self._create_user('new_user@takewing.ru', 'q123')
        cad_info = setup_cadastral_info(new_user)

        response = self.api_client.post(
            reverse('api_fields', kwargs={'cadastral_id': cad_info.id}),
            data={
                'name': 'Test field',
                'polygon': self.FIELD_POLYGON_JSON
            })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

    def test_get_fields_list(self):
        cad_info = setup_cadastral_info(self.user)
        fields = [
            Field.objects.create(
                cadastral=cad_info,
                polygon=self.FIELD_POLYGON_JSON,
                centroid=self.FIELD_CENTROID_JSON,
                name='Field %s' % i
            )
            for i in range(2)
        ]

        response = self.api_client.get(reverse('api_fields', kwargs={'cadastral_id': cad_info.id}))
        polygon_dict = json.loads(self.FIELD_POLYGON_JSON)
        centroid_dict = json.loads(self.FIELD_CENTROID_JSON)

        self.assertEqual(response.json(), [{
                'centroid': centroid_dict,
                'color': '#333777',
                'crop_type': 'Wheat',
                'id': fields[0].id,
                'name': 'Field 0',
                'polygon': polygon_dict
            }, {
                'centroid': centroid_dict,
                'color': '#333777',
                'crop_type': 'Wheat',
                'id': fields[1].id,
                'name': 'Field 1',
                'polygon': polygon_dict
            }])

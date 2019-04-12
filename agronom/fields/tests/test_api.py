import json
from django.urls import reverse
from rest_framework import status
from model_mommy import mommy

from fields.models import Field
from core.tests.base_test_case import APITestCase


class TestFieldsAPI(APITestCase):
    FIELD_POLYGON_JSON = ('{ "type": "Polygon", "coordinates": [ [ [ 38.206071853637688, 53.970072576021586 ], '
                          '[ 38.210020065307617, 53.970552192883133 ], [ 38.206243515014648, 53.972849228691111 ], '
                          '[ 38.206071853637688, 53.970072576021586 ] ] ] }')
    FIELD_CENTROID_JSON = '{ "type": "Point", "coordinates": [ 38.20744514465332, 53.971157999198617 ] }'

    def test_field_craetion(self):
        cad_info = mommy.make('cadastral.CadastralInfo', user=self.user)

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
            'name': 'Test field'})

    def test_invalid_cadastral_user(self):
        cad_info = mommy.make('cadastral.CadastralInfo')

        response = self.api_client.post(
            reverse('api_fields', kwargs={'cadastral_id': cad_info.id}),
            data={
                'name': 'Test field',
                'polygon': self.FIELD_POLYGON_JSON
            })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

    def test_no_authenticated(self):
        cad_info = mommy.make('cadastral.CadastralInfo')
        self.api_client.logout()

        response = self.api_client.get(reverse('api_fields', kwargs={'cadastral_id': cad_info.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_get_fields_list(self):
        cad_info = mommy.make('cadastral.CadastralInfo', user=self.user)
        fields = mommy.make(Field, cadastral=cad_info, _fill_optional=True, _quantity=2)

        response = self.api_client.get(reverse('api_fields', kwargs={'cadastral_id': cad_info.id}))

        self.assertEqual(response.json(), [{
                'centroid': json.loads(fields[0].centroid.geojson),
                'color': fields[0].color,
                'crop_type': fields[0].crop_type,
                'id': fields[0].id,
                'name': fields[0].name,
                'polygon': json.loads(fields[0].polygon.geojson)
            }, {
                'centroid': json.loads(fields[1].centroid.geojson),
                'color': fields[1].color,
                'crop_type': fields[1].crop_type,
                'id': fields[1].id,
                'name': fields[1].name,
                'polygon': json.loads(fields[1].polygon.geojson)
            }])

    def test_delete_field(self):
        field = mommy.make(Field, cadastral__user=self.user)

        response = self.api_client.delete(
            reverse('api_fields', kwargs={'cadastral_id': field.cadastral.id}),
            data={'id': field.id})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Field.DoesNotExist):
            field.refresh_from_db()

    def test_update_field(self):
        field = mommy.make(Field, cadastral__user=self.user)

        response = self.api_client.put(
            reverse('api_fields', kwargs={'cadastral_id': field.cadastral.id}),
            data={
                'id': field.id,
                'name': 'Edited name',
                'color': '#fff',
                'polygon': self.FIELD_POLYGON_JSON})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        field.refresh_from_db()
        self.assertEqual(field.name, 'Edited name')
        self.assertEqual(field.color, '#fff')
        self.assertEqual(field.polygon.geojson, self.FIELD_POLYGON_JSON)

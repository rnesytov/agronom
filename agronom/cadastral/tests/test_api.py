import json
from django.urls import reverse
from rest_framework import status
from model_mommy import mommy

from cadastral.models import CadastralInfo
from core.tests.base_test_case import APITestCase


class TestCadastralAPI(APITestCase):
    cadastral_number = '86:11:0102013:2125'

    def test_cadsatral_info_craetion(self):
        response = self.api_client.post(
            reverse('api_cadastral'),
            data={'cadastral_number': self.cadastral_number}
        )

        cadastral_info = CadastralInfo.objects.last()
        self.assertIsNotNone(cadastral_info)
        self.assertEqual(cadastral_info.cadastral_number, self.cadastral_number)
        self.assertEqual(cadastral_info.loading_state, CadastralInfo.NOT_LOADED)
        self.assertIsNone(cadastral_info.polygon)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'id': cadastral_info.id,
            'loading_state': 0,
            'cadastral_number': '86:11:0102013:2125'
        })

    def test_invalid_cadastral_number(self):
        invalid_cad_number = 'Q123:11:0102013'

        response = self.api_client.post(
            reverse('api_cadastral'),
            data={'cadastral_number': invalid_cad_number}
        )

        cadastral_info = CadastralInfo.objects.filter(cadastral_number=invalid_cad_number)

        self.assertFalse(cadastral_info.exists())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'cadastral_number': ['Invalid cadastral number']})

    def test_get_cadastarl_info_list(self):
        cad_infos = mommy.make(CadastralInfo, user=self.user, _quantity=3)
        response = self.api_client.get(reverse('api_cadastral'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{
            'id': cad_infos[0].id,
            'loading_state': 0,
            'cadastral_number': cad_infos[0].cadastral_number,
            }, {
            'id': cad_infos[1].id,
            'loading_state': 0,
            'cadastral_number': cad_infos[1].cadastral_number,
            }, {
            'id': cad_infos[2].id,
            'loading_state': 0,
            'cadastral_number': cad_infos[2].cadastral_number,
        }])

    def test_retrieve_cadastral_info(self):
        cad_info = mommy.make(CadastralInfo, user=self.user, _fill_optional=True)

        response = self.api_client.get(reverse('api_cadastral', kwargs={'cadastral_id': cad_info.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'id': cad_info.id,
            'loading_state': cad_info.loading_state,
            'cadastral_number': cad_info.cadastral_number,
            'polygon': json.loads(cad_info.polygon.geojson)
        })

    def test_invalid_cadastral_user(self):
        new_user = mommy.make('customuser.User')
        cad_info = mommy.make(CadastralInfo, user=new_user)

        response = self.api_client.get(reverse('api_cadastral', kwargs={'cadastral_id': cad_info.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

    def test_no_authenticated(self):
        self.api_client.logout()

        response = self.api_client.get(reverse('api_cadastral'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

        cad_info = mommy.make(CadastralInfo, user=self.user)
        response = self.api_client.get(reverse('api_cadastral', kwargs={'cadastral_id': cad_info.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

from django.urls import reverse
from rest_framework import status

from cadastral.models import CadastralInfo
from core.tests.base_test_case import APITestCase


class TestCadastralAPI(APITestCase):
    def test_cadsatral_info_craetion(self):
        response = self.api_client.post(
            reverse('api_cadastral'),
            data={'cadastral_number': '86:11:0102013:2125'}
        )

        cadastral_info = CadastralInfo.objects.last()
        self.assertIsNotNone(cadastral_info)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
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
        self.assertEqual(response.data, {'cadastral_number': ['Invalid cadastral number']})

    def test_get_cadastarl_info_list(self):
        cad_infos = [
            CadastralInfo.objects.create(user=self.user, cadastral_number='86:11:0102013:212%s' % i)
            for i in range(3)
        ]

        response = self.api_client.get(reverse('api_cadastral'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'id': cad_infos[0].id,
            'loading_state': 0,
            'cadastral_number': '86:11:0102013:2120',
            }, {
            'id': cad_infos[1].id,
            'loading_state': 0,
            'cadastral_number': '86:11:0102013:2121',
            }, {
            'id': cad_infos[2].id,
            'loading_state': 0,
            'cadastral_number': '86:11:0102013:2122',
        }])

    def test_retrieve_cadastral_info(self):
        cad_info = CadastralInfo.objects.create(user=self.user, cadastral_number='86:11:0102013:2121')

        response = self.api_client.get(reverse('api_cadastral', kwargs={'cadastral_id': cad_info.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': cad_info.id,
            'loading_state': 0,
            'cadastral_number': '86:11:0102013:2121',
            'polygon': None
        })

    def test_invalid_cadastral_user(self):
        new_user = self._create_user('new_user@takewing.ru', 'q123')
        cad_info = CadastralInfo.objects.create(user=new_user, cadastral_number='86:11:0102013:2121')

        response = self.api_client.get(reverse('api_cadastral', kwargs={'cadastral_id': cad_info.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

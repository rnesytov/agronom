import responses
from model_mommy import mommy

from cadastral.services import SaveCadastralPolygon, GetCadastralPolygon
from cadastral.models import CadastralInfo
from core.tests.base_test_case import BaseTestCase


class TestSaveCadastralPolygon(BaseTestCase):
    @responses.activate
    def test_save_cadastral_polygon(self):
        cadastral_info = mommy.make(CadastralInfo, user=self.user, cadastral_number='71:12:030110:46')

        responses.add(
            responses.GET,
            'https://pkk5.rosreestr.ru/api/features/1/71:12:30110:46',
            body=self.load_fixture('feature_api_response.json'),
            status=200
        )
        responses.add(
            responses.GET,
            'https://apkk5.rosreestr.ru/arcgis/rest/services/Cadastre/CadastreSelected/MapServer/export',
            body=self.load_fixture('cadastral_poly_img.png', 'rb'),
            status=200,
            content_type='image/png'
        )
        result = SaveCadastralPolygon().save_polygon.run(cadastral_info.id)

        self.assertTrue(result.is_success)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(
            responses.calls[1].request.url, (
                'https://apkk5.rosreestr.ru/arcgis/rest/services/Cadastre/CadastreSelected/MapServer/export?dpi=96&tr'
                'ansparent=True&format=png8&layers=show%3A6%2C7&bbox=4231607.644111109%2C7169934.57139908%2C4232231.75'
                '483952%2C7170462.429686588&bboxSR=102100&size=800%2C+677&layerDefs=%7B%226%22%3A%22ID+%3D+%2771%3A12%'
                '3A30110%3A46%27%22%2C%227%22%3A%22ID+%3D+%2771%3A12%3A30110%3A46%27%22%7D&imageSR=102100&f=image'
                ))

        cadastral_info.refresh_from_db()
        self.assertEqual(cadastral_info, result.value)
        self.assertTrue(cadastral_info.loading_state, CadastralInfo.LOADED)
        self.assertJSONEqual(cadastral_info.polygon.geojson, self.load_fixture('expected_cad_poly.json'))

    def test_always_loaded_info(self):
        cadastral_info = mommy.make(CadastralInfo, user=self.user, loading_state=CadastralInfo.LOADED)
        result = SaveCadastralPolygon().save_polygon.run(cadastral_info.id)

        self.assertTrue(result.is_failure)
        self.assertTrue(result.failed_on('check_loading_state'))
        self.assertTrue(result.failed_because(SaveCadastralPolygon().save_polygon.failures.wrong_loading_state))


class TestGetCadastralPolygon(BaseTestCase):
    @responses.activate
    def test_multipoly_cadastral(self):
        responses.add(
            responses.GET,
            'https://pkk5.rosreestr.ru/api/features/1/61:2:600018:158',
            body=self.load_fixture('multipoly_feature_api_response.json'),
            status=200
        )
        responses.add(
            responses.GET,
            'https://apkk5.rosreestr.ru/arcgis/rest/services/Cadastre/CadastreSelected/MapServer/export',
            body=self.load_fixture('cadastral_multipoly_img.png', 'rb'),
            status=200,
            content_type='image/png'
        )
        result = GetCadastralPolygon().get_polygon.run('61:02:0600018:158')

        self.assertTrue(result.is_success)
        self.assertJSONEqual(result.value.geojson, self.load_fixture('expected_cad_multipoly.json'))

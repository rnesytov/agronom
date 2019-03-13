from core.tests.base_test_case import BaseTestCase

from fields.services import CheckPolygon
from .helpers import setup_cadastral_info


class TestCheckPolygon(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.cad_info = setup_cadastral_info(self.user)

    def test_successful_check(self):
        polygon_json = ('{ "type": "Polygon", "coordinates": [ [ [ 38.206071853637688, 53.970072576021586 ], '
                        '[ 38.210020065307617, 53.970552192883133 ], [ 38.206243515014648, 53.972849228691111 ], '
                        '[ 38.206071853637688, 53.970072576021586 ] ] ] }')
        centroid_json = '{ "type": "Point", "coordinates": [ 38.20744514465332, 53.971157999198603 ] }'

        result = CheckPolygon().check.run(cadastral_id=self.cad_info.id, polygon=polygon_json)

        self.assertTrue(result.is_success)
        self.assertEqual(result.value.geojson, centroid_json)

    def test_invalid_geo_type(self):
        point_json = '{"type":"Point","coordinates":[38.210856914520264,53.97183955821782]}'

        result = CheckPolygon().check.run(cadastral_id=self.cad_info.id, polygon=point_json)

        self.assertTrue(result.is_failure)
        self.assertTrue(result.failed_on('build_polygon_obj'))
        self.assertTrue(result.failed_because(CheckPolygon().check.failures.invalid_geometry_type))

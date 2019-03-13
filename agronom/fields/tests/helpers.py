from cadastral.models import CadastralInfo
from fields.models import Field


STUB_CADASTRAL_POLYGON = ('{ "type": "MultiPolygon", "coordinates": [ [ [ [ 38.20396900177002, 53.967522941095602 ], '
                          '[ 38.212723731994629, 53.967522941095602 ], [ 38.212723731994629, 53.97370742935837 ], '
                          '[ 38.20396900177002, 53.97370742935837 ], [ 38.20396900177002, 53.967522941095602 ] ] ] ] }')

STUB_FIELD_POLYGON = ('{ "type": "Polygon", "coordinates": [ [ [ 38.206071853637688, 53.970072576021586 ], '
                      '[ 38.210020065307617, 53.970552192883133 ], [ 38.206243515014648, 53.972849228691111 ], '
                      '[ 38.206071853637688, 53.970072576021586 ] ] ] }')
STUB_FIELD_CENTROID = '{ "type": "Point", "coordinates": [ 38.20744514465332, 53.971157999198603 ] }'


def setup_cadastral_info(user):
    return CadastralInfo.objects.create(
        user=user,
        cadastral_number='86:11:0102013:1',
        loading_state=CadastralInfo.LOADED,
        polygon=STUB_CADASTRAL_POLYGON)


def setup_field(cad_info):
    return Field.objects.create(
        cadastral=cad_info,
        name='Test field',
        polygon=STUB_FIELD_POLYGON,
        centroid=STUB_FIELD_CENTROID)

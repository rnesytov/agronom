import requests
import numpy as np

import rasterio
from rasterio.features import shapes
from rasterio.io import MemoryFile
from skimage.measure import approximate_polygon
from functools import partial

from enum import Enum, auto
from django.conf import settings
from django.contrib.gis.geos import MultiPolygon, Polygon, Point
from stories import story, arguments, Success, Failure, Result
from stories.shortcuts import failures_in

from cadastral.models import CadastralInfo


class GetCadastralPolygon:
    GET_FEATURE_API_URL = 'https://pkk5.rosreestr.ru/api/features/1/'
    GET_IMAGE_API_URL = 'https://apkk5.rosreestr.ru/arcgis/rest/services/Cadastre/CadastreSelected/MapServer/export'
    API_SRID = 102100

    IMG_BAND = 1
    MASK_VALUE = 10
    IMAGE_WIDTH = 800
    APPOXIMATE_TOLERANCE = 3

    @story
    @arguments('cadastral_number')
    def get_polygon(I):
        I.format_cadastral_nubmer
        I.send_get_feature_request
        I.check_get_feature_resposne
        I.build_min_max_points
        I.calc_img_height
        I.get_image
        I.extract_dataset
        I.extract_polygons

    def format_cadastral_nubmer(self, ctx):
        # Remove leading zeroes from parts of cad number
        splited = ctx.cadastral_number.split(':')

        def fix_part(part):
            part = part.lstrip('0')

            return part if part != '' else '0'

        formated_cad_num = ':'.join(list(map(fix_part, splited)))

        return Success(formated_cad_num=formated_cad_num)

    def send_get_feature_request(self, ctx):
        try:
            response = requests.get(
                self.GET_FEATURE_API_URL + ctx.formated_cad_num,
                timeout=settings.CADASTRAL_API_TIMEOUT
            )

            return Success(feature_response=response)
        except requests.exceptions.Timeout:
            return Failure(Errors.api_timeout)

    def check_get_feature_resposne(self, ctx):
        response = ctx.feature_response

        if response.status_code == requests.codes.ok:
            json = response.json()

            if json['status'] == 200 and json.get('feature') is not None and \
                json.get('feature', {}).get('center') is not None and \
                    json.get('feature', {}).get('extent') is not None:
                return Success(feature_data=json)

        return Failure(Errors.invalid_api_response)

    def build_min_max_points(self, ctx):
        min = Point(
            ctx.feature_data['feature']['extent']['xmin'],
            ctx.feature_data['feature']['extent']['ymin']
        )
        max = Point(
            ctx.feature_data['feature']['extent']['xmax'],
            ctx.feature_data['feature']['extent']['ymax']
        )

        return Success(min=min, max=max)

    def calc_img_height(self, ctx):
        divider = (ctx.min.x - ctx.max.x) / (ctx.min.y - ctx.max.y)
        height = round(self.IMAGE_WIDTH / divider)

        return Success(img_width=self.IMAGE_WIDTH, img_height=height)

    def get_image(self, ctx):
        bbox = "%s,%s,%s,%s" % (
            ctx.min.x,
            ctx.min.y,
            ctx.max.x,
            ctx.max.y
        )
        layer_defs = "{\"6\":\"ID = '%s'\",\"7\":\"ID = '%s'\"}" % (
            ctx.formated_cad_num,
            ctx.formated_cad_num
        )
        try:
            response = requests.get(
                self.GET_IMAGE_API_URL,
                params={
                    'dpi': 96,
                    'transparent': True,
                    'format': 'png8',
                    'layers': 'show:6,7',
                    'bbox': bbox,
                    'bboxSR': self.API_SRID,
                    'size': '%s, %s' % (ctx.img_width, ctx.img_height),
                    'layerDefs': layer_defs,
                    'imageSR': self.API_SRID,
                    'f': 'image'
                    },
                timeout=settings.CADASTRAL_API_TIMEOUT
            )
            return Success(img_response=response)
        except requests.exceptions.Timeout:
            return Failure(Errors.api_timeout)

    def extract_dataset(self, ctx):
        response = ctx.img_response

        if response.status_code == requests.codes.ok and response.headers['Content-Type'] == 'image/png':
            with MemoryFile(response.content) as memfile:
                with memfile.open() as dataset:
                    return Success(band=dataset.read(self.IMG_BAND))
        else:
            return Failure(Errors.invalid_api_response)

    def _approximate_and_normalize_poly(self, affine, shape):
        coords = np.array(shape[0]['coordinates'][0])

        approximated_poly = approximate_polygon(coords, tolerance=self.APPOXIMATE_TOLERANCE)
        normalized_poly = np.apply_along_axis(affine.__mul__, 1, approximated_poly)  # affine * [x, y]

        polygon = Polygon(normalized_poly, srid=self.API_SRID)
        polygon.transform(4326)

        return polygon

    def extract_polygons(self, ctx):
        mask = ctx.band == self.MASK_VALUE
        list_shapes = shapes(ctx.band, mask)
        affine = rasterio.transform.from_bounds(
            west=ctx.min.x,
            south=ctx.min.y,
            east=ctx.max.x,
            north=ctx.max.y,
            width=ctx.img_width,
            height=ctx.img_height
        )

        polygons = list(map(partial(self._approximate_and_normalize_poly, affine), list_shapes))

        return Result(MultiPolygon(polygons))


class SaveCadastralPolygon:
    @story
    @arguments('cadastral_id')
    def save_polygon(I):
        I.find_cadastral_object
        I.check_loading_state
        I.load_polygon

    def find_cadastral_object(self, ctx):
        try:
            obj = CadastralInfo.objects.get(id=ctx.cadastral_id)

            return Success(obj=obj, cadastral_number=obj.cadastral_number)
        except CadastralInfo.DoesNotExist:
            return Failure(Errors.cadastral_not_found)

    def check_loading_state(self, ctx):
        if ctx.obj.loading_state == CadastralInfo.NOT_LOADED:
            return Success()
        else:
            return Failure(Errors.wrong_loading_state)

    def load_polygon(self, ctx):
        obj = ctx.obj
        result = GetCadastralPolygon().get_polygon.run(obj.cadastral_number)

        if result.is_success:
            obj.polygon = result.value
            obj.loading_state = CadastralInfo.LOADED
            obj.save()

            return Result(obj)
        else:
            if not result.failed_because(Errors.api_timeout):
                obj.loading_state = CadastralInfo.FAILED

                obj.save()

            return result


@failures_in(GetCadastralPolygon)
@failures_in(SaveCadastralPolygon)
class Errors(Enum):
    cadastral_not_found = auto()
    wrong_loading_state = auto()
    api_timeout = auto()
    invalid_api_response = auto()
    failed_to_extraxt_polygon = auto()

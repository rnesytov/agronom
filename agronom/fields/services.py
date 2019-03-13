from enum import Enum, auto
from stories import story, arguments, Success, Failure, Result
from stories.shortcuts import failures_in
from django.contrib.gis.geos import GEOSGeometry


class CheckPolygon:
    @story
    @arguments('cadastral_id', 'polygon')
    def check(I):
        I.build_polygon_obj
        I.calc_field_centroid

    def build_polygon_obj(self, ctx):
        field_poly = GEOSGeometry(str(ctx.polygon))

        if field_poly.geom_type == 'Polygon':
            return Success(field_poly=field_poly)
        else:
            return Failure(Errors.invalid_geometry_type)

    def calc_field_centroid(self, ctx):
        return Result(ctx.field_poly.centroid)


@failures_in(CheckPolygon)
class Errors(Enum):
    invalid_geometry_type = auto()

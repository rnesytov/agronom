import numpy as np
from rasterio import enums, features, warp
from affine import Affine
from stories import story, arguments, Result, Success
from django.conf import settings
from django.contrib.gis.geos import Point, MultiPoint

from fields.models import Field


class ExtractNDVIForField:
    RED_BAND_IDX = 1  # About band indexes
    NIR_BAND_IDX = 4  # https://gdal.org/frmt_sentinel2.html

    @property
    def upscale_factor(self):
        return settings.NDVI_UPSCALE_FACTOR

    @property
    def upscale_transform(self):
        return Affine.scale(1 / self.upscale_factor)

    @story
    @arguments('dataset', 'field_id')
    def extract(I):
        I.find_field
        I.transform_polygon
        I.upscale_and_mask_bands
        I.calc_ndvi

    def find_field(self, ctx):
        field = Field.objects.get(pk=ctx.field_id)

        return Success(field=field)

    def transform_polygon(self, ctx):
        polygon = ctx.field.polygon.transform(ctx.dataset.crs.to_epsg(), True)

        return Success(polygon=polygon)

    def _process_band(self, dataset, window, mask, out_shape, band_index):
        band = dataset.read(window=window, masked=True, indexes=band_index)

        upscaled = np.ma.zeros(out_shape)

        warp.reproject(
            source=band,
            src_crs=dataset.crs,
            dst_crs=dataset.crs,
            destination=upscaled,
            src_transform=dataset.transform,
            dst_transform=dataset.transform * self.upscale_transform,
            resampling=enums.Resampling.bilinear
        )

        upscaled.mask = mask

        return upscaled.filled(0)

    def upscale_and_mask_bands(self, ctx):
        shapes = [{'type': 'Polygon', 'coordinates': ctx.polygon.coords}]

        window = features.geometry_window(
            dataset=ctx.dataset,
            shapes=shapes,
            north_up=ctx.dataset.transform.e <= 0,
            rotated=ctx.dataset.transform.b != 0 or ctx.dataset.transform.d != 0
        )
        window_transform = ctx.dataset.window_transform(window) * self.upscale_transform

        out_shape = (int(window.height) * self.upscale_factor, int(window.width) * self.upscale_factor)
        mask = features.geometry_mask(
            geometries=shapes,
            out_shape=out_shape,
            transform=window_transform,
            all_touched=True)

        red = self._process_band(ctx.dataset, window, mask, out_shape, self.RED_BAND_IDX)
        nir = self._process_band(ctx.dataset, window, mask, out_shape, self.NIR_BAND_IDX)

        def point_builder(x, y):
            return Point(window_transform * (x, y), srid=ctx.dataset.crs.to_epsg()).transform(4326, True)

        boundary = MultiPoint(
            point_builder(0, 0),
            point_builder(out_shape[1], 0),
            point_builder(0, out_shape[0]),
            point_builder(out_shape[1], out_shape[0]))

        return Success(red=red, nir=nir, boundary=boundary)

    def calc_ndvi(self, ctx):
        red = ctx.red.astype(float)
        nir = ctx.nir.astype(float)
        check = np.logical_or(red > 0, nir > 0)

        with np.errstate(divide='ignore', invalid='ignore'):  # allow zero division
            ndvi = np.where(check, (nir - red) / (nir + red), np.NaN)

        mean = np.nanmean(ndvi)

        return Result({'ndvi': ndvi, 'ndvi_mean': mean, 'boundary': ctx.boundary})

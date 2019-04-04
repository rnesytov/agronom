import shutil
import rasterio
import rasterio.mask
import numpy as np
import matplotlib.image
from os.path import join
from datetime import date, timedelta
from stories import story, arguments, Result, Success
from sentinelsat import SentinelAPI
from django.conf import settings

from .models import NDVI
from fields.models import Field


def ndvi_image_filename(field_id, product_id, file_format='png'):
    return '%s_%s.%s' % (field_id, product_id, file_format)


class SentinelAPIMixin:
    API_URL = 'https://scihub.copernicus.eu/dhus'

    def get_api(self):
        return SentinelAPI(
            user=settings.SCIHUB_LOGIN,
            password=settings.SCIHUB_PASSWORD,
            api_url=self.API_URL,
            show_progressbars=False
        )


class GetFieldProducts(SentinelAPIMixin):
    API_PLATFORM_NAME = 'Sentinel-2'
    API_PRODUCT_TYPE = 'S2MSI1C'

    def __init__(self):
        self.api = SentinelAPI(
            user=settings.SCIHUB_LOGIN,
            password=settings.SCIHUB_PASSWORD,
            api_url=self.API_URL
        )

    @property
    def days_past(self):
        return timedelta(settings.SENTINEL_PRODUCTS_DAYS_PAST)

    @property
    def max_clouds_percentage(self):
        return settings.SENTINEL_MAX_CLOUD_PERCENTAGE

    def find_products(self, area, product_date):
        return self.api.query(
            area=area,
            area_relation='Contains',
            date=(product_date - self.days_past, product_date),
            platformname=self.API_PLATFORM_NAME,
            producttype=self.API_PRODUCT_TYPE,
            cloudcoverpercentage=(0, self.max_clouds_percentage)
        )

    def __call__(self, fields_qs, product_date=None):
        if product_date is None:
            product_date = date.today()

        product_fields_map = {}

        for field in fields_qs.iterator():
            products = self.find_products(field.polygon.wkt, product_date)
            products_ids = set(products.keys())

            existing = set(
                NDVI.objects.filter(
                    field=field,
                    product_id__in=products_ids
                ).values_list('product_id', flat=True)
            )

            for product_id in products_ids - existing:
                product_fields_map[product_id] = product_fields_map.get(product_id, []) + [field.id]

        return product_fields_map


class ExtractNDVIForField:
    RED_BAND_IDX = 3  # About band indexes
    NIR_BAND_IDX = 4  # https://gdal.org/frmt_sentinel2.html

    @story
    @arguments('src', 'field_id')
    def extract(I):
        I.find_field
        I.transform_polygon
        I.mask_bands
        I.calc_ndvi

    def find_field(self, ctx):
        field = Field.objects.get(pk=ctx.field_id)

        return Success(field=field)

    def transform_polygon(self, ctx):
        polygon = ctx.field.polygon.transform(ctx.src.crs.to_epsg(), True)

        return Success(polygon=polygon)

    def mask_bands(self, ctx):
        mask = [{'type': 'Polygon', 'coordinates': ctx.polygon.coords}]

        red, trared = rasterio.mask.mask(ctx.src, mask, crop=True, indexes=self.RED_BAND_IDX)
        nir, tranir = rasterio.mask.mask(ctx.src, mask, crop=True, indexes=self.NIR_BAND_IDX)

        return Success(red=red, nir=nir)

    def calc_ndvi(self, ctx):
        red = ctx.red.astype(float)
        nir = ctx.nir.astype(float)
        check = np.logical_or(red > 0, nir > 0)

        with np.errstate(divide='ignore', invalid='ignore'):  # allow zero division
            ndvi = np.where(check, (nir - red) / (nir + red), np.NaN)

        mean = np.nanmean(ndvi)

        return Result({'ndvi': ndvi, 'ndvi_mean': mean})


class LoadNDVI(SentinelAPIMixin):
    NDVI_COLOR_MAP = 'summer'

    @arguments('product_id', 'field_ids', 'cleanup')
    @story
    def load(I):
        I.download_product
        I.extract_subdataset_path
        I.extract_ndvi
        I.save_ndvis
        I.maybe_cleanup

    def download_product(self, ctx):
        api = self.get_api()

        product = api.download(
            id=ctx.product_id,
            directory_path=settings.SENTINEL_PRODUCTS_DOWNLOAD_PATH,
            checksum=True)

        return Success(product=product)

    def extract_subdataset_path(self, ctx):
        with rasterio.open(ctx.product['path']) as src:
            return Success(subdataset_path=src.subdatasets[0])  # First dataset with bands B2, B3, B4, B8

    def extract_ndvi(self, ctx):
        ndvis = []

        with rasterio.open(ctx.subdataset_path) as src:
            for field_id in ctx.field_ids:
                result = ExtractNDVIForField().extract.run(src, field_id)

                filename = ndvi_image_filename(field_id, ctx.product_id)
                path = join(settings.MEDIA_ROOT, filename)
                matplotlib.image.imsave(path, result.value['ndvi'], cmap=self.NDVI_COLOR_MAP)

                if result.is_success:
                    ndvis.append(NDVI(
                        field_id=field_id,
                        product_id=ctx.product_id,
                        date=ctx.product['date'],
                        img=filename,
                        mean=result.value['ndvi_mean']))
                # TODO: some errors, warnings etc

        return Success(ndvis=ndvis)

    def save_ndvis(self, ctx):
        NDVI.objects.bulk_create(ctx.ndvis)

        return Success()

    def maybe_cleanup(self, ctx):
        if ctx.cleanup:
            shutil.rmtree(ctx.products_path)

        return Result()

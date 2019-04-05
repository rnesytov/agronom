import shutil
import rasterio
import matplotlib.image
from os.path import join
from stories import story, arguments, Result, Success
from django.conf import settings

from core.logging import getLogger
from .mixins import SentinelAPIMixin
from .extract_ndvi import ExtractNDVIForField
from ndvi.models import NDVI


def ndvi_image_filename(field_id, product_id, file_format='png'):
    return '%s_%s.%s' % (field_id, product_id, file_format)


class LoadNDVI(SentinelAPIMixin):
    NDVI_COLOR_MAP = 'summer'

    @property
    def logger(self):
        return getLogger(self.__class__.__name__)

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

        with rasterio.open(ctx.subdataset_path) as dataset:
            for field_id in ctx.field_ids:
                result = ExtractNDVIForField().extract.run(dataset, field_id)

                if result.is_success:
                    filename = ndvi_image_filename(field_id, ctx.product_id)
                    path = join(settings.MEDIA_ROOT, filename)
                    matplotlib.image.imsave(
                        fname=path,
                        arr=result.value['ndvi'],
                        vmin=0,
                        vmax=1,
                        cmap=self.NDVI_COLOR_MAP)

                    ndvis.append(NDVI(
                        field_id=field_id,
                        product_id=ctx.product_id,
                        date=ctx.product['date'],
                        img=filename,
                        mean=result.value['ndvi_mean'],
                        boundary=result.value['boundary']))
                else:
                    self.logger.error('ExtractNDVIForField failed with %s' % result.value)

        return Success(ndvis=ndvis)

    def save_ndvis(self, ctx):
        NDVI.objects.bulk_create(ctx.ndvis)

        return Success()

    def maybe_cleanup(self, ctx):
        if ctx.cleanup:
            shutil.rmtree(settings.SENTINEL_PRODUCTS_DOWNLOAD_PATH)

        return Result()

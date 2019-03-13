from agronom.celery import app
from django.conf import settings

from .services import SaveCadastralPolygon


@app.task(bind=True, ignore_results=True, max_retries=10)
def get_cadastral_polygon(self, cadastral_id):
    result = SaveCadastralPolygon().save_polygon.run(cadastral_id)

    if result.is_failure:
        if result.failed_because(SaveCadastralPolygon().save_polygon.failures.api_timeout):
            raise self.retry(countdown=settings.CADASTRAL_INFO_TIMEOUT_DELAY)

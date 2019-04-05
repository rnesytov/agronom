from sentinelsat import SentinelAPI
from django.conf import settings


class SentinelAPIMixin:
    API_URL = 'https://scihub.copernicus.eu/dhus'

    def get_api(self):
        return SentinelAPI(
            user=settings.SCIHUB_LOGIN,
            password=settings.SCIHUB_PASSWORD,
            api_url=self.API_URL,
            show_progressbars=False
        )

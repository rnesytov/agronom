import os

from django.core.exceptions import ImproperlyConfigured


def safe_getenv(env_name):
    value = os.getenv(env_name)
    if value is None:
        raise ImproperlyConfigured(f'Environtment varialbe "{env_name}" is not set')
    return value


CELERY_BROKER_URL = safe_getenv('CELERY_BROKER_URL')

METRICS_BROKER_URL = safe_getenv('METRICS_BROKER_URL')

CACHEOPS_REDIS = safe_getenv('CACHEOPS_REDIS')

STATIC_ROOT = '/volumes/static/'
MEDIA_ROOT = '/volumes/media/'

ACTIVITY_METRICS_REDIS_URL = safe_getenv('ACTIVITY_METRICS_REDIS_URL')

# Settings for querying logs from elastic for support users
ELASTIC_HOST = safe_getenv('ELASTIC_HOST')
ELASTIC_USER = safe_getenv('ELASTIC_USER')
ELASTIC_PASSWORD = safe_getenv('ELASTIC_PASSWORD')

ELASTIC_INDEX_FILE_PATH = '/elk/logstash/logstash-index.json'

# CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [
#     (safe_getenv('CHANNEL_REDIS_HOST'), safe_getenv('CHANNEL_REDIS_PORT')),
# ]

SENTRY_URL = os.getenv('SENTRY_URL')  # Sentry URL, missing in dev mode.

DATABASES['default'].update({
    'NAME': safe_getenv('POSTGRES_DB_NAME'),
    'USER': safe_getenv('POSTGRES_USER'),
    'PASSWORD': safe_getenv('POSTGRES_PASSWORD'),
    'HOST': safe_getenv('POSTGRES_HOST'),
})

try:
    LOGGING['handlers']['logstash']['host'] = ''
except KeyError:  # In light settings no handlers
    pass

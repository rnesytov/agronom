CELERY_BROKER_URL = 'amqp://backend:password@rabbit:5672/backend'  # host on default network, non-TLS port

METRICS_BROKER_URL = 'amqp://backend:password@rabbit:5672/backend'

CACHEOPS_REDIS = "redis://redis:6379/1"

STATIC_ROOT = '/volumes/static/'
MEDIA_ROOT = '/volumes/media/'

ACTIVITY_METRICS_REDIS_URL = 'redis://redis:6379'

# Settings for querying logs from elastic for support users
ELASTIC_HOST = 'elasticsearch'
ELASTIC_USER = 'elastic'
ELASTIC_PASSWORD = 'password'

ELASTIC_INDEX_FILE_PATH = '/elk/logstash/logstash-index.json'

# CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [
#     ('redis', 6379),
# ]

DATABASES['default'].update({
    'NAME': f'test_{PROJECT_NAME}_db',
    'USER': f'test_{PROJECT_NAME}_user',
    'PASSWORD': 'pass',
    'HOST': 'postgres',  # host on default network
})

try:
    LOGGING['handlers']['logstash']['host'] = ''
except KeyError:  # In light settings no handlers
    pass

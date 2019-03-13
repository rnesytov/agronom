CELERY_BROKER_URL = 'amqp://backend:password@localhost:5672/backend'

METRICS_BROKER_URL = 'amqp://backend:password@localhost:5672/backend'

ACTIVITY_METRICS_REDIS_URL = 'redis://localhost:6379'

DATABASES['default'].update({
    'HOST': 'localhost',
    'USER': f'test_{PROJECT_NAME}_user',
    'PASSWORD': 'pass',
    'NAME': f'{PROJECT_NAME}_db',
})

import os

from django.contrib import messages

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'logstash': {
            'level': 'DEBUG',
            'class': 'logstash.TCPLogstashHandler',  # Use logstash.LogstashHandler for short messages
            'host': '127.0.0.1',
            'port': 5044,  # Default port of logstash
            'version': 1,  # Version of logstash event schema. Default value: 0
                           #  (for backward compatibility of the library)
            'message_type': 'logstash',  # 'type' field in logstash message. Default value: 'logstash'.
            'fqdn': False,  # Fully qualified domain name. Default value: false.
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logstash', 'console'],
            'level': 'INFO',
        },
        'backend': {
            'handlers': ['logstash'],
            'level': 'INFO',
        },
        'celery': {
            'handlers': ['logstash'],
            'level': 'DEBUG',
        }
    },
}

DEFAULT_FROM_EMAIL = "from@example.com"
ALERTS_PHONE_NUMBER = '+71111111111'
ALERTS_EMAILS = ['to@example.com']

# Settings for querying logs from elastic for support users
ELASTIC_HOST = None
ELASTIC_USER = None
ELASTIC_PASSWORD = None
ELASTIC_TIMEOUT = 5

WATCHDOG_FILE = None

# Настройка правильного стиля для вывода сообщений об ошибках с помощью
# приложения messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

ELASTIC_INDEX_FILE_PATH = os.path.join(
    BASE_DIR, "../configs/elk/logstash/logstash-index.json"
)

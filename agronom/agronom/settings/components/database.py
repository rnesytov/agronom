import sys

DATABASES = {
    'default': {
        'ENGINE': (
            # celery has problems with geventpool (celery forks after pool creation),
            # use sync connection pool for it.
            # Maybe, instead of 'if' this should be separate config
            'django.contrib.gis.db.backends.postgis' if sys.argv[0].endswith('/celery')
            else 'django_db_geventpool.backends.postgis'
        ),
        'NAME': None,  # update in child configs
        'USER': None,  # update in child configs
        'PASSWORD': None,  # update in child configs
        'HOST': None,  # update in child configs
        'PORT': '',
        'CONN_MAX_AGE': 0,
    },
}

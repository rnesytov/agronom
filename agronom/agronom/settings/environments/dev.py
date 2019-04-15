import os

DEBUG = True

INTERNAL_IPS = ['127.0.0.1', 'localhost']

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'rest_framework_docs',
    'crispy_forms',  # Красивые формы в документации
    'debug_toolbar',
    'debug_panel',
    'django_extensions',
    'webpack_loader'
]

MIDDLEWARE = [
    'debug_panel.middleware.DebugPanelMiddleware',
] + MIDDLEWARE

CACHES = {
    'default': {
        # do not actually use cache in dev (for faster tests)
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    # for debugging and tests only
    f'{PROJECT_NAME}.helpers.CsrfExemptSessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
)

# set very high throttle rates for tests
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    #  Default for all views (all views will catch them in get_throttles method)
    'anon': '10000/min',
    'user': '30000/min',
}

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += (
    'rest_framework.renderers.BrowsableAPIRenderer',
)

ELASTIC_INDEX_FILE_PATH = os.path.join(
    BASE_DIR, '../configs/elk/logstash/logstash-index.json'
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'STATS_FILE': os.path.join(BASE_DIR, 'frontend/build/webpack-stats.json')
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_FILE_NAME = 'junit.xml'

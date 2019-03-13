
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # Restrictive default permission
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'core.jsonrenderer.DecimalJSONRenderer',
    ),
    'DEFAULT_THROTTLE_RATES': {
        #  Default for all views (all views will catch them in get_throttles method)
        'anon': '100/min',
        'user': '300/min',

    },
    'NON_FIELD_ERRORS_KEY': 'non_field_errors',
    'DATETIME_FORMAT': '%s',
    'COERCE_DECIMAL_TO_STRING': True,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'EXCEPTION_HANDLER': 'core.exception_handler.custom_exception_handler',
}

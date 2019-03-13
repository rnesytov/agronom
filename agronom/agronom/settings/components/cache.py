
# Cacheops settings
CACHEOPS_DEFAULTS = {
    'ops': 'all',
    'timeout': 60 * 60,
}

CACHEOPS = {
    'core.*': {},
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

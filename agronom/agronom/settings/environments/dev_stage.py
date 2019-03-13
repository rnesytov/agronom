# WARNING: this config should be applied after environments.dev

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]

RAVEN_CONFIG = {
    'dsn': SENTRY_URL,
}

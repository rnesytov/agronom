"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
Default environment is `dev_local`.
To change settings file:
`DJANGO_ENV=prod_k8s_hotfix python manage.py runserver`
"""
from django.core.exceptions import ImproperlyConfigured
from split_settings.tools import include
from os import environ


settings = [
    'components/base.py',
    'components/internationalization.py',
    'components/auth.py',
    'components/database.py',
    'components/cache.py',
    'components/celery.py',
    'components/logic.py',
    'components/logs.py',
    'components/rest.py',
    'components/redis_db_numbers.py',
    'components/fake_secrets.py',
    'components/sensitive.py',
    'components/leaflet.py',
    'components/allauth.py'
]

# Hardcoded deploy variants. Hardcode here solves two problems:
# - everyone knows, what deploys are used
# - keep variants to a reasonable minimum
deploy_variants = {
    # For development on local machine
    'dev_local': [
        'environments/dev.py',
        'deploys/local.py',
    ],
    # Runs in docker-compose
    'dev_docker': [
        'environments/dev.py',
        'deploys/docker.py',
    ],
    # "Normal" dev environment for k8s
    'dev_k8s': [
        'environments/dev.py',
        'deploys/k8s.py',
        'components/k8s_secrets.py',
    ],
    # "Half-production" dev environment for k8s (sentry is enabled)
    'dev_stage_k8s': [
        'environments/dev.py',
        'deploys/k8s.py',
        'components/k8s_secrets.py',
        'environments/dev_stage.py',
    ],
    # For ci (dev without logs)
    'dev_k8s_ci': [
        'environments/dev.py',
        'deploys/k8s.py',
        'components/k8s_secrets.py',
        'deploys/k8s_ci.py',
    ],
}

ENV = environ.get('DJANGO_ENV') or 'dev_local'
if ENV in deploy_variants:
    settings += deploy_variants[ENV]
else:
    variants_list = list(deploy_variants.keys())
    raise ImproperlyConfigured(
        f'DJANGO_ENV="{ENV}" is not in list of available variants {variants_list}'
    )

include(*settings)

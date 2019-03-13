import os

DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL', 'Agronom <noreply@agronom.com>')
EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", 'smtp.sendgrid.com')
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_PASSWORD")
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_USERNAME')
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_SUBJECT_PREFIX = os.environ.get("EMAIL_SUBJECT_PREFIX", '[Agronom]')
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER

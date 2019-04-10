from celery.schedules import crontab

CELERY_BROKER_USE_SSL = False

CELERY_TASK_ROUTES = {
    # 'sms.tasks.*': {'queue': 'sms'},
}

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'UTC'  # Other timezone can cause infinite backend_cleanup tasks

CELERY_BEAT_SCHEDULE = {
    'update_weather': {
        'task': 'weather.tasks.update_current_weather_for_all_fields',
        'schedule': crontab(hour=3)
    },
    'load_ndvi': {
        'task': 'ndvi.tasks.load_ndvi_for_all_fields',
        'shedule': crontab(hour=4)
    }
}

# Integration tests with acquiring api are slow and can fail
# because of unstable demo servers. They are skipped by default.
SKIP_ACQUIRING_TESTS = True

# When profiling is enabled, unauthenticated users can see
# very sensitive data
ENABLE_UNSAFE_PROFILING = False

# Name of metics excange in RabbitMQ.
# Can be created in the same vhost as celery, so do not name
# this with name of celery queue or internal celery name.
METRICS_EXCHANGE = 'metrics_exchange'

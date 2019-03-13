import os

from django.conf import settings

from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown


app = Celery(settings.PROJECT_NAME)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


if os.getenv('COVERAGE_FILE', None):

    coverage_instance = None

    @worker_process_init.connect
    def start_coverage_in_worker_process(*args, **kwargs):
        """
        start coverage measuring in child worker processes
        :param args:
        :param kwargs:
        :return:
        """
        import coverage
        global coverage_instance
        coverage_instance = coverage.coverage(
            config_file='.docker_coveragerc', source='.',
            data_file=os.getenv('COVERAGE_FILE') + '.pid.' + str(os.getpid()),
        )
        coverage_instance.start()

    @worker_process_shutdown.connect
    def end_coverage_in_worker_process(*args, **kwargs):
        """
        stop coverage measuring and save results before exit of child
        worker processes
        :param args:
        :param kwargs:
        :return:
        """
        coverage_instance.stop()
        coverage_instance.save()

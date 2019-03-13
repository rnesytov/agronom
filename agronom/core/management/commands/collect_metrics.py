import _thread

from django.conf import settings
from django.core.management.base import BaseCommand
from prometheus_client import start_http_server, Summary, Gauge

import core.metrics as metrics


DEPOSIT_SUCCESS_SUMMARY = Summary(
    'backend_deposit_successful',
    "Number and amounts of successful deposit trades",
)
DEPOSIT_FAILED_SUMMARY = Summary(
    'backend_deposit_failed',
    "Number and amounts of failed deposit trades",
)

USERS_WITH_TRADES_LAST_GAUGE = Gauge(
    'backend_users_with_trades_last_{}s'.format(metrics.PERIOD),
    "Users with trades during last {} seconds".format(metrics.PERIOD),
)


METRICS = {
    metrics.DEPOSIT_SUCCESS_SUMMARY: lambda x: DEPOSIT_SUCCESS_SUMMARY.observe(float(x)),
    metrics.DEPOSIT_FAILED_SUMMARY: lambda x: DEPOSIT_FAILED_SUMMARY.observe(float(x)),
    metrics.USERS_WITH_TRADES_LAST_GAUGE: lambda x: USERS_WITH_TRADES_LAST_GAUGE.set(float(x)),
}


class Command(BaseCommand):
    help = 'Collect metrics and send to prometheus'

    def handle(self, *args, **options):

        start_http_server(8001)

        _thread.start_new_thread(collect_metrics_tasks, ())

        channel = metrics.connect_to_metrics_exchange()

        channel.exchange_declare(exchange=settings.METRICS_EXCHANGE, exchange_type='fanout')

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=settings.METRICS_EXCHANGE, queue=queue_name)

        channel.basic_consume(
            callback, queue=queue_name, no_ack=True
        )

        channel.start_consuming()


def callback(ch, method, properties, body):
    metric_name, metric_value = body.decode('UTF-8').split(':')
    METRICS[metric_name](metric_value)
    print(f'{metric_name} : {metric_value}')


def collect_metrics_tasks():
    pass
    #  while True:
    #      management.call_command('online_users', time=10)
    #      management.call_command('users_with_trades', time=10)
    #      sleep(10)

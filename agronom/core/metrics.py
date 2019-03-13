import redis
import pika
from pika.exceptions import ConnectionClosed

from django.utils import timezone
from django.conf import settings

PERIOD = 10

DEPOSIT_SUCCESS_SUMMARY = "DEPOSIT_SUCCESS_SUMMARY"
DEPOSIT_FAILED_SUMMARY = "DEPOSIT_FAILED_SUMMARY"

USERS_LOGIN_LAST_GAUGE = "BACKEND_USERS_LOGIN_LAST_{}s".format(PERIOD)

redis_connections = {
    settings.ACTIVITY_METRICS_REDIS_DB_TRADES: redis.StrictRedis.from_url(
        url=settings.ACTIVITY_METRICS_REDIS_URL,
        db=settings.ACTIVITY_METRICS_REDIS_DB_TRADES,
    ),
    settings.ACTIVITY_METRICS_REDIS_DB_ONLINE: redis.StrictRedis.from_url(
        url=settings.ACTIVITY_METRICS_REDIS_URL,
        db=settings.ACTIVITY_METRICS_REDIS_DB_ONLINE,
    ),
}


def connect_to_metrics_exchange():
    # FIXME: add socket_timeout and blocked_connection_timeout
    connection = pika.BlockingConnection(pika.URLParameters(settings.METRICS_BROKER_URL))
    channel = connection.channel()
    channel.exchange_declare(exchange=settings.METRICS_EXCHANGE, exchange_type='fanout')
    return channel


metrics_channel = None


def publish(metric_name, metric_value):
    message = f"{metric_name}:{metric_value}"
    global metrics_channel
    if metrics_channel is None:  # Connect on first publish
        metrics_channel = connect_to_metrics_exchange()
    try:
        metrics_channel.basic_publish(
            exchange=settings.METRICS_EXCHANGE, routing_key='', body=message
        )
    except (ConnectionClosed, FileNotFoundError):
        metrics_channel = connect_to_metrics_exchange()  # try to reconnect
        metrics_channel.basic_publish(
            exchange=settings.METRICS_EXCHANGE, routing_key='', body=message
        )


def mark_user_id_active(user_id, db):
    """
    Mark a user as "active".
    """
    redis_conn = redis_connections[db]
    redis_conn.set(user_id, timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S.%f'))

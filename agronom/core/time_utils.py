import datetime

from django.utils.timezone import get_default_timezone


def round_timestamp_to_default_tz_midnight(timestamp):
    default_tz = get_default_timezone()
    datetime_ = default_tz.localize(datetime.datetime.fromtimestamp(timestamp))
    time_ = datetime_.time()
    midnight = datetime.datetime.combine(
        datetime_, datetime.time.min,
    )
    midnight = default_tz.localize(midnight)
    if time_ > datetime.time(12, 0, 0):
        return midnight + datetime.timedelta(days=1)
    else:
        return midnight


def datetime_to_unix(dt: datetime.datetime):
    """
    Converts datetime object to seconds since the epoch
    :param dt: datetime object
    :return: seconds since the epoch, integer
    """
    return int(dt.timestamp())

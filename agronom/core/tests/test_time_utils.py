import datetime
from unittest import TestCase

import pytz
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

from ..time_utils import round_timestamp_to_default_tz_midnight


class TestRoundToMSK(TestCase):

    def test_how_timezones_work(self):
        """
        Just testing of library functions. Kept here for educational reasons.
        """
        base_datetime_msk = parse_datetime('2018-01-01T00:00:00+03')
        self.assertIsNotNone(base_datetime_msk)
        base_datetime_utc = parse_datetime('2018-01-01T00:00:00Z')
        self.assertIsNotNone(base_datetime_utc)
        self.assertEqual(base_datetime_utc - base_datetime_msk, datetime.timedelta(hours=3))

        now = datetime.datetime.now()
        now_london = pytz.timezone('Europe/London').localize(now)
        now_moscow = pytz.timezone('Europe/London').localize(now)
        self.assertEqual(now_london.timestamp(), now_moscow.timestamp())

    def test_round_timestamp_to_MSK_midnight(self):
        base_timestamp = parse_datetime('2018-01-01T00:00:00+03').timestamp()
        base_datetime = make_aware(datetime.datetime(2018, 1, 1))
        self.assertEqual(
            round_timestamp_to_default_tz_midnight(base_timestamp), base_datetime,
        )

    def test_rounding_to_same_date(self):
        base_timestamp = parse_datetime('2018-01-01T00:00:00+03').timestamp()
        base_datetime = make_aware(datetime.datetime(2018, 1, 1))
        hour = 3600
        self.assertEqual(
            round_timestamp_to_default_tz_midnight(base_timestamp + hour),
            base_datetime,
        )
        self.assertEqual(
            round_timestamp_to_default_tz_midnight(base_timestamp - hour),
            base_datetime,
        )
        self.assertEqual(
            round_timestamp_to_default_tz_midnight(base_timestamp + 11 * hour),
            base_datetime,
        )
        self.assertEqual(
            round_timestamp_to_default_tz_midnight(base_timestamp - 11 * hour),
            base_datetime,
        )

    def test_rounding_to_next_date(self):
        base_timestamp = parse_datetime('2018-01-01T00:00:00+03').timestamp()
        base_datetime = make_aware(datetime.datetime(2018, 1, 1))
        hour = 3600
        self.assertEqual(
            round_timestamp_to_default_tz_midnight(base_timestamp + 13 * hour),
            base_datetime + datetime.timedelta(days=1),
        )

    def test_rounding_to_prev_date(self):
        base_timestamp = parse_datetime('2018-01-01T00:00:00+03').timestamp()
        base_datetime = make_aware(datetime.datetime(2018, 1, 1))
        hour = 3600
        self.assertEqual(
            round_timestamp_to_default_tz_midnight(base_timestamp - 13 * hour),
            base_datetime - datetime.timedelta(days=1),
        )

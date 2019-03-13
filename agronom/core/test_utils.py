import datetime
import random
import sys
from unittest import mock

from django.db.models import QuerySet


def generate_random_phone():
    return '+7' + str(random.randrange(1, 10 ** 10 + 1)).zfill(10)


real_datetime_class = datetime.datetime


def mock_datetime(target, datetime_module):
    class DatetimeSubclassMeta(type):
        @classmethod
        def __instancecheck__(mcs, obj):
            return isinstance(obj, real_datetime_class)

    class BaseMockedDatetime(real_datetime_class):
        @classmethod
        def now(cls, tz=None):
            return target.replace(tzinfo=tz)

        @classmethod
        def utcnow(cls):
            return target

        @classmethod
        def today(cls):
            return target

    # Python2 & Python3-compatible metaclass
    MockedDatetime = DatetimeSubclassMeta('datetime', (BaseMockedDatetime,), {})

    return mock.patch.object(datetime_module, 'datetime', MockedDatetime)


def check_equal(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)


class MockQuery(QuerySet):
    """
    Saves all filter parameters to _args property.
    """
    def __init__(self, **kwargs):
        super(MockQuery, self).__init__(**kwargs)
        self._args = {}

    def filter(self, **kwargs):
        self._args.update(kwargs)
        return super(MockQuery, self).filter(**kwargs)

    def _clone(self):
        clone = super(MockQuery, self)._clone()
        clone._args = self._args.copy()
        return clone


class MockResponse:
    """
    Mock for Response from requests library.
    """

    def __init__(self, status_code, json_):
        self.status_code = status_code
        self.json_ = json_

    def json(self):
        return self.json_


def should_be_mocked_in_test_mode(celery_task):
    """
    Decorate celery tasks with this function to prevent calling
    .delay and .apply_async in test mode.
    :param celery_task:
    :return:
    """
    test_mode = len(sys.argv) >= 2 and sys.argv[1] == 'test'
    if not test_mode:
        return celery_task

    def should_not_be_mocked(*args, **kwargs):
        assert False, f'Task {celery_task} should be mocked in test mode'

    celery_task.delay = should_not_be_mocked
    celery_task.apply_async = should_not_be_mocked
    return celery_task


def patch_delay(celery_task):
    """
    Patch celery task delay method to do nothing (useful for manually calling tasks in tests).
    :param celery_task: celery task to be patched
    :return: patched object (use it in with statement)
    """
    return mock.patch.object(
        celery_task, 'delay', side_effect=lambda *args, **kwargs: None,
    )


class CallDelayedTaskAfter:
    """
    Mocks celery .delay method to do nothing, calls delayed task directly
    after code executed in ``with`` statement
    """

    def __init__(self, celery_task):
        self.celery_task = celery_task
        self.ctx_manager = mock.patch.object(
            celery_task, 'delay', side_effect=lambda *args, **kwargs: None,
        )

    def __enter__(self):
        self.mocked = self.ctx_manager.__enter__()
        return self.mocked

    def __exit__(self, *exc_info):
        retval = self.ctx_manager.__exit__(*exc_info)
        self.mocked.assert_called_once()
        self.celery_task.apply(*self.mocked.call_args)
        return retval


class CeleryTaskNotDelayed:
    """
    Asserts that given celery task in not launched with .delay
    """
    def __init__(self, celery_task):
        self.ctx_manager = mock.patch.object(
            celery_task, 'delay', side_effect=lambda *args, **kwargs: None,
        )

    def __enter__(self):
        self.mocked = self.ctx_manager.__enter__()
        return self.mocked

    def __exit__(self, *exc_info):
        retval = self.ctx_manager.__exit__(*exc_info)
        self.mocked.assert_not_called()
        return retval


def patch_apply_async(celery_task):
    """
    Patch celery task apply_async method to do nothing (useful for manually calling tasks in tests).
    :param celery_task: celery task to be patched
    :return: patched object (use it in with statement)
    """
    return mock.patch.object(
        celery_task, 'apply_async', side_effect=lambda *args, **kwargs: None,
    )

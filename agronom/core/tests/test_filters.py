from unittest import TestCase

from django.db import models

from django_filters import rest_framework as filters

from ..filters import NullableCharFilter
from ..test_utils import MockQuery


class TestNullableCharFilter(TestCase):

    class TestModel(models.Model):
        text = models.CharField(max_length=100)

        class Meta:
            abstract = True

    class TestFilter(filters.FilterSet):
        text = NullableCharFilter(field_name='text', lookup_expr='contains')

    def test_not_null_arg(self):
        query = MockQuery(model=self.TestModel)
        filtered = self.TestFilter(
            {'text': 'hello world'},
            query,
        )
        self.assertEqual(
            filtered.qs._args,
            {
                'text__contains': 'hello world',
            }
        )

    def test_null_arg(self):
        query = MockQuery(model=self.TestModel)
        filtered = self.TestFilter(
            {'text': 'NULL'},
            query,
        )
        self.assertEqual(
            filtered.qs._args,
            {
                'text__isnull': True,
            }
        )

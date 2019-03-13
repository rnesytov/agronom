from django_filters import filters


class NullableCharFilter(filters.CharFilter):
    empty_value = 'NULL'

    def filter(self, qs, value):
        if value != self.empty_value:
            return super(NullableCharFilter, self).filter(qs, value)

        qs = self.get_method(qs)(**{(self.field_name + '__isnull'): True})
        return qs.distinct() if self.distinct else qs

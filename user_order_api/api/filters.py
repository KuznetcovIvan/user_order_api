import django_filters
from orders.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFilter(django_filters.FilterSet):
    age = django_filters.NumberFilter(method='filter_by_age')
    age_range = django_filters.NumericRangeFilter(method='filter_by_age_range')
    birth_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = User
        fields = ('age', 'age_range', 'birth_date')

    def filter_by_age(self, users, name, value):
        return users.filter(age=value)

    def filter_by_age_range(self, users, name, value):
        if value.start is not None:
            users = users.filter(age__gte=value.start)
        if value.stop is not None:
            users = users.filter(age__lte=value.stop)
        return users


class OrderFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name='user__username', lookup_expr='exact'
    )
    email = django_filters.CharFilter(
        field_name='user__email', lookup_expr='icontains'
    )
    created_at = django_filters.DateFromToRangeFilter()
    updated_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Order
        fields = ('username', 'email', 'created_at', 'updated_at')

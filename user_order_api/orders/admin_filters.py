from django.contrib.admin import SimpleListFilter
from .models import User
from django.db.models import Q, Count


class AgeGroupFilter(SimpleListFilter):
    title = 'Возраст'
    parameter_name = 'age_group'
    LOOKUPS = (
        ('not specified', 'Не задан'),
        ('<18', 'До 18'),
        ('18-25', '18–25'),
        ('26-35', '26–35'),
        ('36-50', '36–50'),
        ('50+', '50+')
    )

    def lookups(self, request, model_admin):
        return self.LOOKUPS

    def queryset(self, request, queryset):
        age_filters = {
            '<18': Q(age__lt=18),
            '18-25': Q(age__gte=18, age__lte=25),
            '26-35': Q(age__gte=26, age__lte=35),
            '36-50': Q(age__gte=36, age__lte=50),
            '50+': Q(age__gt=50),
            'not specified': Q(birth_date__isnull=True),
        }
        condition = age_filters.get(self.value())
        return (
            queryset.annotate(age=User.calculate_age_expression())
            .filter(condition) if condition else queryset
        )


class OrdersCountFilter(SimpleListFilter):
    title = 'Количество заказов'
    parameter_name = 'orders_count'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.few = None
        self.medium = None
        self.ranges = None

    def set_ranges(self):
        unique_counts = set(User.objects.annotate(count=Count('orders'))
                                .values_list('count', flat=True))

        if len(unique_counts) < 3:
            self.ranges = None
            return

        max_count = max(unique_counts)
        self.few = max_count // 3
        self.medium = (2 * max_count) // 3
        self.ranges = {
            'none': (0, 0),
            'few': (1, self.few),
            'medium': (self.few + 1, self.medium),
            'many': (self.medium + 1, max_count),
        }

    def filter_by_range(self, key, users=None):
        if key not in self.ranges:
            return User.objects.none()

        users = users or User.objects.all()
        low, high = self.ranges[key]
        return users.annotate(count=Count('orders'))\
            .filter(count__range=(low, high))

    def lookups(self, request, model_admin):
        self.set_ranges()
        if not self.ranges:
            return []
        return [
            (
                'none',
                f'Нет заказов '
                f'({self.filter_by_range("none").count()})'
            ),
            (
                'few',
                f'Мало (1–{self.few}) '
                f'({self.filter_by_range("few").count()})'
            ),
            (
                'medium',
                f'Средне ({self.few + 1}–{self.medium}) '
                f'({self.filter_by_range("medium").count()})'
            ),
            (
                'many',
                f'Много ({self.medium + 1}+) '
                f'({self.filter_by_range("many").count()})'
            )
        ]

    def queryset(self, request, users):
        self.set_ranges()
        if not self.value() or not self.ranges:
            return users

        return self.filter_by_range(self.value(), users)

from django.conf import settings
from django.contrib.admin import (ModelAdmin, TabularInline, display, register,
                                  site)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from .models import User, Order
from .admin_filters import AgeGroupFilter, OrdersCountFilter

site.site_header = f'Администрирование {settings.PROJECT_NAME}'
site.site_title = f'{settings.PROJECT_NAME} Администрирование'
site.index_title = (
    f'Добро пожаловать в панель управления {settings.PROJECT_NAME}'
)
site.empty_value_display = 'Не задано'

site.unregister(Group)


@register(User)
class ExtendedUserAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'email', 'birth_date', 'age', 'date_joined',
        'orders_count'
    )

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .annotate(age=User.calculate_age_expression())
        )

    @display(description='Возраст')
    def age(self, obj):
        return obj.age

    @display(description='Число заказов')
    def orders_count(self, obj):
        return obj.orders.count()

    search_fields = ('email', 'username')
    list_filter = (AgeGroupFilter, OrdersCountFilter)

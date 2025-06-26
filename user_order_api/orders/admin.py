from django.conf import settings
from django.contrib.admin import ModelAdmin, display, register, site
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .admin_filters import AgeGroupFilter, OrdersCountFilter
from .models import Order, User

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
    list_display_links = list_display
    fieldsets = (
        ('Основная информация', {
            'fields': ('username', 'password')
        }),
        ('Персональные данные', {
            'fields': ('email', 'birth_date')
        }),
        ('Права доступа', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'user_permissions'
            )
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'birth_date')}),
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
    list_filter = (AgeGroupFilter, OrdersCountFilter, 'date_joined')


@register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        'id', 'title', 'description', 'user', 'created_at', 'updated_at'
    )
    list_display_links = list_display
    search_fields = ('id', 'title', 'description', 'user__username',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('user',)

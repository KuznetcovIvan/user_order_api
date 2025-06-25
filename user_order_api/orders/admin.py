from django.conf import settings
from django.contrib.admin import (ModelAdmin, TabularInline, display, register,
                                  site)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

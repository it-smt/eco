from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'last_name', 'first_name',
              'middle_name', ('email', 'is_email_confirmed'), 'number', 'status', 'is_staff', 'is_active', 'date_joined', 'password')
    readonly_fields = ('status', 'date_joined', 'password')
    list_display = ('username', 'last_name', 'first_name',
                    'email', 'is_email_confirmed', 'number', 'status')
    list_filter = ('username', 'last_name', 'first_name',
                   'email', 'is_email_confirmed', 'number', 'status')
    ordering = ('username',)


admin.site.unregister(Group)

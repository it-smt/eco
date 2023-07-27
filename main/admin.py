from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Класс представления модели Message в админ панели."""
    list_display = ('author', 'type', 'weight', 'worker',
                    'is_complited', 'submitted')
    list_filter = ('author', 'type', 'weight', 'worker',
                   'is_complited', 'submitted')
    ordering = ('author', 'submitted')


admin.site.site_title = 'Чистый Мир'
admin.site.site_header = 'Чистый Мир'

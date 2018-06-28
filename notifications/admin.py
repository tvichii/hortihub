from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('verb',)


admin.site.register(Notification, NotificationAdmin)


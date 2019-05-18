from django.contrib import admin

from .models import Tasks


@admin.register(Tasks)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'params', 'received_t', 'status')
    list_filter = ('endpoint', 'error_type', 'status', 'email', 'received_t', 'start_t', 'end_t')

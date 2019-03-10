from django.contrib import admin

from .models import Tasks


@admin.register(Tasks)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ('id', 'status', 'email', 'received_t', 'start_t', 'end_t')

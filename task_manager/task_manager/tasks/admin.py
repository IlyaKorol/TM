from django.contrib import admin
from .models import Task, FavoriteTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'due_date', 'completed')
    list_filter = ('priority', 'due_date', 'completed')
    search_fields = ('title', 'description')

@admin.register(FavoriteTask)
class FavoriteTaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'task')
    list_filter = ('user', 'task')
    search_fields = ('user__username', 'task__title')
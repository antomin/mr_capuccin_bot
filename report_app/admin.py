from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder

from report_app.models import Task
from tgbot_app.models import WorkSession


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ('task_type', 'is_completed', 'completed_at', 'preview', 'work_session')
    list_filter = (("created_at", DateRangeFilterBuilder()), 'work_session__store', 'work_session__worker',
                   'is_completed')
    list_display = ('task_type', 'is_completed', 'get_worker', 'get_store', 'created_at')
    readonly_fields = ('task_type', 'is_completed', 'work_session', 'completed_at', 'preview')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(WorkSession)
class WorkSessionAdmin(admin.ModelAdmin):
    pass

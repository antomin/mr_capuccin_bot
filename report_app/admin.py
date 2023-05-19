from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder

from report_app.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    exclude = ('img_hash', 'out_of_time')
    list_filter = (("created_at", DateRangeFilterBuilder()), 'work_session__store', 'work_session__worker',
                   'is_completed')
    list_display = ('task_type', 'is_completed', 'get_worker', 'get_store', 'created_at')
    readonly_fields = ('task_type', 'img_confirmation', 'is_completed', 'work_session', 'completed_at')


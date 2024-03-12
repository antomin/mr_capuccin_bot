from django.contrib import admin
from django.contrib.auth.models import Group
from django.conf import settings

from .models import AdminReport, Store, TaskType, Worker


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    fields = ('title', 'morning_time', 'midday_time', 'close_time', 'task_types')
    filter_horizontal = ('task_types', )


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_exec', 'need_confirmation')
    list_filter = ('time_exec', )


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tgid')


@admin.register(AdminReport)
class AdminReportAdmin(admin.ModelAdmin):
    list_display = ('tgid', 'comment')


admin.site.site_title = settings.SITE_NAME
admin.site.site_header = settings.SITE_NAME
admin.site.site_url = None
admin.site.unregister(Group)

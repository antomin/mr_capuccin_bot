from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Store, TaskType, Worker


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


admin.site.site_title = 'Mr.Capuccin'
admin.site.site_header = 'Mr.Capuccin'
admin.site.site_url = None
admin.site.unregister(Group)

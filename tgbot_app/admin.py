from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Store, TaskType, Worker


class TaskTypeInline(admin.TabularInline):
    model = Store.task_types.through


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    inlines = (TaskTypeInline, )
    exclude = ('tasks', )


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

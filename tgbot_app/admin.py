from django.contrib import admin
from .models import Store, Worker, TaskType


class TaskTypeInline(admin.TabularInline):
    model = Store.tasks.through


class StoreAdmin(admin.ModelAdmin):
    inlines = (TaskTypeInline, )
    exclude = ('tasks', )


class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_exec')
    list_filter = ('time_exec', )



admin.site.register(Store, StoreAdmin)
admin.site.register(Worker)
admin.site.register(TaskType, TaskTypeAdmin)

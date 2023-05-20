from asgiref.sync import sync_to_async
from django.db import models
from django.utils.safestring import mark_safe

from tgbot_app.models import Store, TaskType, WorkSession


class DailyReport(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    is_perfect = models.BooleanField(default=True)
    unfulfilled_tasks = models.TextField(blank=True)
    tasks_cnt = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)


class Task(models.Model):
    task_type = models.ForeignKey(TaskType, verbose_name='задача', on_delete=models.SET_NULL, null=True)
    img_confirmation = models.ImageField(verbose_name='фото подтверждение', upload_to='confirmations/')
    img_hash = models.CharField(verbose_name='хеш подтверждения', max_length=100, null=True)
    is_completed = models.BooleanField(verbose_name='выполнена', default=False)
    out_of_time = models.BooleanField(verbose_name='доступно для выполнения', default=False)
    work_session = models.ForeignKey(WorkSession, verbose_name='смена', on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    completed_at = models.DateTimeField(verbose_name='время выполнения', null=True)

    def get_worker(self):
        return self.work_session.worker

    def get_store(self):
        return self.work_session.store

    def preview(self):
        return mark_safe(f'<a href="{self.img_confirmation.url}"><img src="{self.img_confirmation.url}"'
                         f'style="max-height: 300px;"></a>')

    @sync_to_async
    def get_title(self):
        return self.task_type.title

    def __str__(self):
        return f'{self.task_type.title} | {self.work_session.worker}'

    get_worker.short_description = "сотрудник"
    get_store.short_description = "торговая точка"
    preview.short_description = 'подтверждение'

    class Meta:
        verbose_name = 'задание'
        verbose_name_plural = 'задания'

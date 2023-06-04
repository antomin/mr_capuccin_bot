from asgiref.sync import sync_to_async
from django.db import models


class TaskType(models.Model):
    __TIME_EXEC = (
        ('morning', 'утро'),
        ('midday', 'обед'),
        ('evening', 'вечер'),
        ('all_day', 'весь день'),
    )

    title = models.CharField(verbose_name='название', max_length=255)
    need_confirmation = models.BooleanField(verbose_name='фото подтверждение')
    time_exec = models.CharField(verbose_name='время выполнения', choices=__TIME_EXEC, max_length=10)
    created_at = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='время обновления', auto_now=True)

    def __str__(self):
        return f'{self.title} ({self.get_time_exec_display()})'

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'


class Store(models.Model):
    title = models.CharField(verbose_name='название', max_length=50)
    task_types = models.ManyToManyField(TaskType, verbose_name='задачи')
    morning_time = models.TimeField(verbose_name='крайнее время для утренних задач')
    midday_time = models.TimeField(verbose_name='крайнее время для дневных задач')
    close_time = models.TimeField(verbose_name='время закрытия торговой точки')
    created_at = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='время обновления', auto_now=True)

    def __str__(self):
        return self.title

    @sync_to_async
    def get_time_exec(self, time_exec):
        time_exec_dict = {'morning': self.morning_time, 'midday': self.midday_time, 'evening': self.close_time}
        return time_exec_dict[time_exec]

    class Meta:
        verbose_name = 'торговая точка'
        verbose_name_plural = 'торговые точки'


class Worker(models.Model):
    tgid = models.BigIntegerField(verbose_name='телеграм ID', primary_key=True)
    first_name = models.CharField(verbose_name='имя', max_length=20)
    last_name = models.CharField(verbose_name='фамилия', max_length=20)
    created_at = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='время обновления', auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'


class WorkSession(models.Model):
    is_open = models.BooleanField(verbose_name='открыта', default=True)
    open_time = models.DateTimeField(verbose_name='начало смена', auto_now_add=True)
    close_time = models.DateTimeField(verbose_name='окончание смены', null=True)
    worker = models.ForeignKey(Worker, verbose_name='сотрудник', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, verbose_name='торговая точка', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='комментарии', blank=True)

    @sync_to_async
    def get_worker_id(self):
        return self.worker.tgid

    def __str__(self):
        return f'{self.open_time.strftime("%d.%m.%Y")} | {self.worker} | {self.store}'

    class Meta:
        verbose_name = 'смена'
        verbose_name_plural = 'смены'


class AdminReport(models.Model):
    tgid = models.BigIntegerField(verbose_name='телеграм ID', primary_key=True)
    comment = models.CharField(verbose_name='комментарий', max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.tgid)

    class Meta:
        verbose_name = 'администратор'
        verbose_name_plural = 'администраторы'

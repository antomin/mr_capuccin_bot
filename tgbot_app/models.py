from django.db import models


class TaskType(models.Model):
    __TIME_EXEC = (
        ('morning', 'утро'),
        ('midday', 'обед'),
        ('evening', 'вечер'),
        ('all_day', 'весь день'),
    )

    title = models.CharField(verbose_name='название', max_length=50)
    need_confirmation = models.BooleanField(verbose_name='подтверждение')
    time_exec = models.CharField(verbose_name='время выполнения', choices=__TIME_EXEC, max_length=10)
    created_at = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='время обновления', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'


class Store(models.Model):
    title = models.CharField(verbose_name='название', max_length=50)
    tasks = models.ManyToManyField(TaskType, verbose_name='задачи')
    created_at = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='время обновления', auto_now=True)

    def __str__(self):
        return self.title

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
    open_time = models.DateTimeField(verbose_name='начало смена', auto_now_add=True)
    close_time = models.DateTimeField(verbose_name='окончание смены', null=True)
    worker = models.ForeignKey(Worker, verbose_name='сотрудник', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, verbose_name='торговая точка', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='комментарии', blank=True)

    def __str__(self):
        return f'{self.start_time.strftime("%d.%m.%Y")} | {self.worker} | {self.store}'

    class Meta:
        verbose_name = 'смена'
        verbose_name_plural = 'смены'


class Task(models.Model):
    img_confirmation = models.ImageField(verbose_name='фото-подтверждение', upload_to='confirmations/')
    img_hash = models.CharField(verbose_name='хеш подтверждения', max_length=100, null=True)
    is_completed = models.BooleanField(verbose_name='выполнена', default=False)
    work_session = models.ForeignKey(WorkSession, verbose_name='смена', on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    completed_at = models.DateTimeField(verbose_name='время выполнения', null=True)

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    tgid = models.BigIntegerField(verbose_name='телеграм ID', null=True)
    recv_reports = models.BooleanField(verbose_name='получать отчёты', default=False)

# Generated by Django 4.2.1 on 2023-05-16 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='recv_reports',
            field=models.BooleanField(default=False, verbose_name='получать отчёты'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='tgid',
            field=models.BigIntegerField(null=True, verbose_name='телеграм ID'),
        ),
    ]

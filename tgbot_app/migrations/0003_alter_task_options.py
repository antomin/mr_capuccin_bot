# Generated by Django 4.2.1 on 2023-05-17 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot_app', '0002_alter_task_options_task_task_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': 'задание', 'verbose_name_plural': 'задания'},
        ),
    ]

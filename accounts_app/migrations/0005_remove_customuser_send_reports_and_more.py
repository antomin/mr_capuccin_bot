# Generated by Django 4.2.1 on 2023-05-19 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0004_customuser_send_reports_customuser_tgid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='send_reports',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='tgid',
        ),
    ]

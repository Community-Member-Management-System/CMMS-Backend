# Generated by Django 3.1 on 2020-09-05 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0003_auto_20200831_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='mail',
            field=models.BooleanField(default=False, verbose_name='是否发送邮件通知'),
        ),
    ]

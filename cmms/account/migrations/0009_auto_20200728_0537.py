# Generated by Django 3.0.5 on 2020-07-28 05:37

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20200713_0955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar_url',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.FileField(blank=True, upload_to=account.models.user_avatar_path, verbose_name='头像'),
        ),
    ]
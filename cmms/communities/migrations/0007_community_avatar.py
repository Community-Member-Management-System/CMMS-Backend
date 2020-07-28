# Generated by Django 3.0.5 on 2020-07-28 06:01

import communities.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0006_invitation'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=communities.models.community_avatar_path, verbose_name='头像'),
        ),
    ]

# Generated by Django 3.0.7 on 2020-08-05 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0007_community_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='checklist',
            field=models.JSONField(default=dict, verbose_name='待办清单 JSON'),
        ),
    ]

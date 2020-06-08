# Generated by Django 3.0.6 on 2020-06-08 02:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communities', '0002_auto_20200526_0627'),
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='related_community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='communities.Community', verbose_name='关联社团'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='related_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关联用户'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='subtype',
            field=models.IntegerField(blank=True, null=True, verbose_name='通知子类型'),
        ),
    ]

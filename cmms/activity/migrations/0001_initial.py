# Generated by Django 3.0.6 on 2020-06-09 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communities', '0002_auto_20200526_0627'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('location', models.TextField(verbose_name='活动地点')),
                ('title', models.TextField(verbose_name='活动标题')),
                ('description', models.TextField(verbose_name='活动提要')),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('end_time', models.DateTimeField(verbose_name='结束时间')),
                ('related_community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='communities.Community', verbose_name='关联社团')),
                ('signed_in_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='签到成员')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='评论时间')),
                ('title', models.TextField(verbose_name='评论标题')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('related_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.Activity', verbose_name='关联活动')),
                ('related_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
        ),
    ]
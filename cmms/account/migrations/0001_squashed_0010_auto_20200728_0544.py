# Generated by Django 3.0.7 on 2020-08-05 04:16

import account.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('account', '0001_initial'), ('account', '0002_user_is_staff'), ('account', '0003_auto_20200501_1155'), ('account', '0004_auto_20200507_1451'), ('account', '0005_auto_20200507_1504'), ('account', '0006_auto_20200507_1504'), ('account', '0007_delete_visibility'), ('account', '0008_auto_20200713_0955'), ('account', '0009_auto_20200728_0537'), ('account', '0010_auto_20200728_0544')]

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('gid', models.CharField(max_length=16, unique=True, verbose_name='GID')),
                ('student_id', models.CharField(max_length=10, unique=True, verbose_name='学号')),
                ('real_name', models.CharField(max_length=16, verbose_name='真实姓名')),
                ('nick_name', models.CharField(max_length=64, verbose_name='昵称')),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=32, verbose_name='手机号')),
                ('profile', models.TextField(blank=True, verbose_name='个人简介')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='注册时间')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='上次登录时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('is_staff', models.BooleanField(default=False, help_text='对 admin/ 管理页的只读权限', verbose_name='staff status')),
                ('id', models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to=account.models.user_avatar_path, verbose_name='头像')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
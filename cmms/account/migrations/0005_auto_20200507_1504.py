# Generated by Django 3.0.5 on 2020-05-07 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200507_1451'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='actual_name',
            new_name='real_name',
        ),
        migrations.CreateModel(
            name='Visibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_name', models.CharField(choices=[('0', '公开'), ('1', '仅社团成员可见'), ('2', '仅管理员可见')], max_length=1)),
                ('student_id', models.CharField(choices=[('0', '公开'), ('1', '仅社团成员可见'), ('2', '仅管理员可见')], max_length=1)),
                ('email', models.CharField(choices=[('0', '公开'), ('1', '仅社团成员可见'), ('2', '仅管理员可见')], max_length=1)),
                ('phone', models.CharField(choices=[('0', '公开'), ('1', '仅社团成员可见'), ('2', '仅管理员可见')], max_length=1)),
                ('profile', models.CharField(choices=[('0', '公开'), ('1', '仅社团成员可见'), ('2', '仅管理员可见')], max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

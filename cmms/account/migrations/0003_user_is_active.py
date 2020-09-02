# Generated by Django 3.1 on 2020-09-02 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200805_0438'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='是否为有效用户。去除选择以冻结用户。', verbose_name='是否有效'),
        ),
    ]

# Generated by Django 3.0.6 on 2020-07-08 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
        ('notice', '0003_notice_related_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='related_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activity.Comment', verbose_name='关联评论'),
        ),
    ]

# Generated by Django 3.1 on 2020-08-31 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_activity_secret_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True, verbose_name='纬度'),
        ),
        migrations.AddField(
            model_name='activity',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True, verbose_name='经度'),
        ),
    ]

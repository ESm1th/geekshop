# Generated by Django 2.1.4 on 2018-12-11 11:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20181211_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(default=21, verbose_name='age'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 13, 11, 54, 16, 895262, tzinfo=utc)),
        ),
    ]

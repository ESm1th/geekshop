# Generated by Django 2.1.4 on 2018-12-13 16:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20181213_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 15, 16, 29, 26, 574927, tzinfo=utc)),
        ),
    ]

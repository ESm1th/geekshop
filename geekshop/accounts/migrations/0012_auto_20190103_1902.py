# Generated by Django 2.1.4 on 2019-01-03 16:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20181227_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 5, 16, 2, 21, 616318, tzinfo=utc)),
        ),
    ]

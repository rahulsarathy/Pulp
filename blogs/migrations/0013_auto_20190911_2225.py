# Generated by Django 2.2.3 on 2019-09-11 22:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0012_auto_20190911_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='date_subscribed',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 11, 22, 25, 48, 103521, tzinfo=utc), verbose_name='Date Subscribed'),
        ),
    ]

# Generated by Django 2.2.5 on 2019-10-07 00:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0020_auto_20190921_0532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='date_subscribed',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 7, 0, 55, 16, 126431, tzinfo=utc), verbose_name='Date Subscribed'),
        ),
    ]
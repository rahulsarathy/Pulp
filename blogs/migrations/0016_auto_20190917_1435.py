# Generated by Django 2.2.5 on 2019-09-17 14:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0015_auto_20190915_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='date_subscribed',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 17, 14, 35, 27, 987391, tzinfo=utc), verbose_name='Date Subscribed'),
        ),
    ]

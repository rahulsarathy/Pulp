# Generated by Django 2.2.5 on 2019-09-17 22:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0017_auto_20190917_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='date_subscribed',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 17, 22, 57, 32, 699962, tzinfo=utc), verbose_name='Date Subscribed'),
        ),
    ]

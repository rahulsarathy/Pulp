# Generated by Django 2.2.5 on 2019-09-17 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_stripetoken'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StripeToken',
        ),
    ]

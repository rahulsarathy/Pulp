# Generated by Django 2.2.4 on 2019-08-13 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Blog Name'),
        ),
    ]
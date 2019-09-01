# Generated by Django 2.2.3 on 2019-08-29 03:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0005_auto_20190817_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='home_url',
            field=models.URLField(verbose_name='Home URL'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='rss_url',
            field=models.URLField(verbose_name='RSS URL'),
        ),
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('file_link', models.URLField(primary_key=True, serialize=False, verbose_name='S3 File Link')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogBlock',
            fields=[
                ('file_link', models.URLField(primary_key=True, serialize=False, verbose_name='S3 File Link')),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.Blog')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='magazine',
            field=models.ManyToManyField(to='blogs.Magazine'),
        ),
    ]
# Generated by Django 2.2.4 on 2019-08-12 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('title', models.CharField(max_length=100, verbose_name='Article Title')),
                ('permalink', models.CharField(max_length=500, primary_key=True, serialize=False, verbose_name='Permalink')),
                ('date_published', models.CharField(max_length=100, verbose_name='Date Published')),
                ('author', models.CharField(max_length=100, verbose_name='Author')),
                ('file_link', models.URLField(verbose_name='S3 File Link')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Blog Name')),
                ('last_polled_time', models.DateTimeField(max_length=8, verbose_name='Last Polled Time')),
                ('home_url', models.CharField(max_length=100, verbose_name='Home URL')),
                ('rss_url', models.CharField(max_length=100, verbose_name='RSS URL')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_subscribed', models.DateTimeField(verbose_name='Date Subscribed')),
                ('blog', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blogs.Blog')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100, verbose_name='Author')),
                ('content', models.CharField(max_length=100, verbose_name='Content')),
                ('date_published', models.CharField(max_length=8, verbose_name='Date Published')),
                ('parent_comment_id', models.IntegerField(default=None, verbose_name='Parent Comment ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.Article')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.Blog'),
        ),
    ]
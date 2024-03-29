# Generated by Django 2.2.7 on 2020-03-17 20:29

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InstapaperCredentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oauth_token', encrypted_model_fields.fields.EncryptedCharField(null=True, verbose_name='Password')),
                ('oauth_token_secret', encrypted_model_fields.fields.EncryptedCharField(null=True, verbose_name='Password')),
                ('last_polled', models.DateTimeField(default=None, null=True)),
                ('polled_bookmarks', django.contrib.postgres.fields.jsonb.JSONField(default=dict, null=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(_('Article Title'), max_length=255)
    permalink = models.URLField(_('Permalink'), primary_key=True, max_length=500)
    page_count = models.IntegerField(_('Number of Words'), default=None, null=True)
    mercury_response = JSONField()
    preview_text = models.CharField(_('Preview Text'), null=True, max_length=350)


class ReadingListItem(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, default=None, null=True)
    date_added = models.DateTimeField(_('Date Added'), default=timezone.now)
    archived = models.NullBooleanField(_('Archived'), default=False)
    trashed = models.NullBooleanField(_('Trashed'))
    delivered = models.NullBooleanField(_('Delivered'))
    to_deliver = models.BooleanField(_('Delivered'), default=False)

    class Meta:
        unique_together = (("reader", "article"),)
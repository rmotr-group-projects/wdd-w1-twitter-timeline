from django.db import models
from django.conf import settings


class Tweet(models.Model):
    class Meta:
        ordering = ['-created']

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)

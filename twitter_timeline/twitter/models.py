from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings


class Tweet(models.Model):
    # {
    #     "username": "jack",
    #     "content": "hello world!",
    #     "created": "2016-08-26T10:03:28"
    # }
    # tweet_info_json = models.CharField(max_length=1500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    content = models.CharField(max_length=140, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-created']


class User(AbstractUser):
    pass

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


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


class UserRelationship(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')


class User(AbstractUser):
    def follow(self, other_user):
        pass

    def unfollow(self, other_user):
        pass

    @property
    def all_following(self):
        pass

    @property
    def all_followers(self):
        pass

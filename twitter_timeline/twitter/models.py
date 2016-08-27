from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Tweet(models.Model):
    class Meta:
        ordering = ['-created']

    # {
    #     "username": "jack",
    #     "content": "hello world!",
    #     "created": "2016-08-26T10:03:28"
    # }
    # tweet_info_json = models.CharField(max_length=1500)

    # Shouldn't be seen by students
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    content = models.CharField(max_length=140, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


class Relationship(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')


class User(AbstractUser):

    def follow(self, twitter_profile):
        try:
            Relationship.objects.get(follower=self, following=twitter_profile)
        except Relationship.DoesNotExist:
            Relationship.objects.create(follower=self, following=twitter_profile)

    def unfollow(self, twitter_profile):
        try:
            rel = Relationship.objects.get(follower=self, following=twitter_profile)
        except Relationship.DoesNotExist:
            return
        rel.delete()

    def is_following(self, twitter_profile):
        return Relationship.objects.filter(
            follower=self, following=twitter_profile).exists()

    @property
    def following(self):
        return [rel.following for rel in Relationship.objects.filter(follower=self)]

    @property
    def followers(self):
        return [rel.following for rel in Relationship.objects.filter(following=self)]

    @property
    def count_following(self):
        return Relationship.objects.filter(follower=self).count()

    @property
    def count_followers(self):
        return Relationship.objects.filter(following=self).count()

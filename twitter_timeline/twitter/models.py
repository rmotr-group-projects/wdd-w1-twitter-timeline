from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Tweet(models.Model):
    class Meta:
        ordering = ['-created']

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)


class Relationship(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    
    
class User(AbstractUser):
    
    def is_following(self, twitter_profile):
        try:
            Relationship.objects.get(follower=self, following=twitter_profile)
        except Relationship.DoesNotExist:
            return False
        return True
        
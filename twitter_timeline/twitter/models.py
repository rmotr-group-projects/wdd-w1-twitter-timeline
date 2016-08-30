from django.db import models
from django.conf import settings
from django.contrib.auth import models as auth_models

class User(auth_models.AbstractUser):
    # our fields here

    
    # our methods here for test_timeline
    def follow(self, other):
        """
        Creates a following relationship with another user.
        """
        # Create the relationship
        Relationship.objects.create(
            follower = self,
            following = other
        )
        
    def unfollow(self, other):
        """
        Removes a following relationship with another user.
        """
        # Delete the relationship, if it exists (will raise exception otherwise)
        Relationship.objects.get(
            follower = self,
            following = other
            ).delete()
    
    @property
    def count_followers(self):
        """
        Returns the number of followers this user has.
        """
        return Relationship.objects.filter(following=self).count()
        
    @property
    def count_following(self):
        """
        Returns the number of users a user is following.
        """
        return Relationship.objects.filter(follower=self).count()
    
    def is_following(self, other):
        """
        Checks to see if a user is following another user.
        """
        return Relationship.objects.filter(follower = self, following = other).count() > 0
    
    
class Relationship(models.Model):
    # our fields here
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_user')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_user')
    
    class Meta:
        unique_together = (('follower', 'following'),)


class Tweet(models.Model):
    # {
    #     "username": "jack",
    #     "content": "hello world!",
    #     "created": "2016-08-26T10:03:28"
    # }
    
    ## Old field
    # tweet_info_json = models.CharField(max_length=1500)
    
    ## New fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']

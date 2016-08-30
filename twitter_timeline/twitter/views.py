from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import IntegrityError
from django.contrib import messages

from .models import Tweet, Relationship, User


@login_required()
def logout(request):
    django_logout(request)
    return redirect('/')


@login_required()
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if tweet.user != request.user:
        raise PermissionDenied
    tweet.delete()
    messages.success(request, 'Tweet successfully deleted')
    return redirect(request.GET.get('next', '/'))


@login_required()
def create_tweet(request):
    Tweet.objects.create(user=request.user, content=request.POST['content'])
    return redirect(request.GET.get('next', '/'))


@login_required()
def index(request, username=None):
    '''
    Displays the authenticated user's timeline
    '''
    # All relationships where the authenticated user is the follower
    relationships = Relationship.objects.filter(follower=request.user)
    
    # A set containing the authenticated user and every user he is following
    following = {relationship.following for relationship in relationships}
    following.add(request.user)
    
    # Every tweet written by someone the authenticated user is following, or
    #  by the user
    feed_tweets = Tweet.objects.filter(user__in=following)
    
    context = {
        "all_tweets": feed_tweets
    }
    
    return render(request, "twitter/feed.html", context)

@login_required()
def profile(request, username):
    '''
    Displays a user's feed 
    '''
    # The user whose profile page was requested
    feed_user = get_object_or_404(User, username=username)
    
    # True if the authenticated user is following the user whose profile
    #  was requested
    is_following = Relationship.objects.filter(
        follower=request.user, following=feed_user
        ).count() > 0
    
    # Red button to unfollow the user & blue button to follow the user
    btn_type = 'btn-danger' if is_following else 'btn-info'
    
    # All tweets by the user whose profile page was requested
    tweets = Tweet.objects.filter(user=feed_user)
    
    context = {
        'feed_user': username,
        'is_following': is_following,
        'btn_type': btn_type,
        'all_tweets': tweets,
    }
    
    return render(request, "twitter/feed.html", context)

@login_required()
def follow(request):
    """
    Creates a following relationship between the authenticated user and
    another user.
    """
    # Query for the user to be followed
    other_user = get_object_or_404(User, username=request.POST['username'])
    
    # Create the relationship
    try:
        Relationship.objects.create(
            follower=request.user, following=other_user
        )
    except IntegrityError:
        pass
    
    return redirect(request.GET.get('next', '/'))

@login_required()
def unfollow(request):
    """
    Deletes an existing following relationship between the authenticated
    user and another user.  Raises an error if the relationship does not
    exist.
    """
    # Query for the user to be unfollowed
    other_user = get_object_or_404(User, username=request.POST['username'])
    
    # Delete the relationship
    Relationship.objects.filter(
        follower=request.user, following=other_user
    ).delete()
    
    return redirect(request.GET.get('next', '/'))
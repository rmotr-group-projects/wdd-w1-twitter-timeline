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

# def login(request):
#     print("init")
#     return render(request, "twitter/login.html")
def other_index(request):
    # All relationships where the authenticated user is the follower
    relationships = Relationship.objects.filter(follower=request.user)
    
    # A list of every user the authenticated user is following
    following = [relationship.following for relationship in relationships]
    
    # Every tweet written by someone the authenticated user is following
    feed_tweets = Tweet.objects.filter(user__in=following)
    context = {
        "all_tweets": feed_tweets,
    }
    return render(request, "twitter/feed.html", context)

def index(request):
    current_user = User.objects.all()
    print(current_user)
    try:
        # Fetch id for user that belongs to current logged in user
        current_user = User.objects.get(username=str(request.user))
        # print(request.user)
        # # Find out which users the logged in user is following
        currently_following = Relationship.objects.filter(follower=current_user.id)
        # currently_following = Relationship.objects.filter(follower=request.user)
        # print currently_following
        # Fetch
        context = {
            "all_tweets": Tweet.objects.filter(user=current_user.id)
            #"all_tweets": None
        }
    except ObjectDoesNotExist:
        raise PermissionDenied
    return render(request, "twitter/feed.html", context)#HttpResponse(currently_following)

@require_POST()
def follow(request):
    """
    Creates a following relationship between the authenticated user and
    another user.
    """
    # Query for the user to be followed. That user will be passed to the template.
    other_user = User.objects.get(username=request.POST.username)
    
    # Query for tweets to be displayed
    tweets = Tweet.objects.filter(user=other_user)
    
    # Create the relationship
    try:
        Relationship.objects.create(
            follower=request.user, following=other_user
        )
    except IntegrityError:
        pass
    
    # Return to the feed page of the user who was followed
    return render(request, "twitter/feed.html", {'feed_user': other_user})

@require_POST()
def unfollow(request):
    """
    Deletes an existing following relationship between the authenticated
    user and another user.  Raises an error if the relationship does not
    exist.
    """
    # Query for the user to be unfollowed. That user will be passed to the template.
    other_user = User.objects.get(username=request.POST.username)
    
    # Query for tweets to be displayed
    tweets = Tweet.objects.filter(user=other_user)
    
    # Delete the relationship
    Relationship.objects.filter(
        follower=request.user, following=other_user
    ).delete()
    
    return render(request, "twitter/feed.html", {'feed_user': other_user})
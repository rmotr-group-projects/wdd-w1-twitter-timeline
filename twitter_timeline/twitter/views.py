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
def other_index(request, username=None):
    
    # context = {}
    
    # if username:
    #     # The user whose profile page was requested
    #     feed_user = get_object_or_404(User, username=username)
        
    #     # True if the authenticated user is following the user whose profile
    #     #  was requested
    #     followed = Relationship.objects.filter(
    #         follower=request.user, following=username
    #         ).count() > 0
        
    #     # All tweets by the user whose profile page was requested
    #     tweets = Tweet.objects.filter(user=feed_user)
        
    #     context = {
    #         'feed_user': feed_user,
    #         'followed': followed,
    #         'all_tweets': tweets,
    #     }
    #     print("INIT" + context['feed_user'])
    # else:
    # All relationships where the authenticated user is the follower
    relationships = Relationship.objects.filter(follower=request.user)
    
    # A list of every user the authenticated user is following
    following = [relationship.following for relationship in relationships]
    
    # Every tweet written by someone the authenticated user is following
    feed_tweets = Tweet.objects.filter(user__in=following)
    
    context = {
        "all_tweets": feed_tweets
    }
    
    return render(request, "twitter/feed.html", context)

@login_required()
def profile(request, username):
    # The user whose profile page was requested
    feed_user = get_object_or_404(User, username=username)
    
    # True if the authenticated user is following the user whose profile
    #  was requested
    is_following = Relationship.objects.filter(
        follower=request.user, following=feed_user
        ).count() > 0
    
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

# def index(request):
#     current_user = User.objects.all()
#     print(current_user)
#     try:
#         # Fetch id for user that belongs to current logged in user
#         current_user = User.objects.get(username=str(request.user))
#         # print(request.user)
#         # # Find out which users the logged in user is following
#         currently_following = Relationship.objects.filter(follower=current_user.id)
#         # currently_following = Relationship.objects.filter(follower=request.user)
#         # print currently_following
#         # Fetch
#         context = {
#             "all_tweets": Tweet.objects.filter(user=current_user.id)
#             #"all_tweets": None
#         }
#     except ObjectDoesNotExist:
#         raise PermissionDenied
#     return render(request, "twitter/feed.html", context)#HttpResponse(currently_following)

# @require_POST()
@login_required()
def follow(request):
    """
    Creates a following relationship between the authenticated user and
    another user.
    """
    # Query for the user to be followed. That user will be passed to the template.
    # other_user = User.objects.get(username=request.POST.username)
    # other_user = get_object_or_404(User, username=request.POST.username)
    other_user = get_object_or_404(User, username=request.POST['username'])
    
    # Query for tweets to be displayed
    # tweets = Tweet.objects.filter(user=other_user)
    
    # context = {
    #     'feed_user': other_user,
    #     'all_tweets': tweets,
    # }
    
    # Create the relationship
    try:
        Relationship.objects.create(
            follower=request.user, following=other_user
        )
    except IntegrityError:
        pass
    
    # Return to the feed page of the user who was followed
    # return render(request, "twitter/feed.html", context)
    return redirect(request.GET.get('next', '/'))

# @require_POST()
@login_required()
def unfollow(request):
    """
    Deletes an existing following relationship between the authenticated
    user and another user.  Raises an error if the relationship does not
    exist.
    """
    # Query for the user to be unfollowed. That user will be passed to the template.
    # other_user = User.objects.get(username=request.POST.username)
    # print("request.POST =", request.POST)
    # print("request.POST['username'] =", request.POST['username'])
    other_user = get_object_or_404(User, username=request.POST['username'])
    
    # # Query for tweets to be displayed
    # tweets = Tweet.objects.filter(user=other_user)
    
    # context = {
    #     'feed_user': other_user,
    #     'all_tweets': tweets,
    # }
    
    # Delete the relationship
    Relationship.objects.filter(
        follower=request.user, following=other_user
    ).delete()
    
    # Return to the feed page of the user who was unfollowed
    # return render(request, "twitter/feed.html", context)
    return redirect(request.GET.get('next', '/'))
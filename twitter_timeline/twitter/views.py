from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TweetForm
from .models import Tweet


@login_required
def home_page(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            form = TweetForm()
            messages.success(request, 'Tweet created!')
    else:
        form = TweetForm()
    # TODO following too
    tweets = Tweet.objects.filter(user=request.user)
    context = {
        'form': form,
        'tweets': tweets,
        'user': request.user.username
    }
    return render(request, 'feed.html', context)


def user_profile(request, username):
    if request.user.is_authenticated() and username == request.user.username:
        return home_page(request)
    if request.method == 'POST':
        return HttpResponseForbidden()
    user = get_object_or_404(get_user_model(), username=username)
    tweets = Tweet.objects.filter(user=user)
    context = {'tweets': tweets, 'user': username, 'other_user': username}
    print("is auth'd:{}".format(request.user.is_authenticated()))
    print("is following:{}".format(request.user.is_following(user)))
    if request.user.is_authenticated() and not request.user.is_following(user):
        context.update(follow=True)
    return render(request, 'feed.html', context)


@login_required
@require_POST
def follow(request):
    user_to_follow = get_object_or_404(get_user_model(), username=request.POST['username'])
    request.user.follow(user_to_follow)
    return redirect(request.GET.get('next', '/'))


@login_required
@require_POST
def unfollow(request):
    user_to_unfollow = get_object_or_404(get_user_model(), username=request.POST['username'])
    request.user.unfollow(user_to_unfollow)
    return redirect(request.GET.get('next', '/'))


@login_required()
def logout(request):
    django_logout(request)
    return redirect('/')


@login_required()
@require_POST
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if tweet.user != request.user:
        raise PermissionDenied
    tweet.delete()
    messages.success(request, 'Tweet successfully deleted')
    return redirect(request.GET.get('next', '/'))

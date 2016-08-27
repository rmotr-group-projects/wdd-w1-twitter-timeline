from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

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


@require_GET
def user_profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    tweets = Tweet.objects.filter(user=user)
    context = {'tweets': tweets, 'user': username, 'other_user': username}
    if request.user.is_authenticated() and request.user.is_following(username):
        context.update(follow=True)
    return render(request, 'feed.html', context)


@login_required
@require_POST
def follow(request):
    pass


@login_required
@require_POST
def unfollow(request):
    pass


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

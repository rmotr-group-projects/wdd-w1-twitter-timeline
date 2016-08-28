from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'twitter'

urlpatterns = [
    url(r'^login', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^follow$', views.follow, name='follow'),
    url(r'^unfollow$', views.unfollow, name='unfollow'),
    url(r'^$', views.home_page, name='home_page'),
    url(r'^(?P<username>\w+)$', views.user_profile, name='user_feed'),
    url(r'^tweet/(?P<tweet_id>\d+)/delete', views.delete_tweet, name='delete_tweet'),
]

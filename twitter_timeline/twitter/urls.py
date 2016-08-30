from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.other_index, name="index"),
    url(r'^login', auth_views.login, {'template_name': 'twitter/login.html'}),
    url(r'^logout', views.logout),
    url(r'^tweet/(?P<tweet_id>\d+)/delete', views.delete_tweet),
    url(r'^create_tweet/', views.create_tweet, name="create_tweet"),
    url(r'^unfollow', views.unfollow),
    url(r'^follow', views.follow),
    url(r'^(?P<username>\w+)', views.profile, name="profile"),
]

# -*- coding:utf-8 -*-


from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import Context
from postermaker.models import User
from postermaker.twitter_timeline import TwitterTimeLine
from requests_oauthlib import OAuth1Session


_CONSUMER_KEY = settings.SOCIAL_AUTH_TWITTER_KEY
_CONSUMER_SECRET = settings.SOCIAL_AUTH_TWITTER_SECRET
_REQUEST_TOKEN_URL = settings.TWITTER_REQUEST_TOKEN_URL
_AUTHORIZATION_URL = settings.TWITTER_AUTHORIZATION_URL
_ACCESS_TOKEN_URL = settings.TWITTER_ACCESS_TOKEN_URL
_CALLBACK_URI = settings.TWITTER_CALLBACK_URI


def poster(request):
    access_token = request.session.get('access_token', None)
    if not access_token:
        return redirect('postermaker:login')

    user = User.objects.get(oauth_token=access_token)

    tw_timeline = TwitterTimeLine(consumer_key=_CONSUMER_KEY,
                                  consumer_secret=_CONSUMER_SECRET,
                                  access_token_key=user.oauth_token,
                                  access_token_secret=user.oauth_token_secret)

    user.twitter_account = tw_timeline.get_user_twitter_account()
    user.twitter_id = tw_timeline.get_user_twitter_id()
    user.save()

    context = Context()
    context['twitter_account'] = user.twitter_account
    context['tweets'] = tw_timeline.get_user_timeline(max_tweets=100)

    return render_to_response('postermaker/poster.html', context)


def login(request):
    oauth_client = OAuth1Session(_CONSUMER_KEY,
                                 client_secret=_CONSUMER_SECRET,
                                 callback_uri=_CALLBACK_URI)
    request_token_url = _REQUEST_TOKEN_URL
    response = oauth_client.fetch_request_token(request_token_url)

    redirect_url = _AUTHORIZATION_URL + '?oauth_token=' +\
        response['oauth_token']

    return redirect(redirect_url)


def callback(request):
    request_token = request.GET['oauth_token']
    verifier = request.GET['oauth_verifier']
    oauth_client = OAuth1Session(_CONSUMER_KEY,
                                 client_secret=_CONSUMER_SECRET,
                                 resource_owner_key=request_token,
                                 verifier=verifier)
    access_token_url = _ACCESS_TOKEN_URL
    response = oauth_client.fetch_access_token(access_token_url)

    try:
        user = User.objects.get(twitter_id=response['user_id'])
    except User.DoesNotExist:
        user = User()
        user.twitter_id = response['user_id']
        user.oauth_token = response['oauth_token']
        user.oauth_token_secret = response['oauth_token_secret']
        user.save()

    if user.oauth_token != response['oauth_token']:
        user.oauth_token = response['oauth_token']
        user.oauth_token_secret = response['oauth_token_secret']
        user.save()

    request.session['access_token'] = response['oauth_token']

    return redirect('postermaker:poster')

# -*- coding:utf-8 -*-


from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from postermaker.get_category import CategoryExtractor
from postermaker.twitter_timeline import TwitterTimeLine
from requests_oauthlib import OAuth1Session


_CONSUMER_KEY = settings.SOCIAL_AUTH_TWITTER_KEY
_CONSUMER_SECRET = settings.SOCIAL_AUTH_TWITTER_SECRET
_REQUEST_TOKEN_URL = settings.TWITTER_REQUEST_TOKEN_URL
_AUTHORIZATION_URL = settings.TWITTER_AUTHORIZATION_URL
_ACCESS_TOKEN_URL = settings.TWITTER_ACCESS_TOKEN_URL
_CALLBACK_URI = settings.TWITTER_CALLBACK_URI

@login_required
def poster(request):

    user = request.user
    twitter_auth = user.social_auth.get(provider='twitter')
    access_token = twitter_auth.access_token

    tw_timeline = TwitterTimeLine(consumer_key=_CONSUMER_KEY,
                                  consumer_secret=_CONSUMER_SECRET,
                                  access_token_key=access_token.get('oauth_token'),
                                  access_token_secret=access_token.get('oauth_token_secret'))

    tweets = tw_timeline.get_user_tweets(max_tweets=100)
    ce = CategoryExtractor()

    """
    TODOs:
    try:
        category_list = ce.get_category_list(tweets)
    except SomeException:
        pass

    candidates = Candidates()
    cf = CandidateFinder()
    candidates = cf.get_candidates(category_list) # returns Candidates object

    context['candidates'] = candidates # returns as text strings in json format
    """

    context = RequestContext(request)
    context['twitter_account'] = user.username
    context['categories'] = ce.get_category_list(tweets)

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

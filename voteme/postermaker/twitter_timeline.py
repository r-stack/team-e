# -*- coding: utf-8 -*-

import settings
import twitter

from requests_oauthlib import OAuth1Session


class TwitterTimeLine(object):

    def __init__(self, access_token_key, access_token_secret):
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret

    def get_user_timeline(self, twitter_account, max_tweets):
        api = twitter.Api(consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
                          consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                          access_token_key=self.access_token_key,
                          access_token_secret=self.access_token_secret)

        user = api.GetUser(screen_name=twitter_account)
        states = api.GetUserTimeline(screen_name=twitter_account,
                                     count=max_tweets)

        return(user, states)

# -*- coding: utf-8 -*-

import twitter


class TwitterTimeLine(object):
    def __init__(self, consumer_key, consumer_secret, access_token_key,
                 access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
        self.api = twitter.Api(consumer_key=self.consumer_key,
                               consumer_secret=self.consumer_secret,
                               access_token_key=self.access_token_key,
                               access_token_secret=self.access_token_secret)
        self.user = self.api.VerifyCredentials()

    def get_tweets(self, twitter_account, max_tweets=100):
        timelines = self.api.GetUserTimeline(screen_name=twitter_account,
                                             cound=max_tweets)
        tweets = []
        for timeline in timelines:
            tweets.append(timeline.text)

        return tweets

    def get_user_tweets(self, max_tweets=100):
        timelines = self.api.GetUserTimeline(screen_name=self.user.screen_name,
                                             count=max_tweets)

        tweets = []
        for timeline in timelines:
            tweets.append(timeline.text)

        return tweets

    def get_user_twitter_account(self):
        return self.user.screen_name

    def get_user_twitter_id(self):
        return self.user.id

    def get_user_twitter_profile_image_url(self):
        return self.user.profile_image_url

# -*- coding: utf-8 -*-

from django.conf import settings
from postermaker.get_category import CategoryExtractor
from postermaker.get_tweets import TwitterTimeLine
from postermaker.models import Politician

_CONSUMER_KEY = settings.SOCIAL_AUTH_TWITTER_KEY
_CONSUMER_SECRET = settings.SOCIAL_AUTH_TWITTER_SECRET
_ACCESS_TOKEN = settings.TWITTER_ACCESS_TOKEN
_ACCESS_SECRET = settings.TWITTER_ACCESS_TOKEN_SECRET

_POLITICIAN_TWITTER_ACCOUNTS = [
    '',
]


def get_politician_category_list(twitter_account):
    tw_timeline = TwitterTimeLine(consumer_key=_CONSUMER_KEY,
                                  consumer_secret=_CONSUMER_SECRET,
                                  access_token_key=_ACCESS_TOKEN,
                                  access_token_secret=_ACCESS_SECRET)

    tweets = tw_timeline.get_tweets(twitter_account=twitter_account)

    ce = CategoryExtractor()
    category_list = ce.get_category_list(tweets)

    return category_list


if __name__ == '__main__':
    p_twitter_accounts = _POLITICIAN_TWITTER_ACCOUNTS

    for p_twitter_account in p_twitter_accounts:
        try:
            politician = Politician.objects.get(
                twitter_account=p_twitter_account)
        except Politician.DoesNotExist:
            politician = Politician()

        politician.category_list = get_politician_category_list(
            p_twitter_account)
        politician.save()

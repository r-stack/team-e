# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
from django.conf import settings
from postermaker.get_category import CategoryExtractor
from postermaker.models import Politician
from postermaker.twitter_timeline import TwitterTimeLine

_CONSUMER_KEY = settings.SOCIAL_AUTH_TWITTER_KEY
_CONSUMER_SECRET = settings.SOCIAL_AUTH_TWITTER_SECRET
_ACCESS_TOKEN = settings.TWITTER_ACCESS_TOKEN
_ACCESS_SECRET = settings.TWITTER_ACCESS_TOKEN_SECRET

_POLITICIAN_TWITTER_ACCOUNTS = [
    'Shogo_tkhs',
    'YujiroTaniyama',
    'Doronpa01',
    'shuntorigoe',
    'macakasaka',
    'toshio1040pj',
    'ytammasa1',
    'ecoyuri',
    'uesugitakashi',
    'hiroko_nanami',
    'Chozo_Nakagawa',
    'miyazaki_tokyo',
]


class PoliticianUpdator(object):
    def __init__(self):
        self._tw_timeline = TwitterTimeLine(consumer_key=_CONSUMER_KEY,
                                            consumer_secret=_CONSUMER_SECRET,
                                            access_token_key=_ACCESS_TOKEN,
                                            access_token_secret=_ACCESS_SECRET)
        self._ce = CategoryExtractor()

    def get_politician_category_list(self, twitter_account):
        tweets = self._tw_timeline.get_tweets(twitter_account=twitter_account,
                                              max_tweets=100)
        category_list = self._ce.get_category_list(tweets)

        return category_list

    def get_politician_twitter_screen_name(self, twitter_account):
        screen_name = self._tw_timeline.get_user_screen_name(
            twitter_account=twitter_account)

        return screen_name

    def get_politician_twitter_description(self, twitter_account):
        description = self._tw_timeline.get_description(
            twitter_account=twitter_account
        )

        return description

    def get_politician_image(self, twitter_account):
        image_url = self._tw_timeline.get_profile_image_url(
            twitter_account=twitter_account
        )

        return image_url


def main():
    p_twitter_accounts = _POLITICIAN_TWITTER_ACCOUNTS
    p_updator = PoliticianUpdator()

    for p_twitter_account in p_twitter_accounts:
        try:
            politician = Politician.objects.get(
                twitter_account=p_twitter_account)
        except Politician.DoesNotExist:
            politician = Politician(twitter_account=p_twitter_account)

        print('politician account = {tw_account}'.format(
            tw_account=politician.twitter_account))

        politician.category_list = p_updator.get_politician_category_list(
            p_twitter_account)
        print('category_list = {category_list}'.format(
            category_list=politician.category_list))

        politician.manifest = p_updator.get_politician_twitter_description(
            p_twitter_account
        )
        print('manifest = {manifest}'.format(
            manifest=politician.manifest))

        politician.twitter_profile_image_url = p_updator.get_politician_image(
            p_twitter_account
        )
        print('image_url = {image_url}'.format(
            image_url=politician.twitter_profile_image_url))

        politician.save()

if __name__ == '__main__':
    main()

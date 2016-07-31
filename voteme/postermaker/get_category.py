# -*- coding: utf-8 -*-
"""
docomoの言語解析API(カテゴリ分析)を叩くコード
"""

from __future__ import unicode_literals
from logging import getLogger

import json
import requests
import time

from django.conf import settings

_DOCOMO_API_BASE_URL = settings.DOCOMO_API_BASE_URL
_DOCOMO_API_KEY = settings.DOCOMO_API_KEY

logger = getLogger(__name__)


class CategoryExtractor(object):
    def __init__(self, docomo_api_key=_DOCOMO_API_KEY):
        self.uri = "{base_url}?APIKEY={api_key}".format(
            base_url=_DOCOMO_API_BASE_URL, api_key=docomo_api_key)
        self.payload = {
                'text': None,
                'extflg': '0',
                }
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def parse(self, query):
        self.payload['text'] = query
        r = requests.post(self.uri, data=self.payload, headers=self.headers)
        return json.loads(r.text)

    def get_category_list(self, tweets):
        category_list = []

        # packing tweets upto 500 charactors to save the number of api-call
        packed_tweet = ''
        for tweet in tweets:
            # assume that one tweet <= 140 charactors
            logger.debug("get_category: len_packed_tweet = {}".format(
                len(packed_tweet)))

            if len(packed_tweet) > 350:
                """
                TODOs:
                 - currently it ommits the 'tails' of tweets, when it doesn't
                   make up to 350 charactors.
                """
                # To avoid throughput overrun
                time.sleep(0.3)
                categories = self.get_category(packed_tweet)
                if categories is not None:
                    category_list.extend(categories)

                packed_tweet = ''

            else:
                packed_tweet += tweet

        return category_list

    def get_category(self, text):
        resp = self.parse(text)
        count = resp.get('count', 0)

        # Ignore a too short tweet
        if count == 0:
            return None

        # Get the cluster of 1st rank
        categories = []
        clusters = resp['clusters']
        for cluster in clusters:
            logger.debug("get_category: cluster_name = {cluster_name}, \
                cluster_rate = {cluster_rate}".format(
                cluster_name=cluster['cluster_name'],
                cluster_rate=cluster['cluster_rate']))
            if cluster['cluster_rate'] >= 5:
                categories.append(cluster['cluster_name'])

        logger.debug("get_category: categories = {categories}".format(
            categories=categories))

        return categories

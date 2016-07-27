# -*- coding: utf-8 -*-
"""
docomoの言語解析API(カテゴリ分析)を叩くコード
"""

import json
import requests
import time

from django.conf import settings

_DOCOMO_API_BASE_URL = settings.DOCOMO_API_BASE_URL
_DOCOMO_API_KEY = settings.DOCOMO_API_KEY


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

        for tweet in tweets:
            # To avoid throughput overrun
            time.sleep(0.3)
            category = self.get_category(tweet)
            if category is not None:
                category_list.append(category)

        return category_list

    def get_category(self, text):
        resp = self.parse(text)
        count = resp.get('count', 0)

        # Ignore a too short tweet
        if count == 0:
            return None

        # Get the cluster of 1st rank
        clusters = resp['clusters']
        for cluster in clusters:
            if cluster['cluster_rank'] == 1:
                name = cluster['cluster_name']
                break

        return name

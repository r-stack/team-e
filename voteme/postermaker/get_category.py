# -*- coding: utf-8 -*-
"""
docomoの言語解析API(カテゴリ分析)を叩くコード
"""

import json
import requests
import time

from django import settings
from get_user_timeline import TwitterTimeLine

_DOCOMO_API_BASE_URL = settings.DOCOMO_API_BASE_URL
_DOCOMO_API_KEY = settings.DOCOMO_API_KEY


class Docomo(object):

    def __init__(self, docomo_api_key=_DOCOMO_API_KEY):
        self.uri = "{}{}".format(_DOCOMO_API_BASE_URL, docomo_api_key)
        self.payload = {
                "text": None,
                "extflg": "0",
                }
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def parse(self, query):
        self.payload["text"] = query
        r = requests.post(self.uri, data=self.payload, headers=self.headers)
        return json.loads(r.text)


class categoryGetter(object):

    def ext1stRankCategory(self, text):
        agent = Docomo()
        resp = agent.parse(text)
        status = resp["status"]
        count = resp["count"]
        rawdata = resp["rawdata"]

        # Ignore a too short tweet
        if(count == 0):
            return None

        # Get the cluster of 1st rank
        clusters = resp["clusters"]
        for cluster in clusters:
            if cluster["cluster_rank"] == 1:
                name = cluster["cluster_name"]
                break

        return name

    def getCategoryList(self, account, getTweetNum):
        categoryList = []
        user, state = getUserTimeline(account, getTweetNum)

        for s in state:
            text = s.text
            # To avoid throughput overrun
            time.sleep(0.3)
            category = self.ext1stRankCategory(text)
            if(category is not None):
                categoryList.append(category)

        return categoryList
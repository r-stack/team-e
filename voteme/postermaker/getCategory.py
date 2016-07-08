# -*- coding: utf-8 -*-
"""
docomoの言語解析API(カテゴリ分析)を叩くコード
"""

import sys
import requests
import json
import urllib
import time

from getUserTimeline import getUserTimeline

BASEURL = "https://api.apigw.smt.docomo.ne.jp/truetext/v1/clusteranalytics?APIKEY="
APIKEY = "444552716859306e54463832347732396661536342585358677146544852764378504a4f706c6b69715a36" #ここにAPIKEYを入力

class Docomo(object):
    def __init__(self, APIKEY=APIKEY):
        self.uri = "{}{}".format(BASEURL, APIKEY)
        self.payload = {
                "text": None,
#                "extflg": "0" #一般ワード除外フラグ
                }
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def parse(self, query):
        self.payload["text"] = query
        r = requests.post(self.uri, data=self.payload, headers=self.headers)
        return json.loads(r.text)


#################### ext1StRankCategory ####################
class categoryGetter():
    def ext1stRankCategory(self, text):
        agent = Docomo()

#        print type(text)
        resp = agent.parse(text)

        status  = resp["status"]
        count   = resp["count"]
        rawdata = resp["rawdata"]
        
# print response for debug
        print "Status: {}\t Count: {}\t".format(status, count)

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
                

#################### getCategoryList ####################
    def getCategoryList(self, account, getTweetNum):
        categoryList = []
        user, state = getUserTimeline(account, getTweetNum)

        for s in state :
            text = s.text
# To avoid throughput overrun
            time.sleep(0.3)
            category = self.ext1stRankCategory(text)
            if(category != None):
                categoryList.append(category)

        return categoryList


if __name__ == "__main__":
    getter = categoryGetter()
    argv = sys.argv
    categoryList = getter.getCategoryList(argv[1], argv[2])

# For debug
    for category in categoryList:
        print category.encode(sys.getfilesystemencoding())

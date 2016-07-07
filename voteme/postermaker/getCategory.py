# -*- coding: utf-8 -*-
"""
docomoの言語解析API(固有表現抽出)を叩くサンプルコード
"""
import requests
import json
import urllib

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
def ext1StRankCategory(str):
    agent = Docomo()
    resp  = agent.parse(str)

    status  = resp["status"]
    count   = resp["count"]
    rawdata = resp["rawdata"]
    
# print response for debug
    print "Status: {}\t Count: {}\t".format(status, count)

    clusters = resp["clusters"]
    
# Get the cluster of 1st rank
    for cluster in clusters:
        name = cluster["cluster_name"]
        rate = cluster["cluster_rate"]
        rank = cluster["cluster_rank"]
        
        if rank == 1:
            break

    print name
    print rate
    print rank

if __name__ == "__main__":
    str = u'昨日は隅田川に花火を見に行きました。地下鉄の浅草駅で降りた瞬間から、大混雑していました。地上に出てみると人混みと交通規制の多さで大苦戦しましたが、何とか良い場所で花火を見るこが出来ました。夏の風物詩、花火をどうぞお楽しみください'
    ext1StRankCategory(str)

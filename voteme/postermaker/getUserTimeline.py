#!/usr/bin/env python
# -*- coding: utf-8 -*-

# usage: python getUserTimeline userName(excluding @) getTweetNum

from requests_oauthlib import OAuth1Session
import json
import sys
import twitter
import settings

# 引数チェック
argv = sys.argv

# ToDo: 土田アカウントで認証処理しているので変更したい
api = twitter.Api(consumer_key=settings.CONSUMER_KEY,
                  consumer_secret=settings.CONSUMER_SECRET,
                  access_token_key=settings.ACCESS_TOKEN,
                  access_token_secret=settings.ACCESS_TOKEN_SECRET)


state = api.GetUserTimeline(screen_name=argv[1],count = argv[2])
for s in state :
    print s.text.encode(sys.getfilesystemencoding())
    # ToDo カテゴリ取得処理を呼び出し
    

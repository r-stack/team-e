#!/usr/bin/env python
# -*- coding: utf-8 -*-

# usage: python getUserTimeline userName(excluding @) getTweetNum

from requests_oauthlib import OAuth1Session
import json
import sys
import twitter
import settings

def getUserTimeline(userName, tweetNum):

    # ToDo: 土田アカウントで認証処理しているので変更したい
    api = twitter.Api(consumer_key=settings.CONSUMER_KEY,
                      consumer_secret=settings.CONSUMER_SECRET,
                      access_token_key=settings.ACCESS_TOKEN,
                      access_token_secret=settings.ACCESS_TOKEN_SECRET)


    user = api.GetUser(screen_name=userName);
    print user.screen_name
    state = api.GetUserTimeline(screen_name=userName,count = tweetNum)
    for s in state :
        print s.text.encode(sys.getfilesystemencoding())
        # ToDo カテゴリ取得処理を呼び出し
    return(user,state);


if  __name__ == "__main__":
    argv = sys.argv
    getUserTimeline(argv[1],argv[2])

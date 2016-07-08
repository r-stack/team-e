#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from getCategory import categoryGetter

POLI_A_NAME = "ikuemiroku"
POLI_B_NAME = "yokokume"

class Matching():
    def matching(self, account):
        POLI_A = [u"ビジネス一般用語",u"インターネットスラング",u"写メ・ムービー・動画",u"法律・法案"]
        POLI_B = [u"その他ジャーナリズム",u"日本の政治・選挙",u"ビジネス一般用語",u"その他鉄道",u"ビジネス一般用語",u"東京都"]

        getter = categoryGetter()
        
        categoryList = getter.getCategoryList(account, 20)
     
        Match_A = []
        Match_B = []

        for keyword in categoryList:
            for poli_a_key in POLI_A:
                if keyword == poli_a_key:
                    Match_A.append(keyword)
            for poli_b_key in POLI_B:
                if keyword == poli_b_key:
                    Match_B.append(keyword)

        if(len(Match_A) > len(Match_B)):
            name = POLI_A_NAME
            Match = Match_A
        else:
            name = POLI_B_NAME
            Match = Match_B

        print name
        for word in Match:
            print word.encode('utf8')
        return name

if __name__ == "__main__":
    matcher = Matching()
    argv = sys.argv
    categoryList = matcher.matching(argv[1])

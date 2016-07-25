# -*- coding: utf-8 -*-

from postermaker.modles import Politician


class Candidate(object):
    def __init__(self, twitter_account=None):
        self._twitter_account = twitter_account
        self._matched_categories = []

    @property
    def matched_categories():
        doc = "The matched_categories property."

        def fget(self):
            return self._matched_categories

        def fset(self, value):
            self._matched_categories = value

        def fdel(self):
            del self._matched_categories

        return locals()

    matched_categories = property(**matched_categories())

    @property
    def twitter_account():
        doc = "The twitter_account property."

        def fget(self):
            return self._twitter_account

        def fset(self, value):
            self._twitter_account = value

        def fdel(self):
            del self._twitter_account

        return locals()

    twitter_account = property(**twitter_account())


class CandidateFinder(object):
    def __init__(self):
        self._candidates = []
        self._politicians = Politician.objects.all()

    def get_candidates(self, category_list):

        for politician in self._politicians:
            candidate = Candidate(politician.twitter_account)
            # matching
            user_category_set = set(category_list)
            politician_category_set = set(politician.category_list)

            matched_categories = user_category_set & politician_category_set
            candidate.matched_categories = list(matched_categories)

            self._candidates.append(candidate)

        return self._candidates

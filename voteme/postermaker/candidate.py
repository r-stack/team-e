# -*- coding: utf-8 -*-

from postermaker.models import Politician


class Candidate(object):
    def __init__(self, twitter_account=None):
        self._twitter_account = twitter_account
        self._matched_categories = []

    @property
    def matched_categories(self):
        """The matched_categories property."""
        return self._matched_categories

    @matched_categories.setter
    def matched_categories(self, value):
        self._matched_categories = value

    @matched_categories.deleter
    def matched_categories(self):
        del self._matched_categories

    @property
    def twitter_account(self):
        """The twitter_account property."""
        return self._twitter_account

    @twitter_account.setter
    def twitter_account(self, value):
        self._twitter_account = value

    @twitter_account.deleter
    def twitter_account(self):
        del self._twitter_account


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

# -*- coding: utf-8 -*-

from postermaker.models import Politician


class Candidate(object):
    def __init__(self, politician=None):
        self._politician = politician
        self._matched_categories = []
        self._score = 0

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
    def politician(self):
        """The politician property."""
        return self._politician

    @politician.setter
    def politician(self, value):
        self._politician = value

    @politician.deleter
    def politician(self):
        del self._politician

    @property
    def score(self):
        """The score property."""
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @score.deleter
    def score(self):
        del self._score


class CandidateFinder(object):
    def __init__(self):
        self._candidates = []
        self._politicians = Politician.objects.all()

    def get_candidates(self, category_list):

        if len(category_list) > 0:
            for politician in self._politicians:
                candidate = Candidate(politician)
                # matching
                user_category_set = set(category_list)
                p_category_set = set(politician.category_list)

                matched_categories = user_category_set & p_category_set
                candidate.matched_categories = list(matched_categories)

                candidate.score = len(candidate.matched_categories) / \
                    len(category_list)

                self._candidates.append(candidate)

        return self._candidates

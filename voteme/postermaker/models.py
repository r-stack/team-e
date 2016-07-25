# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
import json


class Politician(models.Model):
    twitter_account = models.CharField(max_length=30, default="")
    twitter_profile_image_url = models.URLField(max_length=200, default="")
    manifest = models.CharField(max_length=30, null=True, default="")
    _category_list = models.CharField(
        db_column="category_list", max_length=4096, null=True, default="")

    @property
    def category_list(self):
        return json.loads(self.category_list)

    @category_list.setter
    def category_list(self, category_list):
        self.category_list = json.dumps(category_list)

    @category_list.deleter
    def category_list(self):
        del self._category_list


class Category(models.Model):
    politician = models.ForeignKey(Politician)
    keyword = models.CharField(max_length=30, null=True, default="")


class User(models.Model):
    twitter_id = models.BigIntegerField(primary_key=True)
    twitter_account = models.CharField(max_length=30, default="")
    twitter_profile_image_url = models.URLField(max_length=200, default="")
    oauth_token = models.CharField(max_length=255, db_index=True, unique=True)
    oauth_token_secret = models.CharField(max_length=255, db_index=True,
                                          unique=True)

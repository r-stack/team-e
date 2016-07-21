# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class Politician(models.Model):
    twitter_account = models.CharField(max_length=30, default="")
    manifest = models.CharField(max_length=30, null=True, default="")


class Category(models.Model):
    politician = models.ForeignKey(Politician)
    keyword = models.CharField(max_length=30, null=True, default="")


class User(models.Model):
    twitter_id = models.BigIntegerField(primary_key=True)
    twitter_account = models.CharField(max_length=30, default="")
    oauth_token = models.CharField(max_length=255, db_index=True, unique=True)
    oauth_token_secret = models.CharField(max_length=255, db_index=True,
                                          unique=True)

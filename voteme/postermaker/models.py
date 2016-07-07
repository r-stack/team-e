# @Author: kwbt69
# @Date:   2016-07-07T16:00:42+09:00
# @Last modified by:   kwbt69
# @Last modified time: 2016-07-07T18:47:13+09:00


from __future__ import unicode_literals

from django.db import models

class Category(models.Model):
    twitter_account = models.CharField(max_length=30)
    keyword = models.CharField(max_length=30)
    count = models.IntegerField()

class Manifest(models.Model):
    twitter_account = models.CharField(max_length=30)
    manifest_wording = models.CharField(max_length=30)

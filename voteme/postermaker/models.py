# @Author: kwbt69
# @Date:   2016-07-07T16:00:42+09:00
# @Last modified by:   kwbt69
# @Last modified time: 2016-07-08T10:27:26+09:00


from __future__ import unicode_literals

from django.db import models

class Politician(models.Model):
    twitter_account = models.CharField(max_length=30)
    manifest = models.CharField(max_length=30)

class Category(models.Model):
    politician = models.ForeignKey(Politician)
    keyword = models.CharField(max_length=30)

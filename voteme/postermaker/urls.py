# -*- coding: utf-8 -*-
# @Author: kwbt69
# @Date:   2016-07-07T16:47:47+09:00
# @Last modified by:   kwbt69
# @Last modified time: 2016-07-07T18:46:12+09:00

from django.conf.urls import patterns, include, url
from django.contrib.auth import views
from django.views.generic import TemplateView
from postermaker import views

urlpatterns = patterns('',
    url(r'^/$', TemplateView.as_view(template_name="postermaker/index.html",
    name="index")),
    url(r'^login/$', include('social_auth.urls')),
    url(r'^poster/$', 'postermaker.views.poster'),
)

# -*- coding: utf-8 -*-
# @Date:   2016-07-07T16:47:47+09:00
# @Last modified by:   kwbt69
# @Last modified time: 2016-07-15T11:40:49+09:00

from django.conf.urls import url
from postermaker import views

urlpatterns = [
    url(r'^$', views.poster, name="poster"),
    url(r'^callback/$', views.callback, name="callback"),
    url(r'^login/$', views.login, name="login"),
]

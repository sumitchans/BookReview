'''
Created on Mar 7, 2016

@author: sumit
'''

from .views import *
from django import *
from django.conf.urls.i18n import urlpatterns
from django.conf.urls import patterns, url

urlpatterns=patterns('',url(r'^login/$',Login,name='accounts.login'),
                     url(r'^user_login/',user_login,name='accounts.user_login'),
                      url(r'^user_register/',user_register,name='accounts.user_register'),
                       url(r'^reset/',reset,name='accounts.reset'),
                       url(r'^forgot',forgot_passowrd,name='accounts.forgot'),
                      url(r'^logout/',user_logout,name='accounts.logout'),
                     )

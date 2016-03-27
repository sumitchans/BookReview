"""BookReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf.urls.static import static
from BookReview import settings
from accounts import urls
from Review.views import *
import Review
import accounts
import BookReview
urlpatterns = patterns('',
               url(r'^$',view='Review.views.Home',name='Review.Home'),
                url(r'^accounts/',include(accounts.urls)),
               url(r'^admin/', include(admin.site.urls)),
                      url(regex=r'^AddBook/$',view='Review.views.AddBook',name='Review.AddBook'),
                    url(r'^BookInfo/(\d+)$',view='Review.views.BookInfo',name='Review.BookInfo'),
                     url(r'^UserBooks/$',view='Review.views.Home',kwargs={'Userbook':True},name='Review.UserBooks'),
                     url(r'^BookFilter/$',view='Review.views.BookFilter',name='Review.BookFilter'),
                     url(r'^BookRating/(\d+)$',view='Review.views.BookRating',name='Review.BookRating'),
                     url(r'^AddReview/(\d+)$',view='Review.views.AddReview',name='Review.AddReview'),
                     url(r'^LikeReview/(\d+)/(\d+)$',view='Review.views.LikeReview',name='Review.LikeReview'),
                     url(r'^DisLikeReview/(\d+)/(\d+)$',view='Review.views.DisLikeReview',name='Review.DisLikeReview'), 
                       url(r'^About/$',view='Review.views.About',name='Review.About'),
                          url(r'^Contact/$',view='Review.views.Contact',name='Review.Contact'),
                        url(r'^BookUpload/$',view='Review.views.bookUpload',name='Review.BookUpload'),
)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

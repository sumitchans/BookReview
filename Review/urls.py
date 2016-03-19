'''
Created on Jan 28, 2016

@author: sumit
'''
from django.conf.urls import  url, patterns
from django.conf.urls.static import static
from BookReview import settings
from django.conf.urls.i18n import urlpatterns
from views import AddBook,BookFilter,BookInfo,AddBookInfo,AddReview,LikeReview,DisLikeReview,BookRating,UserBooks
urlpatterns=patterns('',
        
             url(regex=r'^AddBook/$',AddBook,name='Review.AddBook'),
                               url(r'^BookInfo/(\d+)$',BookInfo,name='Review.BookInfo'),
                     url(r'^UserBooks/$',UserBooks,name='Review.UserBooks'),
                     url(r'^BookFilter/$',BookFilter,name='Review.BookFilter'),
                     url(r'^BookRating/(\d+)$',BookRating,name='Review.BookRating'),
                     url(r'^AddReview/(\d+)$',AddReview,name='Review.AddReview'),
                     url(r'^LikeReview/(\d+)/(\d+)$',LikeReview,'Review.LikeReview'),
                     url(r'^DisLikeReview/(\d+)/(\d+)$',DisLikeReview,name='Review.DisLikeReview'),
             )
#urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
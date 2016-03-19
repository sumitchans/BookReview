from django.contrib import admin
from .models import BookType
from Review.models import BookInfo, UserInfo,Review
admin.site.register(BookType)
admin.site.register(BookInfo)
admin.site.register(UserInfo)
admin.site.register(Review)

# Register your models here.

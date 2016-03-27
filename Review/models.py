from django.db import models
from django.template.defaultfilters import default

# Create your models here.
class UserInfo(models.Model):
    user_name=models.CharField(max_length=255,primary_key=True)
    name=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    confirm_password=models.CharField(max_length=255)
class BookType(models.Model):
    type=models.CharField(max_length=255)
class BookInfo(models.Model):
    book_name=models.CharField(max_length=255)
    book_type=models.ForeignKey(BookType)
    date_of_add=models.DateField()
    description=models.TextField()
    image=models.ImageField(upload_to='book')
    user_id=models.ForeignKey(UserInfo)
    approved=models.BooleanField(default=False)
class Rating(models.Model):
    book_id=models.ForeignKey(BookInfo)
    user_id=models.ForeignKey(UserInfo)
    rating=models.IntegerField()
class Review(models.Model):
    review=models.TextField()
    book_id=models.ForeignKey(BookInfo)
    user_id=models.ForeignKey(UserInfo)
class Like(models.Model):
    review_id=models.ForeignKey(Review)
    user_id=models.ForeignKey(UserInfo)
    like=models.IntegerField(default=0)
class DisLike(models.Model):
    review_id=models.ForeignKey(Review)
    user_id=models.ForeignKey(UserInfo)
    dislike=models.IntegerField(default=0)
class Comments(models.Model):
    comment=models.TextField()
    review_id=models.ForeignKey(Review)
    user_id=models.ForeignKey(UserInfo)
    book_id=models.ForeignKey(BookInfo)
    like=models.IntegerField(default=0)
    dislike=models.IntegerField(default=0)
class SoftBook(models.Model):
    book_id=models.ForeignKey(BookInfo)
    user_id=models.ForeignKey(UserInfo)
    book=models.FileField(upload_to='softcopy')
    
        
    
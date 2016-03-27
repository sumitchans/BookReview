'''
Created on Jan 31, 2016

@author: sumit
'''
from django.contrib.auth.models import *
from Review.models import *
from datetime import datetime
from collections import namedtuple
from django.conf.urls.static import static
from django.db.models import Q

class BookInformation(object):
    def AddBook(self,book_name,book_type_id,book_desc,book_image,book_review,book_rating,user_name):
        book_type=BookType.objects.get(id=book_type_id)
        user_id=UserInfo.objects.get(user_name=user_name)
        book=BookInfo(book_name=book_name,book_type=book_type,date_of_add=datetime.now().date(),
                      description=book_desc,image=book_image,user_id=user_id)
        book.save()
        
        review=Review(review=book_review,book_id=book,user_id=user_id)
        review.save()
        rating=Rating(book_id=book,user_id=user_id,rating=book_rating)
        rating.save();
    def GetUsersBook(self,user_name=None,book_type_id=None,book_name=None):
        user_books=[]
        book_details=namedtuple('bookinfo','book_id,book_name,book_type,book_desc,book_image,book_rating,book_total_review')
        book=None
        if user_name is not None:
            book=BookInfo.objects.filter(user_id=user_name)
        else:
            book=BookInfo.objects.all()
        if book_type_id is not None:
            book=book.filter(book_type__in=book_type_id)
        if book_name is not None:
            book=book.filter(book_name=book_name) 
        book=book.order_by('-date_of_add')
        for bookdetail in book:
            book_id=bookdetail.id
            book_name=bookdetail.book_name
            book_type=BookType.objects.get(id=bookdetail.book_type_id).type
            book_desc=bookdetail.description
            book_image=bookdetail.image
            total_rating=0
            rating=bookdetail.rating_set.all()
            for rate in rating:
                total_rating=total_rating+rate.rating
            book_rating=total_rating/1
            book_total_review=bookdetail.review_set.all().count()
            user_books.append(book_details(book_id,book_name,book_type,book_desc,book_image,book_rating,book_total_review))
        bookslist=[]
        for i in range(0,len(user_books),3):
            bookslist.append(user_books[i:i+3])
        return bookslist
    def GetBookType(self,bookTypeid=None):
        booktypelist=[]
        booktype=namedtuple('booktype','id,type')
        booktypes=None
        if bookTypeid is None:
            booktypes=BookType.objects.all()
        else:
            booktypes=BookType.objects.all().filter(id__in=bookTypeid)            
        for booktypedetail in booktypes:
            booktypelist.append(booktype(booktypedetail.id,booktypedetail.type))
        return booktypelist
    def GetBookInfo(self,book_id):
        book_detail={}#=namedtuple('book_detail','book_id,book_name,book_type,book_desc,book_image,book_total_review')
        book=BookInfo.objects.filter(id=book_id)
        if book.count()!=0:
            bk=book.get()
            book_detail['book_id']=bk.id
            book_detail['book_name']=bk.book_name
            book_detail['book_type']=BookType.objects.get(id=bk.book_type_id).type
            book_detail['book_desc']=bk.description
            book_detail['book_image']=bk.image
            book_detail['book_total_review']=bk.review_set.all().count()
            if bk.softbook_set.all().count()!=0:
                book_detail['bookavailable']=True
                bt=bk.softbook_set.all().values('book')[0]
                book_detail['bookpdf']=bt['book']
            else:
                book_detail['bookavailable']=False
                
                
            #book_detail(book_id,book_name,book_type,book_desc,book_image,book_total_review)
            return book_detail
        else:
            return -1
    def GetReviewInfo(self,book_id,user_id):
        review_details=[]
        #namedtuple('review_details','review_id,review,user_name,like_count,dislike_count')
        review=Review.objects.all().filter(book_id=book_id)
        if review.count()!=0:
            for rv in review:
                review_detail={}
                review_detail['review_id']=rv.id
                review_detail['review']=rv.review
                review_detail['user_name']=rv.user_id_id
                review_detail['like_count']=rv.like_set.all().count()
                review_detail['dislike_count']=rv.dislike_set.all().count()
                review_detail['is_user_like']=self.is_user_like(user_id,rv.id)
                review_detail['is_user_dislike']=self.is_user_dislike(user_id,rv.id)
                review_details.append(review_detail)#(review_id,review,user_name,like_count,dislike_count))
            return review_details
        else:
            return -1;
            
    def bookRating(self,book_id,rating,user_id):
        try:
            bk=BookInfo.objects.get(id=book_id)
            if self.is_user_rate(user_id, book_id):
                rate=Rating.objects.filter(book_id=bk).get(user_id_id=user_id)
                rate.rating=rating
                rate.save()
            else:
                rate=Rating(book_id=bk,rating=rating,user_id=UserInfo.objects.get(user_name=user_id))
                rate.save()
        except:
            print "data is not there";    
        #return abs(new_Rating1)
    def AddReview(self,book_id,user_id,review):
        try:
            if(Review.objects.filter(book_id=book_id).filter(user_id=user_id).count()==0):
                bk=Review(review=review,book_id=BookInfo.objects.get(id=book_id),user_id=UserInfo.objects.get(user_name=user_id))
                bk.save()
            else:
                bk=Review.objects.filter(user_id=user_id).filter(book_id=book_id)
                for bp in bk:
                    bp.review=review
                    bp.save()
            
        except:
            print "data is not in database"
    def is_user_like(self,user_id,review_id):
        if Like.objects.filter(user_id=user_id).filter(review_id=review_id).count()!=0:
            return False
        else:
            return True
    
    def is_user_dislike(self,user_id,review_id):
        if DisLike.objects.filter(user_id=user_id).filter(review_id=review_id).count()!=0:
            return False
        else:
            return True
    
    def is_user_rate(self,user_id,book_id):
        if Rating.objects.filter(user_id=user_id).filter(book_id=book_id).count()!=0:
            return True
        else:
            return False
    
    def SaveBook(self,book_id,user_id,book):
        bk=BookInfo.objects.get(id=book_id)
        user=UserInfo.objects.get(user_name=user_id)
        print book
        sb=SoftBook(book_id=bk,user_id=user,book=book)
        sb.save()
        
              
        
        
        
        
            
        
            
                        
        
    
        
        
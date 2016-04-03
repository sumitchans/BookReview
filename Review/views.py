from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
import os
import sys
from django.core.urlresolvers import reverse
from django.shortcuts import redirect,render
from BookReview.settings import BASE_DIR 
from django.http.response import HttpResponseRedirectBase
from django.shortcuts import render_to_response
from Review.models import * 
from django.contrib.auth.context_processors import auth
from email import email
from Review.Business import BookInformation
sys.path.append(os.path.join(BASE_DIR,'Review','Business'))
sys.path.append(os.path.join(BASE_DIR,'Review','Contants'))
from Review import Business
from Review.Contants import Constants 
from validate_email import validate_email
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from accounts.services import UserInformation
from .forms import BookInfoForm,ReviewForm,SearchBook,Book
from endless_pagination.decorators import page_template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

@login_required
def Hi(request):
    return render_to_response('Login.html')
def Home(request,Userbook=None):
    #print  os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    #print  os.path.dirname(os.path.abspath(__file__))
    request.session['booktypes']=Business.BookInformation().GetBookType()
    request.session.modified=True
    #request.session['searchform']=SearchBook()
    context={'page_title':Constants.homeTitle}
    #context['booktypes']=Business.BookInformation().GetBookType()
    userbooks=None
    if request.method=='GET':
        context['searchform']=SearchBook()
        if Userbook is None:
            userbooks=Business.BookInformation().GetUsersBook()
        else:
            userbooks=Business.BookInformation().GetUsersBook(request.session['user_name'])         
    if request.method=='POST':
        serform=SearchBook(data=request.POST)
        name=request.POST['searchBox']
        context['searchform']=serform
        userbooks=BookInformation().GetUsersBook(book_name=name)  
    paginator = Paginator(userbooks,3)
    page = request.GET.get('page')
    try:
        books= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages) 
    context['books']=books   
    return render_to_response('Home.html',context,context_instance=RequestContext(request))
@login_required
def AddBook(request):
    template='AddBook.html'
    c={'page_title':Constants.addBookTitle}
    request.session['booktypes']=Business.BookInformation().GetBookType()
    if request.method=='GET':
        c['form']=BookInfoForm()
        return render_to_response(template,context=c,context_instance=RequestContext(request))
    if request.method=='POST':
        form=BookInfoForm(request.POST,request.FILES)
        if form.is_valid():
            book_name=request.POST['name']
            book_type=request.POST['type']
            book_desc=request.POST['description']
            book_image=request.FILES['image']
            book_review=request.POST['review']
            book_rate=request.POST['rating']
            user_name=request.session['user_name']
            author_name=request.POST['author']
            book=Business.BookInformation().AddBook(book_name=book_name,book_type_id=book_type,book_desc=book_desc,book_image=book_image,
                                    book_rating=book_rate,book_review=book_review,user_name=user_name,author=author_name)
            return HttpResponseRedirect('/UserBooks/')
        else:
            c['form']=form
            return render_to_response(template,c,context_instance=RequestContext(request))
                    
@login_required       
def BookInfo(request,book_id):
    c={'page_title':Constants.addBookTitle}
    c={'page_title':Constants.bookInfoTitle}
    c['BookInfo']=Business.BookInformation().GetBookInfo(book_id=book_id)
    c['BookReview']=Business.BookInformation().GetReviewInfo(book_id=book_id,user_id=request.session['user_name'])
    if request.method=='GET':
        c['form']=ReviewForm()
        return render_to_response('Book_Info.html',context=c,context_instance=RequestContext(request))
    if request.method=='POST':
        form=ReviewForm(data=request.POST)
        if form.is_valid():
            review=request.POST['review']
            user_id=request.session['user_name']
            Business.BookInformation().AddReview(book_id,user_id,review)
            return HttpResponseRedirect("/BookInfo/%s" % book_id)
        else:
            c['form']=form
            return render_to_response('Book_Info.html',context=c,context_instance=RequestContext(request))
                
        

def BookFilter(request):
    c={'page_title':Constants.homeTitle}
    c['searchform']=SearchBook()
    request.session['booktypes']=Business.BookInformation().GetBookType()
                
    book_type=Business.BookInformation().GetBookType()
    book_filter_id=[]
    selectedType=[]
    if request.method=='POST':
        for bk_type in book_type:
            #name=request.POST.get(str(bk_type.id))   
            #book_filter_id.append(name)
            book_filter_id=request.POST.getlist('book_type')
            
    if(book_filter_id.__len__()>0):
           userbooks=Business.BookInformation().GetUsersBook(book_type_id=book_filter_id)
           #c['len']=book_filter_id.__len__()
           c['FilterList']=Business.BookInformation().GetBookType(book_filter_id)
    else:
        userbooks=Business.BookInformation().GetUsersBook()
    c['booktypes']=book_type#Business.BookInformation().GetBookType()
    paginator = Paginator(userbooks,3)
    page = request.GET.get('page')
    try:
        books= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages) 
    c['books']=books
    return render_to_response('Home.html',context=c,context_instance=RequestContext(request))  
@login_required
def BookRating(request,book_id):
    if request.method=='POST':
        rating=request.POST.get('rating_'+str(book_id))
        Business.BookInformation().bookRating(book_id, rating,user_id=request.session['user_name'])
        return redirect(reverse('Review.Home'))  
@login_required
def AddReview(request,book_id):
    if request.method=='POST':
        review=request.POST['review']
        user_id=request.session['user_name']
        Business.BookInformation().AddReview(book_id,user_id,review)
        return HttpResponseRedirect("/BookInfo/%s" % book_id)
import json
@login_required
def LikeReview(request,review_id,book_id):
    review=Review.objects.filter(id=review_id)
    review=Like(review_id=Review.objects.get(id=review_id),user_id=UserInfo.objects.get(user_name=request.session['user_name']),like=1)
    review.save()   
    return HttpResponseRedirect("/BookInfo/%s" % book_id);
@login_required    
def DisLikeReview(request,review_id,book_id):
    review=Review.objects.filter(id=review_id)
    review=DisLike(review_id=Review.objects.get(id=review_id),user_id=UserInfo.objects.get(user_name=request.session['user_name']),dislike=1)
    review.save()   
    return HttpResponseRedirect("/BookInfo/%s" % book_id);

def About(request):
    return render(request,'About.html')

def Contact(request):
    return render(request,'ContactUs.html')

def bookUpload(request):
    if request.method=='POST':
        book_id=request.POST['book_id']
        #fl=request.FILES['bookfile']
        fl1=request.FILES['bookfilesoft']
        BookInformation().SaveBook(book_id=book_id,user_id=request.session['user_name'], book=fl1)
        return HttpResponseRedirect("/BookInfo/%s" % book_id);
     
    
             

        



             
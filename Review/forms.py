'''
Created on Mar 7, 2016

@author: sumit
'''
from django import forms
from Review.models import BookInfo,BookInfo, BookType
from django.core.exceptions import ValidationError
rate=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]
bktype=[]
for ty in BookType.objects.all():
    bktype.append((ty.id,ty.type))
class SearchBook(forms.Form):
    searchBox=forms.CharField(required=True,label='',max_length=200, widget=forms.TextInput(attrs={'required':True,'class':'textbox','placeholder':'Book Name','size':"40"}))
    
class BookInfoForm(forms.Form):
    name=forms.CharField(required=True,label='Name',max_length=200, widget=forms.TextInput(attrs={'required':True,'class':'textbox','placeholder':'Book Name','size':"45"}))
    type=forms.ChoiceField(label='Type',choices=bktype,widget=forms.Select(attrs={'required':True,'class':'selectbox'}))
    description=forms.CharField(label='Description',required=True,widget=forms.Textarea(attrs={'required':True,'class':'textbox','placeholder':'Description','rows':'3','cols':'50'}))
    image=forms.ImageField(label='Image',required=True)
    review=forms.CharField(label='Review',required=True,widget=forms.Textarea(attrs={'required':True,'class':'textbox','placeholder':'Review','rows':'2','cols':'50'}))
    rating=forms.ChoiceField(label='Rating',choices=rate,widget=forms.Select(attrs={'required':True,'class':'selectbox'}))
    
    def clean_image(self):
        return self.cleaned_data['image']
    def clean_description(self):
        des=self.cleaned_data['description']
        if len(des.split(' '))>=50:
            return des
        else:
            raise forms.ValidationError(('Atleast 50 word')) 
        
    def clean_name(self):
        name=self.cleaned_data['name']
        try:
            BookInfo.objects.get(book_name=name)
            raise forms.ValidationError(('Book Already exits'))
        except:
             return name
    
    def clean_review(self):
        des=self.cleaned_data['review']
        if len(des.split(' '))>=20:
            return des
        else:
            raise forms.ValidationError(('Atleast 20 word'))         


class ReviewForm(forms.Form):
    review=forms.CharField(required=True,widget=forms.Textarea(attrs={'required':True,'class':'textbox','placeholder':'Description','rows':'2','cols':'105','id':"Review_Text"}))
     
    def clean_review(self):
        des=self.cleaned_data['review']
        if len(des.split(' '))>=20:
            return des
        else:
            raise forms.ValidationError(('Atleast 20 word'))   
        
class Book(forms.Form):
    file=forms.FileField(label='',required=True,widget=forms.FileInput(required=True))
       
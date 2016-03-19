'''
Created on Mar 8, 2016

@author: sumit
'''
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from validate_email import validate_email
from django.utils.safestring import mark_safe
from __builtin__ import True
from email import email
from Review.models import UserInfo


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))



class  NewUserForm(forms.Form):
    name=forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'required': True,'class':'formCss','placeholder':'Name'}))
    email=forms.EmailField(required=True,max_length=200,widget=forms.EmailInput(attrs={'required': True,'class':'formCss','placeholder':'email'}))
    password=forms.CharField(required=True,max_length=200,widget=forms.PasswordInput(attrs={'required': True,'class':'formCss','placeholder':'Password'}))
    conpassword=forms.CharField(required=True,max_length=200,widget=forms.PasswordInput(attrs={'required': True,'class':'formCss','placeholder':'Password'}))
    
    #privilege=forms.ChoiceField(choices=USER_PRIVILEGES,widget=forms.RadioSelect(renderer=HorizontalRadioRenderer),initial='user')
    def clean_email(self):  
        email=self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise forms.ValidationError('email already exit')
        except User.DoesNotExist:
            return email
    '''    
    def clean_password(self):
        password=self.cleaned_data['password']
        confirm_password=self.cleaned_data['confirm_password']
        if password==confirm_password:
            return password,confirm_password
        else:
            raise forms.ValidationError(' both passwords are not same')
        
    def save(self, commit=True):        
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
             user.is_active = False # not active until he opens activation link
             user.save()
        return user
    '''    
       


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200,widget=forms.EmailInput(attrs={'class':'formCss','placeholder':'email','required': True}),required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'formCss','placeholder':'password','required': True}),required=True)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=200,label='Email',widget=forms.EmailInput(attrs={'class':'formCss','placeholder':'email','required': True}),required=True)
    
    def clean_email(self):
        try:
            email=self.cleaned_data['email']
            User.objects.get(email=email)
            UserInfo.objects.get(user_name=email)
            return email
        except:
            raise forms.ValidationError('Email Does not exixt')


class UserPasswordResetForm(forms.Form):
    new_password=forms.CharField(required=True,max_length=200,widget=forms.PasswordInput(attrs={'required': True,'class':'formCss','placeholder':'Password'}))
    confirm_password=forms.CharField(required=True,max_length=200,widget=forms.PasswordInput(attrs={'required': True,'class':'formCss','placeholder':'Password'}))
    
            
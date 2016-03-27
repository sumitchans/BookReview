from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
# Create your views here.
from django.core.mail import send_mail
from django.http import *
from .forms import *
from django.shortcuts import redirect,render
from django.contrib.auth import *
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
import json
from django.core.urlresolvers import reverse
from .services import *

#Create your views here.
def Login(request):
    if request.method=='GET':
        registerform=NewUserForm()
        loginform=LoginForm()
        return render_to_response("Login.html",{'loginform':loginform,'registerform':registerform},RequestContext(request))
def user_login(request):
    next=request.REQUEST.get('next')
    if request.method=='POST':
        loginform=LoginForm(data=request.POST)
        if loginform.is_valid():
            email=loginform.cleaned_data['email']
            password=loginform.cleaned_data['password']
            user=authenticate(username=email,password=password)
            if user is not None and user.is_active:
                login(request,user)
                request.session['user_name']=email
                request.session['is_logged_in']=True
                if next:
                    return HttpResponseRedirect(next)
                else:
                    return redirect(reverse('Review.Home'))
            else:
                return render_to_response("Login.html",{'loginform':LoginForm(),'registerform':NewUserForm(),'ErrorMsg':'Wrong Credentials'},RequestContext(request))

@require_http_methods(["POST"])        
def user_register(request):
    if  request.method=='POST':
        registerform=NewUserForm(data=request.POST)       
        if registerform.is_valid():
            name=registerform.cleaned_data['name']
            email=registerform.cleaned_data['email']
            password=registerform.cleaned_data['password']
            confirm_password=registerform.cleaned_data['conpassword']
            user=UserRegistration().register(name,email,password,confirm_password)
            if user is not False:
                user=authenticate(username=email,password=password)
                login(request,user)
                request.session['user_name']=email
                request.session['is_logged_in']=True
                return redirect(reverse('Review.Home'))
                #return render_to_response('Welcome.html',{'user_logged_in':False})
            else:
                return redirect(reverse('accounts.login'))
        else:
            return render_to_response("Login.html",{'loginform':LoginForm(),'registerform':NewUserForm(),'ErrorMsg':'User Already Exists Login'},RequestContext(request))
@login_required
def reset(request):
    if request.method=='GET':
        return render_to_response('PasswordReset.html',{'form':UserPasswordResetForm()},RequestContext(request))
    if request.method=='POST':
        passform=UserPasswordResetForm(data=request.POST)
        if passform.is_valid():
            p1=passform.cleaned_data['new_password']
            p2=passform.cleaned_data['confirm_password']
            if p1==p2:
                username=request.session['user_name']
                UserInformation(request.session['user_name']).reset(p1,username)
                return render_to_response('PasswordReset.html',{'ErrorMsg':'Password successfully change','form':UserPasswordResetForm()},RequestContext(request))
            else:
                return render_to_response('PasswordReset.html',{'ErrorMsg':'Both password should same','form':UserPasswordResetForm()},RequestContext(request))
        

def forgot_passowrd(request):
    if request.method=='GET':
        return render_to_response('ForgotPassword.html',{'forgotform':ForgotPasswordForm()},RequestContext(request))            
    if request.method=='POST':
        forgotform=ForgotPasswordForm(data=request.POST)
        if forgotform.is_valid():
            email=forgotform.cleaned_data['email']
            print email
            p1=generate_random_password()
            UserInformation(email).reset(p1,email)
            msg='Hi User\n Your new Password is %s' % p1
            try:
                send_mail('New Password',msg,'bc604391@gmail.com',[email], fail_silently=False)
            except:
                print "email send failed"
            finally:    
                return redirect(reverse('accounts.login'))
        else:
            return render_to_response('ForgotPassword.html',{'forgotform':forgotform},RequestContext(request))
          
def user_logout(request):
    logout(request);
    return redirect(reverse('Review.Home'))
    
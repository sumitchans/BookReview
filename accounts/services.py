'''
Created on Mar 9, 2016

@author: sumit
'''
from django.contrib.auth.models import User
from Review.models import UserInfo
import string
import random 
from string import ascii_lowercase,ascii_uppercase
from email import email

class UserRegistration(object):
        
    def register(self,user_name,email,password,confirm_password):
        try:
            user=UserInfo(user_name=email,name=user_name,password=password, confirm_password=confirm_password)
            user.save()
            user=User.objects.create_user(email, email, password)
            user.is_staff=True
            user.first_name=user_name
            user.is_active=True
            user.is_superuser=False
            user.save()
            return user
        except:
            return False
class UserInformation(object):
    name=None
    email=None
    password=None
    def __init__(self,user_name):
        user=UserInfo.objects.filter(user_name=user_name).values_list()
        if user.count()!=0:
            self.name=user[0][1]
            self.email=user[0][0]
            self.password=user[0][2]
        else:
            return None
    def reset(self,pa1,username):
        user=UserInfo.objects.get(user_name=username)
        user.password=pa1;
        user.confirm_password=pa1
        user.save()
        user=User.objects.get(email=username)
        user.set_password(pa1)
        user.save()
def generate_random_password():
    dt=''
    for i in range(0,10):
         dt=dt+(random.choice(ascii_lowercase+ascii_uppercase))
    return dt
        

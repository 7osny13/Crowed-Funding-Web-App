# from audioop import reverse
from calendar import c
from distutils.command.build_scripts import first_line_re
from email import message
import email
from multiprocessing import context
from os import link
import re
from tracemalloc import stop
from unittest.result import failfast
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from matplotlib.pyplot import get
from platformdirs import user_config_dir
from requests import request
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
import validate_email as ve
from django.core.mail import send_mail 
from django.views import View
from django.utils.encoding import force_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from datetime import datetime, timedelta



# def insert_img(request):
#     context={}
#     ff=ImgForm()
#     context['form']=ff
#     if request.method == 'POST':

#         # form = ImgForm(request.POST, request.FILES)
#         us=Img(img=request.FILES['img'],name=request.POST['name'])
#         # if ff.is_valid():
#         us.save()
#         return render(request, 'ins_img.html', {'form': ff})
#         # else:
#         #     print(ff.errors)
#         #     print('error')


    # return render(request, 'ins_img.html', {'form': ff})
    
def logino(request):
   if(request.method=='GET'):
    return render(request, 'login.html')
   
   else:
      print(request.POST['username'],' ',request.POST['password'])

      user=authenticate(request,username=request.POST['username'],password=request.POST['password'],is_active=True)
      print(user)
       
      if user :
         login(request,user)
         request.session['username']=request.POST['username']
       
         return HttpResponseRedirect( 'logino')
          
      else:
        
         return HttpResponseRedirect('reg/')
   
def Registeration(request):
    context={}
    ff=RegisterForm(request.POST or None)
    context['form']=ff
    if request.method == 'POST':
        # urname=request.POST['username']
        if ff.is_valid():
            
            userr=User.objects.create_user(username=request.POST['username'],password=request.POST['password'],
            email=request.POST['email'],first_name=request.POST['firstname'],last_name=request.POST['lastname'],is_active=False)
            userr.save()
            UserProfile.objects.create(user_id=User.objects.get(username=request.POST['username']).id,
            user_phone=request.POST['user_phone'], user_facebook=request.POST['user_facebook'],
            user_country=request.POST['user_country'], user_birthday=request.POST['user_birthday'])
            # uidb64= urlsafe_base64_encode(force_bytes(User.objects.get(username=request.POST['username']).id))
            # uidb64=urlsafe_base64_encode(force_bytes(userr.pk)) 

            # domain=get_current_site(request).domain
            # link=reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(userr)})
            # activate_url= 'http://'+domain+link
            # email_body= 'HI '+ request.POST['username'] +'Please click on the link to activate your account: '+domain+link
            current_site=get_current_site(request)
            email_body={
                'user':userr,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(userr.pk)),
                'token': token_generator.make_token(userr),

            }
            link=reverse('activate',kwargs={
                'uidb64':urlsafe_base64_encode(force_bytes(userr.pk)),'token':token_generator.make_token(userr)})
            activate_url='http://'+email_body['domain']+link
            email_subject='Activate Your Account'
            # email=message.EmailMessage(email_subject,activate_url,to=[email_body['user'].email])
            # email.send(fail_silently=False)
            print(request.POST['email'])
            send_mail('Fund Time Account Activation',activate_url,'stg1@localhost',[request.POST['email']],fail_silently=False)
            messages.success(request, 'Account created successfully \n Please Check your email to activate your account \n within 24 hours')
            # return render(request, 'register.html')
            return render(request, 'login.html', {'form': ff})

        
        # if not request.Post['user_phone'].startswith('20') and len(request.Post['user_phone'])<13 and len(request.Post['user_phone'])>10:
        #     messages.error(request,'not valid Egyptian number')
        #     # return  HttpResponseRedirect('register.html')
    
        
        
    return render(request, "register.html", context)
    # return render(request,'register.html',{'form':ff})
        
class VerificationLink(View):
    def get(self, request,uidb64,token):
        try:
            idd=force_str(urlsafe_base64_decode(uidb64))
            # print(idd+'iddddd')
            user3=User.objects.get(id=idd)
            # print(user3.username)
            date1=datetime.now()
            date2=user3.date_joined 
            date3=str(date2)
            date4=date3[0:18]
            date5=datetime.strptime(date4,'%Y-%m-%d %H:%M:%S')
            # date_format_str = '%d/%m/%Y %H:%M:%S'
            # start = date1.strptime("%Y-%m-%d %H:%M:%S")
            # print(start + 'strat')
            # end =   datetime.strptime(date2, date_format_str)
            # print(end + 'end')
            diff=date1-date5
            # print(diff)
            # print(timedelta(days=1))
            if diff>timedelta(days=1):
                return redirect('login.html' + '?message='+ 'Link expired')
            # print(user3.username + ' ' + user3.password)
            if not token_generator.check_token(user3,token):
                messages.error(request,'Link is not valid')
                # print(User.username + ' is not a valid')

                return redirect('login')
            if user3.is_active:
                messages.info(request,'Account already activated')
                print(User.username + ' is already activated')
                return redirect('login')
             
                # else:
            user3.is_active=True
            user3.save()
            messages.success(request,'Account activated successfully')
            return redirect('login')
        except Exception as e:   
            pass
        return redirect('login')
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


        


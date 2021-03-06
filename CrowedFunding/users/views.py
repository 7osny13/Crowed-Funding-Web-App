# from audioop import reverse
from calendar import c
from cmath import e
from distutils.command.build_scripts import first_line_re
from email import message
import email
from multiprocessing import context
from os import link
import os
import re
from tracemalloc import stop
from unittest.result import failfast
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from matplotlib.pyplot import get
from platformdirs import user_config_dir
from requests import request

from projects.models import Project, ProjectDonation
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
from datetime import datetime, timedelta, date



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
    return render(request, 'accounts/login.html')
   
   else:
 
      user=authenticate(request,username=request.POST['username'],password=request.POST['password'],is_active=True)
        
      if user :
         login(request,user)
         request.session['username']=request.POST['username']
       
        #  return render( request, 'accounts/main.html' )
         return HttpResponseRedirect('/projects/projects_all')

          
      else:
         messages.error(request, 'Account Not Found')

        #  return HttpResponseRedirect('logino')
         return HttpResponseRedirect('addo')


def profile_edit(request):
    if(request.method=='POST'):
        #update UserProfile
        userm=User.objects.get(username=request.session['username'])
        if userm:
            userp=UserProfile.objects.filter(user_id=userm.id)
            if request.POST['password']!=request.POST['confirm_password']:
                
                messages.error(request, 'Password Not Match')
                return render( request, 'profile/editprofile.html')
            if len(request.POST['password']) < 8:
                messages.error(request, 'Password Too short ')
                return render( request, 'profile/editprofile.html')
            if len(str(request.POST['user_phone'])) < 12:
                messages.error(request, 'Phone Number Too short ')
                return render( request, 'profile/editprofile.html')
            if len(str(request.POST['user_phone'])) > 13:
                messages.error(request, 'Phone Number Too long ')
                return render( request, 'profile/editprofile.html')
            try:
                phone = int(request.POST['user_phone'])
            except ValueError:
                messages.error(request, 'Phone Number is not a valid number')
                return render( request, 'profile/editprofile.html')
            user_birthday = request.POST['user_birthday']
            date22=date(int(user_birthday[0:4]), int(user_birthday[5:7]), int(user_birthday[8:10]))
            if date22 > date.today():
                messages.error(request, 'Birthday is not valid')
                return render( request, 'profile/editprofile.html')
            if userp.count() > 0:
                userp=userp[0]
                userp.user_phone=request.POST['user_phone']
                userp.user_birthday=request.POST['user_birthday']
                userp.user_facebook=request.POST['user_facebook']
                #update User password

                userm.first_name=request.POST['first_name']
                userm.last_name=request.POST['last_name']
                userm.set_password(request.POST['password'])
                if len(request.FILES)!=0:
                    # print(str(userp.user_img))
                    old='media/'+ str(userp.user_img)
                    if os.path.exists(old):
                        os.remove( old)
                    userp.user_img=request.FILES['user_img']
                else:
                    if userp.user_img!='/img/default.png':
                       userp.user_img=userp.user_img
                

                userp.save()
                userm.save()

                return HttpResponseRedirect('profile')
            else:
                return HttpResponseRedirect('profile')
    else:
       if ('ohaio' in request.session):

            if ('username' in request.session):

                if User.objects.filter(username=User.objects.get(username=request.session['username'])).count() > 0:
                    context={}
                    context['title']='profile'
                    userm=User.objects.get(username=request.session['username'])
                    context['user']=userm
                    # filter UserProfile by userm.id
                    
                    userp=UserProfile.objects.filter(user_id=userm.id)
                # filter UserProfile by user
                    if userp.count() > 0:
                        context['userp']=userp[0]
                        # print(userp[0].user_birthday)
                    del request.session['ohaio']
                return render(request, 'profile/editprofile.html',context)
    return redirect('login')

def profile_view(request):
    # try:
    
        if ('username' in request.session) :
         if User.objects.filter(username=User.objects.get(username=request.session['username'])).count() > 0:
            context={}
            context['title']='profile'
            userm=User.objects.get(username=request.session['username'])
            context['user']=userm
            # filter UserProfile by userm.id

             
            userp=UserProfile.objects.filter(user_id=userm.id)
           # filter UserProfile by user
            if userp.count() > 0:
                context['userp']=userp[0]
                # print(userp[0])
            request.session['ohaio']=True
            # context projectdonation of the user

            context['donations'] =ProjectDonation.objects.filter(user=userm.id)
            context['projects'] =Project.objects.filter(user=userm.id)
            context['prosum'] =Project.objects.filter(user=userm.id).count()
            context['donsum'] =ProjectDonation.objects.filter(user=userm.id).count()
            


            return render(request,'profile/profile.html',context)

         
        # profile=UserProfile.objects.all()
        # profile_main=UserProfile.objects.filter(user=request.user)
        # # for Trainee in trainees:
        # #     print(Trainee.id,Trainee.name,Trainee.phone,Trainee.address,Trainee.cource)
        
        # # return HttpResponse('listo')
        # context={}
        # context['title']='trrainee'
        # context['UserProfile']=UserProfile


        # return render(request,'index.html',context)
        else:
         return HttpResponseRedirect('logino')
    # except Exception as e:
    #      return HttpResponseRedirect('logino')
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
            user_country=request.POST['user_country'], user_birthday=request.POST['user_birthday'],user_img='img/default.png')
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
            return render(request, 'accounts/login.html', {'form': ff})

        
        # if not request.Post['user_phone'].startswith('20') and len(request.Post['user_phone'])<13 and len(request.Post['user_phone'])>10:
        #     messages.error(request,'not valid Egyptian number')
        #     # return  HttpResponseRedirect('register.html')
    
        
    else:
        try:

            del request.session['username']
    
        except:
            pass
        return render(request, 'accounts/register.html', context)  
    return render(request, "accounts/register.html", context)

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
        return HttpResponseRedirect( 'logino')


        


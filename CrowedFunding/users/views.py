from calendar import c
from email import message
from multiprocessing import context
import re
from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages

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

def Registeration(request):
    context={}
    ff=RegisterForm()
    context['form']=ff
    if request.method == 'POST':
        if User.objects.filter(username=request.POST['username']).count() > 0:
            messages.error(request,'username already registered ')
            return
        if request.POST['password'] != request.POST['password_confirmation']:
            messages.error(request,'username already registered ')
            return
        phona=request.Post['user_phone']
        if  phona.startswith('20') and len(phona)<13 and len(phona)>10:
            messages.error(request,'not valid Egyptian number')
            return
        # validate email 
        # validate birthday
        



        


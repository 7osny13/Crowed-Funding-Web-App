from audioop import avg, avgpp
from calendar import c
from datetime import date, datetime
from email import message
from re import U
import re
from tkinter import E, N
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from matplotlib.pyplot import get
from requests import post

from users.models import UserProfile
from .models import *

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache, cache_control
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


# Create your views here.
 

@login_required()
@never_cache

def add_project(request):

    if request.method =='POST':
        try:
            rr=request.session['username']
        
        except:
            messages.error(request, 'You are not logged in')
            return HttpResponseRedirect('/users/login')
        tagoo=request.POST['tagoo']
        
        tagoo2=tagoo.split(",")
        tagoo3=[]
        for i in tagoo2:
            if i not in tagoo3:
                tagoo3.append(i)

        prop=Project()
        userm=User.objects.get(username=request.session['username'])
        prop.name=request.POST['project_name']
        prop.description=request.POST['project_description']
        prop.goal=request.POST['project_goal']
        prop.image_thumb=request.FILES['project_image_thumb']
        prop.created_at=datetime.today()
        prop.started_at=request.POST['project_started_at']
        prop.ended_at=request.POST['project_ended_at']
        # project_is_active=request.POST['project_is_active']
        # project_images=request.FILES['project_images']
        # project_rating=request.POST['project_rating']
        prop.user=userm 

        prop.cat_related=CategoryMain.objects.filter( id=request.POST['project_cat_related'])[0]
        print(prop.cat_related)
        # project_actual_goal=request.POST['project_actual_goal']
        prop.actual_goal=0
        if not  CategoryMain.objects.filter( id=request.POST['project_cat_related'])[0]:
            messages.error(request, 'Category not found')
            return render(request, 'addproject.html')
        try:
                prop.goal = int(request.POST['project_goal'])
        except ValueError:
                messages.error(request, 'Invalid Number Of target Price')
                return render( request, 'profile/editprofile.html')
        if Project.objects.filter(name=prop.name,user=prop.user).exists():
            messages.error(request, 'Project already exists at your collection')
            return render(request, 'addproject.html')
        else:
           
            prop.save() #Project.objects.create(name=project_name,description=project_description,goal=project_goal,created_at=project_created_at,started_at=project_started_at,ended_at=project_ended_at,is_active=True,image_thumb=project_image_thumb,rating=0,cat_related=1,actual_goal=project_actual_goal,user=project_user)
            mmimage=MultiImages()
            mmimage.project=Project.objects.last()
            # print(mmimage.project," xxxxxxxxxxxxxxxxxxxxx   ",request.FILES.getlist('project_images'))
            mmimage.image=request.FILES.getlist('project_images')
            for i in mmimage.image:
              MultiImages.objects.create(image=i,project=mmimage.project)
            for i in tagoo3:
                if i:
                    Tago.objects.create(tagg=i,project=Project.objects.filter(name=prop.name,user=prop.user)[0])
            messages.success(request, 'Project added successfully , Try add more!!')
        return render(request, 'addproject.html')
    else:
        try:
            rr=request.session['username']
        
        except:
            messages.error(request, 'You are not logged in')
            return HttpResponseRedirect('/users/login')
        return render(request, 'addproject.html')
@never_cache
def project_all(request):
    context={}
    context['projects']=Project.objects.all()
    projects=Project.objects.all()
    paginatoro = Paginator(projects, 12)
    pagenum = request.GET.get('page')

    page = paginatoro.get_page(pagenum)
    
    context['page']=page
    context['counto']= (projects.count()//12)+1
    if request.method=='GET':

        return render(request, 'project.html',context)
# @never_cache
@login_required()
def project_detail(request,id):
    if ('username' in request.session) :
        context={}
        context['project']=Project.objects.get(id=id)
        # context['images']=MultiImages.objects.filter(project=context['project'])
        # context['tags']=Tago.objects.filter(project=context['project'])
        context['comments']=Comments.objects.filter(project=context['project'])
        context['user']=User.objects.get(username=request.session['username'])
        #context['projectavgrating']=ProjectRating.objects.filter(user=context['user'].id)#.aggregate(avgpp('rating'))
        vv=[]
        vv2=ProjectRating.objects.filter(project=context['project'].id)
        ti= 0
        sui=0
        if vv2:
            for i in vv2:
                ti += 1
                sui+=i.rating
          
            context['projectavgrating']=sui//ti
        else:
            context['projectavgrating']=0
        don=[]
        don2=ProjectDonation.objects.filter(project=context['project'].id)
        if don2:
            for i in don2:
                don.append(i.donation)
            context['projectdonation']=sum(don)
        else:
            context['projectdonation']=0
        if (sum(don)/context['project'].goal)<.25 and context['project'].user==User.objects.get(username=request.session['username']):
           print(sum(don)/context['project'].goal)
           context['project_status']='danger'
        else:
            context['project_status']='success'


        # got category related to project
        context['cat_related']=(CategoryMain.objects.filter(id=context['project'].cat_related_id)[0].name) 
        relatedprojects=Project.objects.filter(cat_related=context['project'].cat_related_id)
        arr1=[]
        ii=0
        for i in relatedprojects:
            ii+=1
            if ii==7:
                break
            else:
                arr1.append(i)
        context['relatedprojects']=arr1
        context['allprojects']=Project.objects.all()

        context['count']=Comments.objects.filter(project=context['project']).count()
        context['commentuserimage']=UserProfile.objects.filter(user_id=context['user'].id)
        context['projectimages']=MultiImages.objects.filter(project=context['project'])
        # gen num of donation of project
        context['projectdonation']=ProjectDonation.objects.filter(project=context['project'].id).count()
          # get user image of comment
    
        if request.method=='GET':
            return render(request, 'projectview.html',context)
        elif request.method=='POST':
            if request.POST['comment']:
                Comments.objects.create(comment=request.POST['comment'],project=context['project'],user=context['user'])
            return render(request, 'projectview.html',context)
    else:
          
        return HttpResponseRedirect('logino')


def project_det(requset):
    return HttpResponseRedirect('projects_all')

@never_cache
@login_required()
def rating(request,id):
    if request.method=='POST':
       prrat=ProjectRating()
       prrat.project=Project.objects.get(id=id)
       prrat.user=User.objects.get(username=request.session['username'])
       prrat.rating=request.POST['divcheckbox']
       if not prrat.rating=='val':
            prrat.project=request.POST['prid']
            prrat.user=request.POST['userid']
            prrat.created_at=datetime.today() 
            if ProjectRating.objects.filter(project=prrat.project,user=prrat.user).exists():
                        messages.error(request, 'You have already rated this project')
                        return HttpResponseRedirect('/projects/project_detail/'+id)
            else:
                        prrat.save()
                        messages.success(request, 'Rating added successfully')
                        return HttpResponseRedirect('/projects/project_detail/'+id)
       else:
            messages.error(request, 'Invalid rating')
            return HttpResponseRedirect('/projects/project_detail/'+id)
    else:
        return HttpResponseRedirect('/projects/project_detail/'+id)
		

  

@never_cache
@login_required()
def comment(request,id):
    if request.method=='POST':
        com=Comments()
        com.comment=request.POST['comment']
        com.project=Project.objects.get(id=id)
        com.user=User.objects.get(username=request.session['username'])
        com.created_at=datetime.today()
        if len(com.comment)>0:
            if Comments.objects.filter(project=com.project,user=com.user).exists():
                messages.error(request, 'You have already commented this project')
                return HttpResponseRedirect('/projects/project_detail/'+id)
            else:
                com.save()
                messages.success(request, 'Comment added successfully')
                return HttpResponseRedirect('/projects/project_detail/'+id)
        else:
            messages.error(request, 'Invalid comment')
            return HttpResponseRedirect('/projects/project_detail/'+id)
    else:
        return HttpResponseRedirect('/projects/project_detail/'+id)

@never_cache
@login_required()
def project_report(request,id):
    if request.method=='POST':
        prr=ProjectReport()
        prr.project=id
        prr.user=request.POST['userid']
        prr.created_at=datetime.today()
        if ProjectReport.objects.filter(project=prr.project,user=prr.user).exists():
            messages.error(request, 'You have already reported this project')
            return HttpResponseRedirect('/projects/project_detail/'+id)
        else:
            prr.save()
            messages.success(request, 'Report added successfully')
            return HttpResponseRedirect('/projects/project_detail/'+id)
    else:
        return HttpResponseRedirect('/projects/project_detail/'+id)

@never_cache
@login_required()
def comment_report(request,id):
    if request.method=='POST':
        comr=CommentsReport()
        comr.comment=request.POST['commentid']
        comr.user=request.POST['userid']
        comr.created_at=datetime.today()
        comr.project=request.POST['prid']
        if CommentsReport.objects.filter(comment=comr.comment,user=comr.user).exists():
            messages.error(request, 'You have already reported this comment')
            return HttpResponseRedirect('/projects/project_detail/'+id)
        else:
            comr.save()
            messages.success(request, 'Report added to comment  successfully')
            return HttpResponseRedirect('/projects/project_detail/'+id)
    else:
        return HttpResponseRedirect('/projects/project_detail/'+id)







@never_cache
def logout(request):
    try:

        del request.session['username']
    
    except:
        pass

    return redirect('/users/login')
def error_404(request,exception):
    return render(request, '404.html')
def error_500(request):
    return render(request, '404.html')

@never_cache
@login_required()
def project_delete(request,id):
    if request.method=='POST':
        pr=Project.objects.get(id=id)
        pr.delete()
        messages.success(request, 'Project deleted successfully')
        return HttpResponseRedirect('/projects/projects_all')
    else:
        return HttpResponseRedirect('/projects/projects_all')
@never_cache
@login_required()
def project_donate(request,id):
    if request.method=='POST':
        pr=Project.objects.get(id=id)
        prd=ProjectDonation()
        # get user id from session username
        prd.user=request.POST['userid']

        prd.project=id
 
        userbalance=UserProfile.objects.get(user_id=request.POST['userid'])
        
        prd.donation=request.POST['amount']
        prd.created_at=datetime.today()
        if prd.donation.isdigit():
            if int(prd.donation)>0:
                
                if int(userbalance.user_balance)>=int(pr.goal):

                    if int(prd.donation)>int(pr.goal):
                        messages.error(request, 'Amount is greater than goal')
                        return HttpResponseRedirect('/projects/project_detail/'+id)
                    else:
                        userbalance.user_balance=int(userbalance.user_balance)-int(prd.donation)
                        userbalance.save()
                        prd.save()
                        messages.success(request, 'Donation added successfully')
                        return HttpResponseRedirect('/projects/project_detail/'+id)
                else:
                    messages.error(request, 'Insufficient balance')
                    return HttpResponseRedirect('/projects/project_detail/'+id)
            else:
                messages.error(request, 'Invalid amount')
                return HttpResponseRedirect('/projects/project_detail/'+id)
        
        else:
            messages.error(request, 'Invalid amount')
            return HttpResponseRedirect('/projects/project_detail/'+id)
    else:
        return HttpResponseRedirect('/projects/project_detail/'+id)

@never_cache
def searching(request):
    if request.method=='POST':
        search=request.POST['search']
        # search="sdf"
        # find in tags and projectnames like search word
        proj=Project.objects.all()
        context={}
        context['projects']=Project.objects.filter(name__contains=search).all  #|Q(project_name__icontains=search))
        tg1=Tago.objects.filter(tagg__contains=search).all()
        tg_arr=[]
        for tg in tg1:
            tg_arr.append(tg.project_id)
        print(tg_arr)
        context['projecttag']=Project.objects.filter(id__in=tg_arr)

        #context['projecttag']=Project.objects.filter(id=tg1).all()    #|Q(tag_name__icontains=search))
             

        if Project.objects.filter(name__contains=search).exists():
            return render(request,'search.html',context)
        else:
            messages.error(request, 'No project found')
        return HttpResponseRedirect('/projects/projects_all')
    else:
        messages.error(request, 'No project found')
 
        return HttpResponseRedirect('/projects/projects_all')
    # else:
    #     if Project.objects.filter(title__icontains=search).exists():
    #         return HttpResponseRedirect('/projects/projects_all')
    #     else:
    #         messages.error(request, 'No project found')
    #         return HttpResponseRedirect('/projects/projects_all')

@never_cache
def project_filter_by_cat(request):
    if request.method=='POST':
        cat=request.POST['filterss']
        if cat=='all':
            return HttpResponseRedirect('/projects/projects_all')
        else:
            context={}
            context['cat']=CategoryMain.objects.get(id=cat)
            context['projects']=Project.objects.filter(cat_related_id=context['cat'])
            
            return render(request,'filter.html',context)
    else:
        return HttpResponseRedirect('/projects/projects_all')

 
 
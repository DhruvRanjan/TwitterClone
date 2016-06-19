from django.shortcuts import render, redirect, get_object_or_404

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse

from socialnetwork.models import *
from socialnetwork.forms import *

from django.utils import timezone
from django.db import transaction

from django.core import serializers

@transaction.atomic
def register_user(request):

    context = {}

    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'register.html', context)
    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        password=form.cleaned_data['password'])
    new_user.save()
    new_myUser = myUser(user=new_user, username=form.cleaned_data['username'])
    new_myUser.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)
    return redirect('profile')                                

@login_required
def global_stream(request):

    context = {}
    postData = Post.objects.all().order_by('post_date')
    postData = postData[::-1]
    context['posts'] = postData
    myUserInfo = myUser.objects.all()
    context['myUser'] = myUserInfo
    return render(request, 'global_stream.html', context)
    
@login_required
@transaction.atomic
def profile(request):

    context = {}
    userInfo = User.objects.filter(username=request.user.username)
    myUserInfo = myUser.objects.filter(username=request.user.username)
    postInfo = Post.objects.filter(user=request.user)
    postInfo = postInfo[::-1]
    context = {'users' : userInfo, 'posts' : postInfo, 'myUser' : myUserInfo}
    if request.method == 'GET':
        context['form'] = PostForm()
        return render(request, 'profile.html', context)
    form = PostForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'profile.html', context)
    
    new_post = request.user.post_set.create(post_text=form.cleaned_data['post_text'],
                                        post_date=timezone.now())
    new_post.save()
    return redirect('profile')

@login_required
@transaction.atomic
def profile_view(request, username):

    context = {}
    userInfo = User.objects.filter(username=username)
    myUserInfo = myUser.objects.filter(username=username)
    postInfo = Post.objects.filter(user=userInfo)
    postInfo = postInfo[::-1]
    context = {'users' : userInfo, 'posts' : postInfo, 'myUser' : myUserInfo}
    if request.method == 'GET':
        return render(request,'profile_view.html', context)
    current_myUser = myUser.objects.get(username=request.user.username)
    current_follower = myUser.objects.get(username=username)
    if 'follow' in request.POST:
        current_myUser.myuser_set.add(current_follower)
    elif 'unfollow' in request.POST:
        current_myUser.myuser_set.remove(current_follower)
    return render(request, 'profile_view.html', context)

@login_required
@transaction.atomic
def edit_profile(request):

    print request.FILES
    context = {}
    userInfo = User.objects.filter(username=request.user.username)
    myUserInfo = myUser.objects.filter(username=request.user.username)
    postInfo = Post.objects.filter(user=request.user)
    postInfo = postInfo[::-1]
    context = {'users' : userInfo, 'posts' : postInfo, 'myUser' : myUserInfo}
    if request.method == 'GET':
        context['form'] = editProfileForm()
        return render(request, 'edit_profile.html', context)
    form = editProfileForm(request.POST, request.FILES)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'edit_profile.html', context)
    if form.cleaned_data['first_name'] is not None and form.cleaned_data['first_name'] != "":
        userInfo.update(first_name = form.cleaned_data['first_name'])
    if form.cleaned_data['last_name'] is not None and form.cleaned_data['last_name'] != "":
        userInfo.update(last_name = form.cleaned_data['last_name'])
    if form.cleaned_data['age'] is not None:
        myUserInfo.update(age = form.cleaned_data['age'])
    if form.cleaned_data['bio'] is not None and form.cleaned_data['bio'] != "":
        myUserInfo.update(bio = form.cleaned_data['bio'])
    if form.cleaned_data['profile_picture']:
        #myUserInfo.update(profile_picture=request.FILES['profile_picture'])
        current_user = myUser.objects.get(username=request.user.username)
        #current_user.content_type = form.cleaned_data['profile_picture'].content_type
        current_user.profile_picture = form.cleaned_data['profile_picture']
        #current_user.profile_picture = request.FILES['profile_picture']
        current_user.save()
        myUser.save(current_user)
    '''if form.cleaned_data['profile_picture']:
       myUserInfo.content_type = form.cleaned_data['profile_picture'].content_type'''
    
    return redirect('profile')

def get_profile_picture(request, username):

    current_user = get_object_or_404(myUser, username=username)
    if not current_user.profile_picture:
        raise Http404
    return HttpResponse(current_user.profile_picture, content_type=current_user.content_type)

@login_required
def follower_stream(request):

    context = {}
    #myUserInfo = myUser.objects.filter(username=request.user.username)
    current_myUser = myUser.objects.get(username=request.user.username)
    print current_myUser
    current_set = current_myUser.myuser_set.all()
    current_set2 = []
    for i in current_set:
        current_set2 += [i.username]
    userData = User.objects.filter(username__in=current_set2)
    print len(userData)
    postData = Post.objects.all().order_by('post_date').filter(user__in=userData)
    postData = postData[::-1]
    context['posts'] = postData
    myUserInfo = myUser.objects.all()
    context['myUser'] = myUserInfo
    return render(request, 'follower_stream.html', context)

def get_posts_json(request):
    
    postData = Post.objects.all().order_by('post_date')
    postData = postData[::-1]
    response_text = serializers.serialize('json', postData)
    return HttpResponse(response_text, content_type='application/json')

def get_posts_xml(request):

    postData = Post.objects.all().order_by('post_date')
    postData = postData[::-1]
    context = { 'posts': postData }
    return render(request, 'posts.xml', context, content_type='application/xml')
    


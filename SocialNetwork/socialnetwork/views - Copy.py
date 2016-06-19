from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from socialnetwork.models import *
from socialnetwork.forms import *

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

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)
    return reditect('/profile/')                                

@login_required
def global_stream(request):

    postData = Post.objects.all().order_by('-date')
    return render(request, 'global_stream.html', postData)
    
@login_required
def profile(request):

    userInfo = User.objects.filter(user=request.user)
    return render(request, 'profile.html', userInfo)




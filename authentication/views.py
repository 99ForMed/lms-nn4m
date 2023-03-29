from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import NewUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from general.models import UcatStudent, UcatSectionInstance, UcatSection
import datetime

import json
# Create your views here.

def general_auth_view(request):
    context = {

    }
    return HttpResponse('testing')

def login_view(request):
    context = {
        'errors': []
    }
    if request.method == 'POST':
        # When they submit username and password
        try:
            username = User.objects.get(email = request.POST['email'])
        except:
            context['errors'].append("Email not found.")

        password = request.POST['password']
        if len(context['errors']) == 0: #(so far)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login-success/')
            else:
                context['errors'].append('invalid login')
                None
    
    context['current_user'] = str(request.user),
    context['is_authenticated'] = request.user.is_authenticated

    return render(request, 'login2.html', context)

def login_success_view(request):
    context = {

    }
    return redirect('/dashboard/')

def create_account_view(request):
    context = {
        'form_errors':[]
    }
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            new_student = UcatStudent(user = request.user, enrolment_date = datetime.datetime.now(), tasks = [])
            new_student.save()
            new_instance = UcatSectionInstance(student = UcatStudent.objects.get(user = request.user), section = UcatSection.objects.get(name = "Decision Making"), start_date = datetime.datetime.now().date(), current = True, skills_mastered = 0)
            new_instance.save()
            return redirect('account-created/')
            
        else:
            for field_errors in form.errors.get_json_data().values():
                for error in field_errors:
                    print(error['message'])
            context['form_errors'] = form.errors.get_json_data().values()
        
    form = NewUserForm()
    context['register_form'] = form
    
    return render(request, 'create_account.html', context)

def account_created_view(request):
    context = {

    }
    return redirect('/dashboard/')
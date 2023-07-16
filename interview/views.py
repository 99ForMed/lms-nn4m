import pytz
from datetime import datetime
from django.shortcuts import render, redirect

from .models import InterviewStudent
# Create your views here.

def interview_dashboard_view(request):
    sydney_tz = pytz.timezone('Australia/Sydney')
    sydney_time = datetime.now(sydney_tz)
    
    if 5 <= sydney_time.hour < 12:
        time_greeting = 'Good morning'
    elif 12 <= sydney_time.hour < 18:
        time_greeting = 'Good afternoon'
    else:
        time_greeting = 'Good evening'
    
    # Assuming there is a logged in user and the user has an associated InterviewStudent model
    user = request.user
    try:
        interview_student = InterviewStudent.objects.get(user = user)
    except:
        return redirect("/")

    interview_student = InterviewStudent.objects.get(user = user)
    title = 'Sir' if interview_student.gender == 'M' else 'Madam'
    context = {
        'day_of_week':'wednesday',
        'time_greeting': time_greeting, 
        'title': title
    }
    
    return render(request, 'interview-dashboard.html', context)

def live_class_view(request):
    context = {

    }
    return render(request, 'live-class.html', context)


def select_question_view(request):
    context = {
        'redirect_template':str(request.GET['type'])
    }
    return render(request, 'select_question.html', context)

def view_question_view(request):
    context = {
        
    }
    return render(request, 'view_question.html', context)
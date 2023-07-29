import pytz
from datetime import datetime
from django.shortcuts import render, redirect

from .models import InterviewStudent
# Create your views here.

from django.shortcuts import get_object_or_404
from .models import InterviewStudent
from pyzoom import request_tokens
import os

def link_zoom_view(request):
    client_id = os.getenv("APP_CLIENT_ID")
    redirect_uri = "https://lms.99formed.com/authenticate-zoom/"  # Replace with your redirect URL
    auth_url = f"https://zoom.us/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    return redirect(auth_url)

def zoom_callback_view(request):
    code = request.GET['code']
    user = request.user  # Assuming you have user authentication in place

    # Exchange the code for a token
    tokens = request_tokens(os.getenv("APP_CLIENT_ID"), os.getenv("APP_CLIENT_SECRET"), "YOUR_REDIRECT_URL", code)

    # Get the user's InterviewStudent record
    interview_student = get_object_or_404(InterviewStudent, user=user)

    # Save the tokens to the user's InterviewStudent record
    interview_student.zoom_access_token = tokens['access_token']
    interview_student.zoom_refresh_token = tokens['refresh_token']
    interview_student.save()

    # Redirect the user back to the dashboard or another page
    return redirect('interview_dashboard_view')


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

    try: 
        print(oauth_wizard("wpT5jz7rQ8W_SNbSp_13Q", "98RiygZI6ZlH26vWdc525ixKERJyTjH8", redirect_uri='https://lms.99formed.com/authenticate-zoom/'))
    except Exception as e:
        print(e)

    interview_student = InterviewStudent.objects.get(user = user)
    title = 'Sir' if interview_student.gender == 'M' else 'Madam'
    context = {
        'day_of_week':'wednesday',
        'time_greeting': time_greeting, 
        'title': title,
        'class_soon': False,
        'class': {}
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
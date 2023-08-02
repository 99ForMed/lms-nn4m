import pytz
from datetime import datetime
from datetime import datetime as dt
from django.shortcuts import render, redirect
from .models import InterviewStudent, InterviewClass
from Tutors.models import Tutor
from django.shortcuts import get_object_or_404
from pyzoom import request_tokens, ZoomClient
import os
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse, HttpResponseRedirect
from live_class.models import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def add_feedback_view(request, live_class_id):
    if request.method == "POST":
        author_username = request.POST.get('author')
        receiver_username = request.POST.get('receiver')
        content = request.POST.get('content')
        question_id = request.POST.get('question_id')

        author = get_object_or_404(User, username=author_username)
        receiver = get_object_or_404(User, username=receiver_username)
        question = Question.objects.all()[0]

        # create feedback
        feedback = Feedback(
            sender=author,
            receiver=receiver,
            Question=question,
            text=content,
        )
        feedback.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'This view only accepts POST requests.'})







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

# @live_class_required
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
        print(oauth_wizard(os.getenv("ZOOM_CLIENT_ID"), os.getenv("ZOOM_CLIENT_SECRET"), redirect_uri=os.getenv("ZOOM_REDIRECT_URL")))
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

    context['live_class'] = None

    try:
        # Get the interview class associated with the user
        interview_student = InterviewStudent.objects.get(user=request.user)
        interview_class = interview_student.interview_class
        # Find a live class associated with the interview class and is active
        live_class = LiveClass.objects.get(interview_class=interview_class, is_active=True)
        # If such a live class exists, update the context

        context['live_class'] = live_class
    except InterviewClass.DoesNotExist:
        print("Interview class doesn't exist")
        # Handle the case when the user is not associated with any interview class
        pass
    except LiveClass.DoesNotExist:
        print("Live class doesn't exist")
        # Handle the case when there is no active live class for the interview class
        pass
    context['link_zoom_uri'] = "https://zoom.us/oauth/authorize?response_type=code&client_id=wpT5jz7rQ8W_SNbSp_13Q&redirect_uri="+os.getenv("ZOOM_INITIAL_REDIRECT_SECURE")+"%3A%2F%2F"+os.getenv("host")+"%2Fzoom-start%2F"

    print(context['live_class'])
    
    return render(request, 'interview-dashboard.html', context)

def live_class_view(request, live_class_id):
    live_class = LiveClass.objects.get(id=live_class_id)

    # Extract the questions and their locked status from the lesson_data field
    questions = []
    for scenario in live_class.lesson_data.values():
        for question in scenario:
            for key, value in question.items():
                questions.append({
                    'text': key,
                    'locked': value == 'locked',
                })
    
    context = {
        'live_class_info': live_class,
        'questions': questions,
    }

    return render(request, 'live-class.html', context)









def select_question_view(request, live_class_id):
    live_class = LiveClass.objects.get(id=live_class_id)

    # Extract the questions and their locked status from the lesson_data field
    questions = []
    for scenario in live_class.lesson_data.values():
        for question in scenario:
            for key, value in question.items():
                questions.append({
                    'text': key,
                    'locked': value == 'locked',
                })

    # Pair each question with its index
    questions = list(enumerate(questions))

    context = {
        'redirect_template': str(request.GET['type']),
        'live_class_info': live_class,
        'questions': questions,
    }
    return render(request, 'select_question.html', context)

def view_question_view(request, live_class_id, question_id):
    live_class = LiveClass.objects.get(id=live_class_id)
    # Fetch the students of the class
    students = InterviewStudent.objects.filter(interview_class=live_class.interview_class)

    # Fetch the question using the question_id
    question_text = ''
    question_locked = False
    question_id = int(question_id)
    for index, scenario in enumerate(live_class.lesson_data.values()):
        if index == question_id:
            for question in scenario:
                for key, value in question.items():
                    question_text = key
                    question_locked = value == 'locked'
                    break

    # Fetch all feedbacks related to the question
    feedbacks = Feedback.objects.filter(Question=Question.objects.all()[0])
    
    # Prepare students_feedbacks dict
    students_feedbacks = {student.user.username: [] for student in students}
    for feedback in feedbacks:
        students_feedbacks[feedback.receiver.username].append(feedback.text)

    context = {
        'redirect_template': str(request.GET.get('type', 'default_value')),
        'live_class_info': live_class,
        'students': students,
        'question': {
            'id': question_id,
            'text': question_text,
            'locked': question_locked,
        },
        'feedbacks': feedbacks,
        'receiver_username': live_class.currently_presenting,
        'question_text': question_text
    }

    return render(request, 'view_question.html', context)



def create_zoom_meeting(request):
    channel_layer = get_channel_layer()


    # Start the live class
    LiveClass(initiator = request.user)


    

    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    # if not hasattr(user, 'tutor'):
    #     return JsonResponse({'error': 'User is not a tutor'}, status=400)

    tutor = Tutor.objects.get(user = request.user)
    client = ZoomClient(tutor.zoom_access_token, tutor.zoom_refresh_token)
    meeting = client.meetings.create_meeting('Auto created 1', start_time=dt.now().isoformat(), duration_min=60, password='not-secure')
    
    # Convert the meeting to a dictionary
    zoom_url = f"https://zoom.us/j/{meeting.id}/"

    async_to_sync(channel_layer.group_send)(
        "live_class_1", 
        {
            "type": "signal", 
            "message": "LCST",
            "meeting_join_url": zoom_url
        }
    )

    return HttpResponseRedirect(zoom_url)
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
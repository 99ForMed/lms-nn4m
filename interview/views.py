import pytz
from datetime import datetime
from datetime import datetime as dt
from django.shortcuts import render, redirect, get_object_or_404
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
import json
from django.conf import settings



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
        'class': {},
        'REDIS_URL': os.getenv('REDIS_URL')
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
    context['link_zoom_uri'] = "https://zoom.us/oauth/authorize?response_type=code&client_id="+os.getenv('ZOOM_CLIENT_ID')+"Q&redirect_uri="+os.getenv("ZOOM_INITIAL_REDIRECT_SECURE")+"%3A%2F%2F"+os.getenv("host")+"%2Fzoom-start%2F"

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

def interview_class_view(request, class_id):

    interview_class = get_object_or_404(InterviewClass, id=class_id)
    students = InterviewStudent.objects.filter(interview_class=interview_class)
    lesson_plans = LessonPlan.objects.filter(tutors=Tutor.objects.get(user = request.user))

    new_task = request.GET.get('new_task')
    task_student_id = request.GET.get('task_student')

    if new_task and task_student_id:
        student = InterviewStudent.objects.get(id=task_student_id)
        current_tasks = student.tasks
        current_tasks.append(new_task)
        student.tasks = current_tasks
        student.save()

    context = {
        'class': interview_class,
        'students': students,
        'lesson_plans': lesson_plans
    }

    return render(request, 'interview-class.html', context)









def select_question_view(request, live_class_id):

    live_class = LiveClass.objects.get(id=live_class_id)

    # Flatten scenario and non-scenario questions
    questions = []
    question_number = 1
    for group_index, (scenario, scenario_questions) in enumerate(live_class.lesson_data.items()):
        for question_index, question in enumerate(scenario_questions):
            question_info = {
                'group_index': group_index,
                'question_index': question_index,
                'text': 'Question {}'.format(question_number),
                'locked': list(question.values())[0] == 'locked'
            }
            questions.append(question_info)
            question_number += 1

    context = {
        'live_class_info': live_class,
        'questions': questions
    }
    
    return render(request, 'select_question.html', context)



def view_question_view(request, live_class_id, group_index, question_index):

    live_class = get_object_or_404(LiveClass, id=live_class_id)
    grouped_questions = live_class.get_grouped_questions()

    # Fetch the question using the group_index and question_index.
    try:
        group = grouped_questions[int(group_index)]
        question = group['questions'][int(question_index)]
    except (ValueError, IndexError):
        raise Http404('Question not found')
    
    # Fetch the students of the class
    students = InterviewStudent.objects.filter(interview_class=live_class.interview_class)

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
            'id': f"{group_index}-{question_index}",
            'text': question['text'],
            'locked': question['locked'],
        },
        'feedbacks': feedbacks,
        'receiver_username': live_class.currently_presenting,
        'question_text': question['text'],
        'scenario': group['scenario'],
        'currently_presenting': live_class.currently_presenting 
    }

    return render(request, 'view_question.html', context)


def active_live_class_view(request):
    # Retrieve the single active LiveClass object. If no such object exists or there's more than one,
    # a Http404 exception will be raised.
    active_class = get_object_or_404(LiveClass, is_active=True)
    
    # Redirect to the URL for this active class.
    return redirect('live_class', live_class_id=active_class.id)

def create_zoom_meeting(request):
    channel_layer = get_channel_layer()

    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        # if not hasattr(user, 'tutor'):
        #     return JsonResponse({'error': 'User is not a tutor'}, status=400)

        tutor = Tutor.objects.get(user = request.user)
        client = ZoomClient(tutor.zoom_access_token, tutor.zoom_refresh_token)
        try:
            meeting = client.meetings.create_meeting('Auto created 1', start_time=dt.now().isoformat(), duration_min=60, password='not-secure')
        except Exception as e:
            # If the error message is a JSON string containing a 'code' field
            redirect_url = f"https://zoom.us/oauth/authorize?response_type=code&client_id={os.getenv('ZOOM_CLIENT_ID')}&redirect_uri={os.getenv('ZOOM_INITIAL_REDIRECT_SECURE')}%3A%2F%2F{os.getenv('host')}%2Fzoom-start%2F"
            return HttpResponseRedirect(redirect_url)
              
        # Convert the meeting to a dictionary
        zoom_url = f"https://zoom.us/j/{meeting.id}/"

        async_to_sync(channel_layer.group_send)(
            "live_class_1", 
            {
                "type": "signal", 
                "message": "LCST",
                "meeting_join_url": zoom_url,
                 
            }
        )

        return HttpResponseRedirect(zoom_url)
    except ValueError as e:
        # Check if the error code indicates an expired token
        if e.args[0]['code'] == 124:
            return HttpResponseRedirect(get_zoom_auth_url())
        else:
            raise e
    channel_layer = get_channel_layer()


    

    
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
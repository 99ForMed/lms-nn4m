import datetime
from django.shortcuts import render, redirect
from .models import *
from datetime import date, timedelta
# Create your views here.

def home_view(request):

    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return redirect('/authentication/login/')

def dashboard_view(request):
    if Tutor.objects.filter(user = request.user).exists():
        return redirect('/tutors/dashboard/')
    return dashboard_view_student(request)

def dashboard_view_student(request):
    return None

def dashboard_view_student(request):
    current_section = None
    user_sections = UcatSectionInstance.objects.filter(student = UcatStudent.objects.get(user = request.user))
    start_dates_ordered = []
    for section in user_sections:
        start_dates_ordered.append(section.start_date)
        if section.current:
            current_section = section
    context = {
        'current_section': current_section,
        'start_dates_ordered':start_dates_ordered,
        'tasks': UcatStudent.objects.get(user = request.user).tasks,
        'date1': (UcatStudent.objects.get(user=request.user).enrolment_date).date(),
        'date2': (UcatStudent.objects.get(user=request.user).enrolment_date+ timedelta(days=30)).date(),
        'date3': (UcatStudent.objects.get(user=request.user).enrolment_date+ timedelta(days=60)).date(),
        'date4': (UcatStudent.objects.get(user=request.user).enrolment_date+ timedelta(days=90)).date(),
        'date5': (UcatStudent.objects.get(user=request.user).enrolment_date+ timedelta(days=120)).date()
    }

    if not context['current_section'] == None:
        context['skills_mastered'] = context['current_section'].skills_mastered
        deadline = context['current_section'].start_date + timedelta(days=30)
        current_day = datetime.datetime.now().date()
        context['days_to_master'] = (deadline - current_day).days

    return render(request, 'dashboard.html', context)

def course_page_view(request, sectionInstanceId):
    sectionInstance = UcatSectionInstance.objects.get(id = sectionInstanceId)
    section = sectionInstance.section

    context = {
        'section_name': section.name,
        'unlocked_vids': UcatVideo.objects.filter(section = section, unlocked = True),
        'locked_vids': UcatVideo.objects.filter(section = section, unlocked = False)
    }
    return render(request, 'course-page.html', context)

def course_video_view(request, sectionInstanceId, videoId):
    sectionInstance = UcatSectionInstance.objects.get(id = sectionInstanceId)
    section = sectionInstance.section
    video = UcatVideo.objects.get(id=videoId)
    # thumbnails = UcatVideo.objects.filter(section = section).thumbnail
    context = {
        'vid': video,
        'vid_name': video.name,
        'vid_description': video.description,
        'share_code': video.url
    }
    return render(request, 'course-video.html', context)
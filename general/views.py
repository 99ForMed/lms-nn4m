from django.shortcuts import render, redirect
from .models import *
# Create your views here.

def home_view(request):

    if request.user.is_authenticated:
        return redirect('/dashboard')
    

    context = {

    }
    return render(request, 'home.html', context)

def dashboard_view(request):
    current_section = None
    user_sections = UcatSectionInstance.objects.filter(student = UcatStudent.objects.get(user = request.user))
    start_dates_ordered = []
    for section in user_sections:
        start_dates_ordered.append(section.start_date)
        if section.current:
            current_section = section
    context = {
        'current_section': current_section,
        'start_dates_ordered':start_dates_ordered
    }

    if not context['current_section'] == None:
        context['skills_mastered'] = context['current_section'].skills_mastered

    return render(request, 'dashboard.html', context)

def course_page_view(request, sectionInstanceId):
    context = {
        
    }
    return render(request, 'course-page.html', context)

def course_video_view(request, sectionInstanceId, videoId):
    section = UcatSection.objects.get(id = sectionInstanceId)
    # thumbnails = UcatVideo.objects.filter(section = section).thumbnail
    context = {
        'section-title': section.name,
        'unlocked-vids': None
    }
    return render(request, 'course-video.html', context)
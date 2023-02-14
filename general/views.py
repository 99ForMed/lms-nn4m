from django.shortcuts import render, redirect

# Create your views here.

def home_view(request):

    if request.user.is_authenticated:
        return redirect('/dashboard')
    

    context = {

    }
    return render(request, 'home.html', context)

def dashboard_view(request):
    context = {
        
    }
    return render(request, 'dashboard.html', context)

def course_page_view(request):
    context = {

    }
    return render(request, 'course-page.html', context)

def course_video_view(request):
    context = {

    }
    return render(request, 'course-video.html', context)
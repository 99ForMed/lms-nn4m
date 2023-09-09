import datetime
from django.shortcuts import render, redirect

from Forum.models import Comment, Reply
from .models import *
from datetime import date, timedelta

from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.decorators.http import require_POST

from .forms import UploadFileForm

from custom_storages import CustomS3Storage
from django.core.files.storage import default_storage

from django.shortcuts import get_object_or_404
from interview.models import InterviewStudent
from pyzoom import request_tokens
import os

from django.http import HttpResponse
from Tutors.models import Tutor

import json


# Create your views here.

def home_view(request):

    if request.user.is_authenticated:
        return redirect('/dashboard/')
    else:
        return redirect('/authentication/login/')

def dashboard_view(request):
    if request.user.is_authenticated:
        if Tutor.objects.filter(user=request.user).exists():
            return redirect('/tutors/dashboard/')
        
        if InterviewStudent.objects.filter(user=request.user).exists():
            return redirect('/interview/')
        
        return dashboard_view_student(request)
    else:
        # Redirect to login page or handle anonymous user here
        return redirect('/authentication/login/')

def dashboard_view_student(request):
    current_section = None
    try:
        student = UcatStudent.objects.get(user=request.user)
        user_sections = UcatSectionInstance.objects.filter(student=student)
    except UcatStudent.DoesNotExist:
        user_sections = UcatSectionInstance.objects.none()  # or set to some default value
    start_dates_ordered = []
    for section in user_sections:
        start_dates_ordered.append(section.start_date)
        if section.current:
            current_section = section
    for section in UcatSection.objects.all():
        if len(UcatSectionInstance.objects.filter(section = section, student=UcatStudent.objects.get(user=request.user))) == 0:
            student_instance = UcatStudent.objects.get(user=request.user)
            section_instance = section

            # Create a UcatSectionInstance object with the desired attributes
            ucat_section_instance = UcatSectionInstance(
                student=student_instance,
                section=section_instance,
                start_date = datetime.datetime.now().date(),
                current=False,  # or False, depending on the desired value
                skills_mastered=0  # or any other valid integer value
            )

            # Save the UcatSectionInstance object to the database
            ucat_section_instance.save()

    context = {
        'current_section': current_section,
        'ucat_student': UcatStudent.objects.get(user = request.user),
        'start_dates_ordered':start_dates_ordered,
        'tasks': UcatStudent.objects.get(user = request.user).tasks_json,
        'date1': (UcatStudent.objects.get(user=request.user).enrolment_date).date(),
        'date2': (UcatStudent.objects.get(user=request.user).enrolment_date+ timedelta(days=30)).date(),
        'date3': (UcatStudent.objects.get(user=request.user).enrolment_date+ timedelta(days=60)).date(),
        'date4': (UcatStudent.objects.get(user=request.user).enrolment_date+ timedelta(days=90)).date(),
        'date5': (UcatStudent.objects.get(user=request.user).enrolment_date+ timedelta(days=120)).date(),
        'sectionId1': UcatSectionInstance.objects.get(student = UcatStudent.objects.get(user = request.user), section = UcatSection.objects.get(id=1)).id,
        'sectionId2': UcatSectionInstance.objects.get(student = UcatStudent.objects.get(user = request.user), section = UcatSection.objects.get(id=2)).id,
        'sectionId3': UcatSectionInstance.objects.get(student = UcatStudent.objects.get(user = request.user), section = UcatSection.objects.get(id=3)).id,
        'sectionId4': UcatSectionInstance.objects.get(student = UcatStudent.objects.get(user = request.user), section = UcatSection.objects.get(id=4)).id,
        'sectionId5': UcatSectionInstance.objects.get(student = UcatStudent.objects.get(user = request.user), section = UcatSection.objects.get(id=5)).id
    }

    if not context['current_section'] == None:
        context['skills_mastered'] = context['current_section'].skills_mastered
        deadline = context['current_section'].start_date + timedelta(days=30)
        current_day = datetime.datetime.now().date()
        context['days_to_master'] = (deadline - current_day).days

    if len(context['tasks']) == 0:
        context['no_tasks'] = True 
    
    return render(request, 'dashboard.html', context)

def course_page_view(request, sectionInstanceId):
    sectionInstance = UcatSectionInstance.objects.get(id=sectionInstanceId)
    section = sectionInstance.section
    videos_dict = {}
    videos = UcatVideo.objects.filter(section=section, unlocked=True)

    for video in videos:
        videos_dict[str(video.syllabus_point)] = []

    for video in videos:
        videos_dict[str(video.syllabus_point)].append(video)

    # Sort videos by index for each syllabus_point
    for syllabus_point, videos in videos_dict.items():
        videos.sort(key=lambda x: x.index)
        videos_dict[syllabus_point] = {
            'videos': videos,
            'remaining_placeholders': 6 - len(videos)
        }

    # Only reorder if the section is "Decision Making"
    if section.name == "Decision Making":
        syllabus_order = [
            "Pre-tutorial content", "Drawing Conclusions", "Strongest Argument",
            "Order/ Logical Puzzles", "Venn Diagrams", "Probability",
            "Course Completion Videos"
        ]

        # Create a new dictionary based on the predefined order
        ordered_videos_dict = {}
        for point in syllabus_order:
            if point in videos_dict:
                ordered_videos_dict[point] = videos_dict[point]

        # Add any additional syllabus points not in the predefined order
        for point in videos_dict.keys():
            if point not in syllabus_order:
                print(point)
                ordered_videos_dict[point] = videos_dict[point]

        videos_dict = ordered_videos_dict

    context = {
        'videos_dict': videos_dict,
        'section_name': section.name,
        'locked_vids': UcatVideo.objects.filter(section=section, unlocked=False)
    }

    return render(request, 'course-page-updated.html', context)



def course_video_view(request, sectionInstanceId, videoId):
    
    
    sectionInstance = UcatSectionInstance.objects.get(id = sectionInstanceId)
    section = sectionInstance.section
    video = UcatVideo.objects.get(id=videoId)
    # thumbnails = UcatVideo.objects.filter(section = section).thumbnail
    
    student = UcatStudent.objects.get(user = request.user) # Assuming the user is logged in
    context = {
        'vid': video,
        'vid_name': video.name,
        'vid_description': video.description,
        'share_code': video.url,
        'comments': Comment.objects.filter(forum = video),
        'section': section,
        'raised': False


    }
    if request.method == 'POST':
        problem_text = request.POST['issue_details']
        if problem_text:
            problem = UcatProblem(student=student, video=video, problem=problem_text)
            problem.save()
            context['raised'] = True
            return redirect(request.path)  # Redirect to the same page to avoid resubmission on refresh


    return render(request, 'course-video.html', context)

@require_POST
def add_comment(request):
    video_id = request.POST.get('video_id')
    user = request.user
    content = request.POST.get('content')

    if not user.is_authenticated:
        return JsonResponse({'error': 'Authentication required.'})

    try:
        video = UcatVideo.objects.get(id=video_id)
    except UcatVideo.DoesNotExist:
        return JsonResponse({'error': 'Video not found.'})

    comment = Comment(forum=video, user=user, content=content, upvotes=0)
    comment.save()

    # Return the new comment as a JSON response
    return JsonResponse({
        'id': comment.id,
        'username': comment.user.username,
        'datetime': comment.datetime.strftime('%Y-%m-%d %H:%M:%S'),
        'content': comment.content,
        'upvotes': comment.upvotes,
    })

def add_reply(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        user = request.user
        content = request.POST.get('reply_content')

        comment = Comment.objects.get(id=comment_id)

        reply = Reply(comment=comment, user=user, content=content, upvotes=0)
        reply.save()

        data = {
            'username': user.username,
            'datetime': reply.datetime.strftime('%Y-%m-%d %H:%M'),
            'content': reply.content,
            'upvotes': reply.upvotes
        }
        return JsonResponse(data)
    else:
        return HttpResponseNotAllowed(['POST'])
    

def upvote_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        comment.upvotes += 1
        comment.save()

        return JsonResponse({'upvotes': comment.upvotes})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def submit_progress_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # s3_storage = CustomS3Storage()
            user_fullname_dir = request.user.username.upper().replace(" ", "_")
            # upload_directory = 'static/uploads/'+user_fullname_dir+"/"

            # # You can change 'uploads/' to any other directory name you want to save the files in.
            # filename = s3_storage.save(upload_directory + file.name, file)
            file_name = default_storage.save('uploads/'+user_fullname_dir+"/"+file.name, file)
            return redirect('/dashboard/submit-progress/?submitted')
    else:
        form = UploadFileForm()
    context = {
        'form': form,
        'tasks': UcatStudent.objects.get(user = request.user).tasks
    }

    if 'submitted' in request.GET.keys():
        context['submitted'] = True
    return render(request, 'submit-progress.html', context)
    # return redirect("../../under-maintenance/")


def maintenance_view(request):
    return render(request, 'maintenance.html', {})

def sitemap_view(request):
    return render(request, 'sitemap.xml', {})


def csrf_failure(request, reason=""):
    # You can use HttpResponse to return a custom message or 
    # use HttpResponseRedirect to redirect to a different page
    print('csrf_faile')
    return HttpResponseRedirect(request.META.HTTP_REFERER)

def handler404(request, *args, **argv):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler403(request, exception=None):
    return redirect(request.path)


def handler500(request, *args, **argv):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

def zoom_authenticated_view(request):
    return HttpResponse("Success")

from Tutors.models import Tutor  # Import the Tutor model

def zoom_start_view(request):
    code = request.GET['code']
    user = request.user  # Assuming you have user authentication in place

    # Exchange the code for a token
    print(os.getenv("ZOOM_CLIENT_ID"))
    print(os.getenv("ZOOM_CLIENT_SECRET"))
    print(os.getenv('ZOOM_INITIAL_REDIRECT_SECURE')+"://"+os.getenv('host')+"/zoom-start/")
    tokens = request_tokens(os.getenv("ZOOM_CLIENT_ID"), os.getenv("ZOOM_CLIENT_SECRET"), os.getenv('ZOOM_INITIAL_REDIRECT_SECURE')+"://"+os.getenv('host')+"/zoom-start/", code)

    # Get the user's InterviewStudent record
    interview_student = get_object_or_404(InterviewStudent, user=user)

    # Save the tokens to the user's InterviewStudent record
    interview_student.zoom_access_token = tokens['access_token']
    interview_student.zoom_refresh_token = tokens['refresh_token']
    interview_student.save()

    # Check if the user is also a tutor
    try:
        tutor = Tutor.objects.get(user=user)
        # Save the tokens to the Tutor record
        tutor.zoom_access_token = tokens['access_token']
        tutor.zoom_refresh_token = tokens['refresh_token']
        tutor.save()
    except Tutor.DoesNotExist:
        # If the user is not a tutor, do nothing
        pass

    # Redirect the user back to the dashboard or another page
    return redirect('/')

def coming_soon_view(request):
    context = {

    }
    return render(request, 'coming_soon.html', context)

def alter_ucat_task_view(request, done, ucat_task_content_exact, ucat_student_id):
    if done.upper() == "FALSE":

        bufferObj = UcatStudent.objects.get(id = ucat_student_id)
        bufferObj.tasks_json[ucat_task_content_exact] = False
        bufferObj.save()
    elif done.upper() == "TRUE":
        bufferObj = UcatStudent.objects.get(id = ucat_student_id)
        bufferObj.tasks_json[ucat_task_content_exact] = True
        bufferObj.save()

    else:
        raise "done is not in the correct format"

    return redirect(request.META.get('HTTP_REFERER', '/'))

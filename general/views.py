import datetime
from django.shortcuts import render, redirect

from Forum.models import Comment, Reply
from .models import *
from datetime import date, timedelta

from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.decorators.http import require_POST

from .forms import UploadFileForm

from custom_storages import CustomS3Storage

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

    if len(context['tasks']) == 0:
        context['no_tasks'] = True 

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
        problem_text = request.POST.get('issue_details')
        if problem_text:
            problem = UcatProblem(student=student, video=video, problem=problem_text)
            problem.save()
            context['raised'] = True
            return redirect(request.path)  # Redirect to the same page to avoid resubmission on refresh

    if len(UcatProblem.objects.filter(video = UcatVideo.objects.get(id=videoId))) > 0:
        context['raised'] = True

    

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
            s3_storage = CustomS3Storage()
            user_fullname_dir = request.user.username.upper().replace(" ", "_")
            upload_directory = 'static/uploads/'+user_fullname_dir+"/"

            # You can change 'uploads/' to any other directory name you want to save the files in.
            filename = s3_storage.save(upload_directory + file.name, file)
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
    
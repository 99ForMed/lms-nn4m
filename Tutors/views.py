from django.shortcuts import render, redirect
import datetime

from .models import *
from general.models import *

from django.conf import settings
import boto3
from botocore.exceptions import ClientError
from django.core.files.storage import default_storage
# from azure.storage.blob import generate_blob_sas, BlobClient, BlobServiceClient, BlobSasPermissions
from urllib.parse import quote

import os

from django.views import View
from django.http import JsonResponse
from live_class.models import LiveClass

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from live_class.models import Question

from django.urls import reverse
from interview.models import InterviewClass


class UpdatePresenterView(View):
    def post(self, request, *args, **kwargs):
        live_class_id = request.POST.get('live_class_id')
        presenter_username = request.POST.get('presenter_username')

        live_class = LiveClass.objects.get(id=live_class_id)
        live_class.currently_presenting = User.objects.get(username=presenter_username)
        live_class.save()

        return JsonResponse({"status": "success"})


# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#     region_name=settings.AWS_S3_REGION_NAME
# )

# def generate_presigned_url(bucket_name, file_path, expiration=3600):
#     try:
#         response = s3_client.generate_presigned_url('get_object',
#                                                     Params={'Bucket': bucket_name,
#                                                             'Key': file_path},
#                                                     ExpiresIn=expiration)
#     except ClientError as e:
#         print(e)
#         return None

#     return response

# Create your views here.

def dashboard_tutor_view(request):
    
    now = datetime.datetime.now()
    current_time = now.time()

    if current_time < datetime.time(12, 0, 0):
        time_greeting = 'Good morning'
    elif current_time < datetime.time(17, 0, 0):
        time_greeting = 'Good afternoon'
    else:
        time_greeting = 'Good evening'

    # Get all questions and organize them in a dict by scenario
    questions_queryset = Question.objects.all()
    interview_questions = {}

    for question in questions_queryset:
        scenario_description = question.scenario.description if question.scenario else None
        if scenario_description not in interview_questions:
            interview_questions[scenario_description] = []
        interview_questions[scenario_description].append(question.question_text)
    
    context = {
        'time_greeting': time_greeting,
        'tutor': Tutor.objects.get(user=request.user),
        'classes': Tutor.objects.get(user=request.user).classes.all(),
        'interview_questions': interview_questions,
        'interview_classes': InterviewClass.objects.filter(tutor = Tutor.objects.get(user=request.user)),
        'ws_host': os.getenv('WS_HOST', ''),
        'route': 'interview/dashboard/'
    }

    # Rest of your view...


    # Assuming there are only going to be 3 classes max
    context['amount_of_classes'] = len(Tutor.objects.get(user = request.user).classes.all())
    context['amount_of_empty_classes'] = 3 - context['amount_of_classes']
    context['amount_of_empty_interview_classes'] = 3 - len(context['interview_classes'])

    # if empty_classes >= 0:
    #     for(i in range(0, len(Tutor.objects.get(user = request.user).classes.all()))):
    #         context['classes'][i] = Tutor.objects.Tutor.objects.get(user = request.user).classes.all()[i]


    # context['link_zoom_uri'] = "https://zoom.us/oauth/authorize?response_type=code&client_id=wpT5jz7rQ8W_SNbSp_13Q&redirect_uri="+os.getenv("ZOOM_INITIAL_REDIRECT_SECURE")+"%3A%2F%2F"+os.getenv("host")+"%2Fzoom-start%2F"


    return render(request, 'tutor-dashboard.html', context)


def raise_issue_view(request):
    context = {

    }
    return render(request, "raise_issue.html", context)

def tutor_strategies_document(request):

    # result = s3_client.list_objects(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix="tutor-strategies/", Delimiter='/')

    # # # Extract the folders
    # # folders = result.get('CommonPrefixes')

    # # # Create a dictionary to store folder-wise files
    # # folder_files = {}

    # # for folder in folders:
    # #     folder_name = folder['Prefix'].strip('/').split('/')[-1]
        
    # #     # Make an API call to get the files within the folder
    # #     folder_result = s3_client.list_objects(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix=folder['Prefix'])
    # #     files_in_folder = folder_result.get('Contents')

    # #     # Filter out the folder itself, extract the file names and generate pre-signed URLs
    # #     file_links = [{'name': file['Key'].split('/')[-1], 'url': generate_presigned_url(settings.AWS_STORAGE_BUCKET_NAME, file['Key'])} for file in files_in_folder if file['Key'] != folder['Prefix']]
        
    # #     folder_files[folder_name] = file_links

    # # context = {
    # #     'folder_files': folder_files,
    # # }
    # # return render(request, "tutor-strategies.html", context)
    # service = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
    # container = service.get_container_client(settings.AZURE_CONTAINER)

    # prefix = "uploads/tutor-strategies/"
    # blob_list = container.list_blobs(name_starts_with=prefix)
    # print(blob_list)

    # folder_files = {}

    # for blob in blob_list:
    #     # split the blob.name based on '/' to simulate folders
    #     parts = blob.name.split('/')
        
    #     # the second last part is the folder name
    #     folder_name = parts[-2] if len(parts) > 1 else ''
        
    #     # the last part is the file name
    #     file_name = parts[-1]
        
    #     # generate download url
    #     blob_client = container.get_blob_client(blob)
    #     sas_token = generate_blob_sas(
    #         account_name=settings.AZURE_ACCOUNT_NAME,
    #         account_key=settings.AZURE_ACCOUNT_KEY,
    #         container_name=settings.AZURE_CONTAINER,
    #         blob_name=blob.name,
    #         permission=BlobSasPermissions(read=True),
    #         expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    #     )
    #     file_url = f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net/{settings.AZURE_CONTAINER}/{quote(blob.name)}?{sas_token}"
        
    #     # append to the dictionary
    #     if folder_name not in folder_files:
    #         folder_files[folder_name] = []
    #     folder_files[folder_name].append({'name': file_name, 'url': file_url})

    # return render(request, 'tutor-strategies.html', {'folder_files': folder_files})
    return redirect('../../../under-maintenance/')

    

def tutor_resources_view(request):

    # service = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
    # container = service.get_container_client(settings.AZURE_CONTAINER)

    # prefix = "uploads/tutor-resources/"
    # blob_list = container.list_blobs(name_starts_with=prefix)
    # print(blob_list)

    # folder_files = {}

    # for blob in blob_list:
    #     # split the blob.name based on '/' to simulate folders
    #     parts = blob.name.split('/')
        
    #     # the second last part is the folder name
    #     folder_name = parts[-2] if len(parts) > 1 else ''
        
    #     # the last part is the file name
    #     file_name = parts[-1]
        
    #     # generate download url
    #     blob_client = container.get_blob_client(blob)
    #     sas_token = generate_blob_sas(
    #         account_name=settings.AZURE_ACCOUNT_NAME,
    #         account_key=settings.AZURE_ACCOUNT_KEY,
    #         container_name=settings.AZURE_CONTAINER,
    #         blob_name=blob.name,
    #         permission=BlobSasPermissions(read=True),
    #         expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    #     )
    #     file_url = f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net/{settings.AZURE_CONTAINER}/{quote(blob.name)}?{sas_token}"
        
    #     # append to the dictionary
    #     if folder_name not in folder_files:
    #         folder_files[folder_name] = []
    #     folder_files[folder_name].append({'name': file_name, 'url': file_url})

    # return render(request, 'tutor-resources.html', {'folder_files': folder_files})
    return redirect('../../../under-maintenance/')

def tutors_class_view(request, classId):

    if 'solved' in request.GET.keys():
        new_obj = UcatProblem.objects.get(id= int(request.GET['solved']))
        new_obj.solved = True
        new_obj.save()
    
    if 'new_task' in request.GET.keys():
        if not request.GET['new_task'] == "null":
            new_obj = UcatStudent.objects.get(id = int(request.GET['task_student']))
            updated_task_dict = new_obj.tasks_json
            updated_task_dict[request.GET['new_task']] = False
            new_obj.tasks_json = updated_task_dict
            new_obj.save()

    student = UcatStudent.objects.get(user = User.objects.get(username = "rafiStudent"))
    problems = student.UcatProblems
    unsolved_problems = []
    for problem in problems.all():
        if not problem.solved:
            unsolved_problems.append(problem)

    context = {
        'class': UcatClass.objects.get(id = classId),
        'unsolved_problems': unsolved_problems
    }
    return render(request, 'ucat_class.html', context)

def evidence_of_work_view(request, classId, studentId):
    # bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    # directory_path = 'static/uploads/'+ str(UcatStudent.objects.get(pk=studentId).user).upper().replace(" ", "_")+'/'
    # response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=directory_path)

    files = []
    # if 'Contents' in response:
    #     for obj in response['Contents']:
    #         file_path = obj['Key']
    #         file_name = file_path.split('/')[-1]
    #         upload_time = obj['LastModified']
    #         file_url = generate_presigned_url(bucket_name, file_path)
    #         files.append({'name': file_name, 'path': file_path, 'uploaded_at': upload_time, 'url': file_url})

    
    # context = {

    # }
    # azure_storage = default_storage._wrapped

    # # Define the directory path in Azure Blob Storage
    # directory_path = 'uploads/'+ str(UcatStudent.objects.get(pk=studentId).user).upper().replace(" ", "_")+'/'

    # # List the files in the directory and get a list of file objects
    # files_strs = default_storage.listdir(directory_path)[1]
    # files = []

    # for file in files_strs:
    #     file_path = f"{directory_path}/{file}" if directory_path else file
    #     file_obj = default_storage.open(file_path)
    #     file = {
    #         'name': file,
    #         'uploaded_at': None,
    #         'url': default_storage.url(file_path),
    #     }
    #     files.append(file)
    

    # context = {
    #     'student': UcatStudent.objects.get(pk=studentId),
    #     'files': files
    # }
    # return render(request, 'evidence-of-work.html', context)
    return redirect("../../../under-maintenance/")





@method_decorator(csrf_exempt, name='dispatch')
class UpdateCurrentQuestionView(View):
    def post(self, request, *args, **kwargs):
        live_class_id = request.POST.get('live_class_id')
        question_text = request.POST.get('question_text')
        scenario_desc = request.POST.get('scenario_desc')
        is_current = request.POST.get('is_current') == 'on'

        # Find the LiveClass object
        live_class = LiveClass.objects.get(id=live_class_id)
        lesson_data = live_class.lesson_data

        # Find the scenario
        for scenario, questions in lesson_data.items():
            if scenario == scenario_desc:
                # Find the question
                for question in questions:
                    if question.get(question_text):
                        if is_current:
                            # If the checkbox is checked, set this question as the current question
                            question[question_text] = 'current'
                        else:
                            # If the checkbox is unchecked, set this question as not the current question
                            question[question_text] = 'unlocked'
                        break

        # Save the changes to the lesson data
        live_class.lesson_data = lesson_data
        live_class.save()

        # Redirect to tutors live class view
        return redirect('tutors_live_class_view', live_class.id)
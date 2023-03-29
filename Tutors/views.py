from django.shortcuts import render
import datetime

from .models import *
from general.models import *

from django.conf import settings
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

def generate_presigned_url(bucket_name, file_path, expiration=3600):
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': file_path},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print(e)
        return None

    return response

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
    context = {
        'time_greeting': time_greeting,
        'tutor': Tutor.objects.get(user = request.user)
    }
    return render(request, 'tutor-dashboard.html', context)


def raise_issue_view(request):
    context = {

    }
    return render(request, "raise_issue.html", context)

def tutor_strategies_document(request):
    result = s3_client.list_objects(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix="tutor-strategies/", Delimiter='/')

    # Extract the folders
    folders = result.get('CommonPrefixes')

    # Create a dictionary to store folder-wise files
    folder_files = {}

    for folder in folders:
        folder_name = folder['Prefix'].strip('/').split('/')[-1]
        
        # Make an API call to get the files within the folder
        folder_result = s3_client.list_objects(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix=folder['Prefix'])
        files_in_folder = folder_result.get('Contents')

        # Filter out the folder itself, extract the file names and generate pre-signed URLs
        file_links = [{'name': file['Key'].split('/')[-1], 'url': generate_presigned_url(settings.AWS_STORAGE_BUCKET_NAME, file['Key'])} for file in files_in_folder if file['Key'] != folder['Prefix']]
        
        folder_files[folder_name] = file_links

    context = {
        'folder_files': folder_files,
    }
    return render(request, "tutor-strategies.html", context)

def tutor_resources_view(request):
    result = s3_client.list_objects(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix="tutor-resources/", Delimiter='/')

    # Extract the folders
    folders = result.get('CommonPrefixes')

    # Create a dictionary to store folder-wise files
    folder_files = {}

    for folder in folders:
        folder_name = folder['Prefix'].strip('/').split('/')[-1]
        
        # Make an API call to get the files within the folder
        folder_result = s3_client.list_objects(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix=folder['Prefix'])
        files_in_folder = folder_result.get('Contents')

        # Filter out the folder itself, extract the file names and generate pre-signed URLs
        file_links = [{'name': file['Key'].split('/')[-1], 'url': generate_presigned_url(settings.AWS_STORAGE_BUCKET_NAME, file['Key'])} for file in files_in_folder if file['Key'] != folder['Prefix']]
        
        folder_files[folder_name] = file_links

    context = {
        'folder_files': folder_files,
    }
    return render(request, "tutor-resources.html", context)

def tutors_class_view(request, classId):

    if 'solved' in request.GET.keys():
        new_obj = UcatProblem.objects.get(id= int(request.GET['solved']))
        new_obj.solved = True
        new_obj.save()
    
    student = UcatStudent.objects.get(user = request.user)
    unsolved_problems = student.UcatProblems.filter(solved=False)  

    context = {
        'class': UcatClass.objects.get(id = classId),
        'unsolved_problems': unsolved_problems
    }
    return render(request, 'ucat_class.html', context)

def evidence_of_work_view(request, classId, studentId):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    directory_path = 'static/uploads/'+ str(UcatStudent.objects.get(pk=studentId).user).upper().replace(" ", "_")+'/'
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=directory_path)

    files = []
    if 'Contents' in response:
        for obj in response['Contents']:
            file_path = obj['Key']
            file_name = file_path.split('/')[-1]
            upload_time = obj['LastModified']
            file_url = generate_presigned_url(bucket_name, file_path)
            files.append({'name': file_name, 'path': file_path, 'uploaded_at': upload_time, 'url': file_url})

    context = {
        'student': UcatStudent.objects.get(pk=studentId),
        'files': files
    }
    return render(request, 'evidence-of-work.html', context)
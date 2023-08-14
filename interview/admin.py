from django.contrib import admin
from .models import InterviewClass, InterviewStudent

# Register your models here.
admin.site.register(InterviewStudent)
admin.site.register(InterviewClass)

from django.contrib import admin
from .models import InterviewStudent, InterviewClass

# Register your models here.
admin.site.register(InterviewStudent)
admin.site.register(InterviewClass)
# admin.site.register(LiveClass)

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(LiveClass)
admin.site.register(LessonPlan)
admin.site.register(Question)
admin.site.register(Scenario)
admin.site.register(Task)
admin.site.register(Feedback)
admin.site.register(InterviewVideo)
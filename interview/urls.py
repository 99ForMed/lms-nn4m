from django.contrib import admin
from django.urls import path, include

from .views import interview_dashboard_view, live_class_view
from .views import select_question_view, view_question_view

urlpatterns = [
    path('', interview_dashboard_view),
    path('live-class/', live_class_view),
    path('live-class/select-question/', select_question_view),
    path('live-class/question/', view_question_view),
    path('live-class/feedback/', view_question_view)
]

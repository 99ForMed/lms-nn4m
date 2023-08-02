from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import dashboard_tutor_view, raise_issue_view, tutor_strategies_document
from .views import tutors_class_view, evidence_of_work_view, tutor_resources_view

from live_class.views import tutors_live_class_view

urlpatterns = [
    path('dashboard/', dashboard_tutor_view),
    path('dashboard/raise-issue/', raise_issue_view),
    path('dashboard/tutor-strategies/', tutor_strategies_document),
    path('dashboard/tutor-resources/', tutor_resources_view),
    path('dashboard/class/<int:classId>/', tutors_class_view),
    path('dashboard/class/<int:classId>/evidence-of-work/<int:studentId>', evidence_of_work_view),
    path('live-class/<str:class_id>/', tutors_live_class_view),
    

]
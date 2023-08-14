from django.contrib import admin
from django.urls import path, include

from interview import views
from .views import interview_dashboard_view, live_class_view
from .views import select_question_view, view_question_view
from .views import add_feedback_view
from .views import interview_class_view, active_live_class_view
from .views import view_feedback_view
from .views import start_group_session_view
from .views import lesson_plan_view
from .views import module_plan_view

urlpatterns = [
    path('', interview_dashboard_view, name = 'interview_dashboard'),
    path('live-class/create-meeting/', views.create_zoom_meeting, name='create-zoom-meeting'),
    path('live-class/', active_live_class_view),
    path('live-class/<str:live_class_id>/', live_class_view, name='live_class'),
    path('live-class/<str:live_class_id>/select-question/', select_question_view),
    path('live-class/<str:live_class_id>/lessson-plan/', lesson_plan_view, name='lesson-plan-info'),
    path('live-class/<str:live_class_id>/feedback/', view_question_view),
    path('live-class/<str:live_class_id>/question/<int:group_index>/<int:question_index>/', view_question_view, name='view_question'),
    path('add_feedback/<int:live_class_id>/<int:question_id>/<int:receiver_id>/', add_feedback_view, name='add_feedback'),
    path('class/<str:class_id>/', interview_class_view),
    path('live-class/<str:live_class_id>/my_feedback/', view_feedback_view, name='view_feedback'),
    path('live-class/group_session/' , start_group_session_view, name='group_session_start'),
    path('module-plan/', module_plan_view, name='module_plan')
]
 
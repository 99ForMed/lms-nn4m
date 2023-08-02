from django.urls import path
from .views import tutors_live_class_view
from .views import end_class_view
from .views import UpdateLockStatusView
from Tutors.views import UpdateCurrentQuestionView, UpdatePresenterView

urlpatterns = [
    path('<str:live_class_id>/end/', end_class_view, name='end_class'),
    path('<str:class_id>/<str:lesson_plan_id>/', tutors_live_class_view, name='live_class'),
    path('update-question-status/', UpdateLockStatusView.as_view(), name='update_question_status'),
    path('update-current-question/', UpdateCurrentQuestionView.as_view()),
    path('update-presenter/', UpdatePresenterView.as_view(), name='update_presenter'),

]
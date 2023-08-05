from django.shortcuts import render, get_object_or_404, redirect
from .models import LiveClass, InterviewClass, LessonPlan
from django.contrib.auth.decorators import login_required
from interview.models import InterviewStudent

from live_class.models import Question

from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from django.http import HttpResponseRedirect

from datetime import datetime, timedelta
from django.utils import timezone

import os

@login_required
def tutors_live_class_view(request, class_id, lesson_plan_id):
    # Try to get all active live classes for the class_id
    active_live_classes = list(LiveClass.objects.filter(interview_class__id=class_id, is_active=True).order_by('start_time'))

    if active_live_classes:
        # If multiple active live classes exist, deactivate all but the most recent one
        if len(active_live_classes) > 1:
            for live_class in active_live_classes[:-1]:
                live_class.is_active = False
                live_class.save()
        
        # Check if the most recent live class is older than 1 hour and 40 minutes
        live_class = active_live_classes[-1]
        if timezone.now() - live_class.start_time > timedelta(minutes=100):
            live_class.is_active = False
            live_class.save()
        else:
            # If the most recent live class is not older than 1 hour and 40 minutes, use it
            context = {
                'live_class': live_class,
                'students': InterviewStudent.objects.filter(interview_class=live_class.interview_class),
                'lesson_data': live_class.lesson_data, 
                'current_question': live_class.current_question,  # current question being answered
                'ws_host': os.getenv('WS_HOST', '')
            }
            return render(request, 'tutors-live-class.html', context)
    
    # If no suitable live class was found, create a new one
    lesson_plan = LessonPlan.objects.get(id=lesson_plan_id)
    live_class = LiveClass.objects.create(
        initiator=request.user, 
        interview_class=InterviewClass.objects.get(id=class_id),
        lesson_plan=lesson_plan,
        is_active=True
    )

    context = {
        'live_class': live_class,
        'students': InterviewStudent.objects.filter(interview_class=live_class.interview_class),
        'lesson_data': live_class.lesson_data, 
        'current_question': live_class.current_question,  # current question being answered
    }

    return render(request, 'tutors-live-class.html', context)



@login_required
def end_class_view(request, live_class_id):
    live_class = get_object_or_404(LiveClass, id=live_class_id, is_active=True)
    live_class.end_class()
    return redirect('/')

class UpdateLockStatusView(View):
    def post(self, request, *args, **kwargs):
        live_class_id = request.POST.get('live_class_id')
        scenario_desc = request.POST.get('scenario_desc')
        question_text = request.POST.get('question_text')
        is_locked = request.POST.get('is_locked') == 'true'
        
        live_class = get_object_or_404(LiveClass, id=live_class_id)
        
        try:
            if scenario_desc not in live_class.lesson_data:
                raise ValidationError('Scenario not found.')
            for question in live_class.lesson_data[scenario_desc]:
                if question_text in question:
                    question[question_text] = 'locked' if is_locked else 'unlocked'
                    live_class.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            raise ValidationError('Question not found.')
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})



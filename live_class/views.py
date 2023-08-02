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


@login_required
def tutors_live_class_view(request, class_id, lesson_plan_id):
    # Fetch the live class information for the current class
    live_class = get_object_or_404(LiveClass, interview_class__id=class_id, is_active=True)

    # Fetch the lesson plan for the tutor
    lesson_plan = LessonPlan.objects.get(id=lesson_plan_id)
    
    context = {
        'live_class': live_class,
        'students': InterviewStudent.objects.filter(interview_class=live_class.interview_class),
        'lesson_data': live_class.lesson_data, 
        'current_question': live_class.current_question,  # current question being answered
    }

    return render(request, 'tutors-live-class.html', context)

@login_required
def end_class_view(request, class_id):
    live_class = get_object_or_404(LiveClass, interview_class__id=class_id, is_active=True)
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



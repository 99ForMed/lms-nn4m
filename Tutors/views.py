from django.shortcuts import render
import datetime

from .models import *

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
    context = {

    }
    return render(request, "tutor-strategies.html", context)
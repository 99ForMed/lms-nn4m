from functools import wraps
from django.shortcuts import redirect
from live_class.models import LiveClass

def check_live_class_active(view_func):
    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):
        live_class_id = kwargs['live_class_id']
        live_class = LiveClass.objects.get(id=live_class_id)
        if not live_class.is_active:
            return redirect('interview_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

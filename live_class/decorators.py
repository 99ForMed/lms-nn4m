from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# from .models import LiveCLass

def live_class_required(function):

    @login_required
    def wrap(request, *args, **kwargs):
        live_class = get_live_class(request.user) 
        if live_class:
            return function(request, *args, **kwargs)
        else:
            return redirect('/live_class_url')  # or wherever you want to redirect
    return wrap


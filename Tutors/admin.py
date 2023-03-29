from django.contrib import admin
from .models import *
from general.models import UcatProblem

# Register your models here.
admin.site.register(Tutor)
admin.site.register(UcatProblem)
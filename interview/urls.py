from django.contrib import admin
from django.urls import path, include

from .views import interview_dashboard_view

urlpatterns = [
    path('', interview_dashboard_view)
]

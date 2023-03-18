from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import dashboard_tutor_view, raise_issue_view, tutor_strategies_document


urlpatterns = [
    path('dashboard/', dashboard_tutor_view),
    path('dashboard/raise-issue/', raise_issue_view),
    path('dashboard/tutor-strategies/', tutor_strategies_document)
]
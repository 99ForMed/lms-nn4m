from django.contrib import admin
from django.urls import path, include

from .views import general_auth_view, login_view, create_account_view
from .views import login_success_view

urlpatterns = [
    path('', general_auth_view),
    path('login/', login_view),
    path('create_account/', create_account_view),
    path('login/login-success/', login_success_view)
]

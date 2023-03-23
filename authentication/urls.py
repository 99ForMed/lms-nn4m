from django.contrib import admin
from django.urls import path, include

from .views import general_auth_view, login_view, create_account_view
from .views import login_success_view, account_created_view

urlpatterns = [
    path('', general_auth_view),
    path('login/', login_view, name='login_view'),
    path('create-account/', create_account_view),
    path('login/login-success/', login_success_view),
    path('create-account/account-created/', account_created_view)
]

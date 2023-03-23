from django.contrib import admin
from django.urls import path, include

from .views import home_view, dashboard_view, course_page_view
from .views import course_video_view, add_comment, add_reply
from .views import upvote_comment
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('', home_view),
    path('dashboard/', dashboard_view),
    path('course-page/<int:sectionInstanceId>/', course_page_view),
    path('course-page/<int:sectionInstanceId>/video/<int:videoId>/', course_video_view),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login_view')), name='logout'),
    path('add_comment/', add_comment, name='add_comment'),
    path('add_reply/', add_reply, name='add_reply'),
    path('upvote_comment/', upvote_comment, name='upvote_comment')
]

from django.contrib import admin
from django.urls import path, include

from .views import home_view, dashboard_view, course_page_view
from .views import course_video_view, add_comment, add_reply
from .views import upvote_comment, submit_progress_view
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

from .views import maintenance_view
from .views import sitemap_view
from .views import zoom_start_view

urlpatterns = [
    path('', home_view),
    path('dashboard/', dashboard_view),
    path('course-page/<int:sectionInstanceId>/', course_page_view),
    path('course-page/<int:sectionInstanceId>/video/<int:videoId>/', course_video_view),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login_view')), name='logout'),
    path('add_comment/', add_comment, name='add_comment'),
    path('add_reply/', add_reply, name='add_reply'),
    path('upvote_comment/', upvote_comment, name='upvote_comment'),
    path('dashboard/submit-progress/', submit_progress_view, name='submit-progress'),
    path('under-maintenance/', maintenance_view),
    path('sitemap', sitemap_view),
    path('authenticate-zoom/', zoom_start_view)
]

handler404 = 'general.views.handler404'
handler500 = 'general.views.handler500'
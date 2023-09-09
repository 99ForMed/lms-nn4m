from django.contrib import admin
from django.urls import path, include

from .views import home_view, dashboard_view, course_page_view
from .views import course_video_view, add_comment, add_reply
from .views import upvote_comment, submit_progress_view
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

from .views import maintenance_view, alter_ucat_task_view
from .views import sitemap_view, coming_soon_view
from .views import zoom_start_view, zoom_authenticated_view

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
    path('zoom-start/', zoom_start_view),
    path('authenticate-zoom/', zoom_authenticated_view),
    path('coming-soon/', coming_soon_view, name = 'coming_soon'),

    # a lot of the endpoints are above this line because i decided 
    # To create this near the end of the project and

    path('alter-ucat-task/<str:done>/<str:ucat_task_content_exact>/<str:ucat_student_id>/', alter_ucat_task_view, name = 'alter_ucat_task')
]

handler404 = 'general.views.handler404'
handler500 = 'general.views.handler500'
handler403 = 'general.views.handler403'
CSRF_FAILURE_VIEW = 'general.views.csrf_failure'

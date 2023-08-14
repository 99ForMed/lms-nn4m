from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/interview/dashboard/$', consumers.LiveClassConsumer.as_asgi()),
    re_path(r'ws/interview/live-class/$', consumers.LiveClassConsumer.as_asgi()),
    re_path(r'ws/tutors/dashboard/$', consumers.LiveClassConsumer.as_asgi()),
    re_path(r'ws/live-class/tutors/$', consumers.LiveClassConsumer.as_asgi()),
    re_path(r'ws/interview/live-class/view_feedback/$', consumers.LiveClassConsumer.as_asgi()),
    re_path(r'ws/interview/live-class/select_question/$', consumers.LiveClassConsumer.as_asgi()),
    re_path(r'ws/interview/live-class/view_question/$', consumers.LiveClassConsumer.as_asgi()),
    re_path(r'ws/tutors/interview-class/$', consumers.LiveClassConsumer.as_asgi()),
    re_path(r'ws/interview/live-class/lesson_plan/', consumers.LiveClassConsumer.as_asgi()),
]
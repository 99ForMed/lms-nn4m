from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/interview/dashboard/$', consumers.LiveClassConsumer.as_asgi()),
    re_path(r'ws/interview/live-class/$', consumers.LiveClassConsumer.as_asgi()),
    re_path(r'ws/tutors/dashboard/$', consumers.LiveClassConsumer.as_asgi()),
    re_path(r'ws/live-class/tutors/$', consumers.LiveClassConsumer.as_asgi()),

]
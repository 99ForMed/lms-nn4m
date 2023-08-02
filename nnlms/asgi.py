"""
ASGI config for nnlms project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import live_class.routing  # replace appName with your app's name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nnlms.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            live_class.routing.websocket_urlpatterns
        )
    ),
})

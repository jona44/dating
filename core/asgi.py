import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import messaging.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from .middleware import WebSocketTokenAuthMiddleware

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": WebSocketTokenAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(messaging.routing.websocket_urlpatterns)
        )
    ),
})

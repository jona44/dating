from django.urls import path, re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/<uuid:room_id>/", ChatConsumer.as_asgi()),
    # Fallback to prevent 'No route found for path' errors if a client connects to the base WS URL
    re_path(r"^$", ChatConsumer.as_asgi()), 
]

from django.urls import path

from . import consumers

websocket_urlpatterns = [
    #re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    path("ws/chat/<slug:room_name>/", consumers.ChatConsumer.as_asgi())
]
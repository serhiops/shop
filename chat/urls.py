from django.urls import path, include
from . import views
from . import api
from rest_framework import routers


routerMessages = routers.SimpleRouter()
routerRooms = routers.SimpleRouter()

routerMessages.register(r'messages', api.MessagesApi )
routerRooms.register(r'rooms', api.RoomApi)

app_name = 'chat'
 
urlpatterns = [
    path('user_chats/', views.user_chats, name = 'user_chats'),

    path("api/v1/", include(routerMessages.urls), name = 'message-api'),
    path("api/v1/", include(routerRooms.urls), name = 'room-api'),
] 
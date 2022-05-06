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
    path('', views.index, name='index'),
    path('<slug:room_name>/', views.room, name='room'),

    path("api/v1/", include(routerMessages.urls)),
    path("api/v1/", include(routerRooms.urls)),
]
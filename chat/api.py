from rest_framework.viewsets import ModelViewSet

from myshop.models import Product
from .models import Messages, Room
#from myshop.models import CustomUser
from .serializers import RoomSerializer, MessagesSerializer
from rest_framework.response import Response
 
class MessagesApi(ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer

    def create(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True

        data = self.request.data
        room = data.get("room", False)
        if type(room) == int and int(room):
            data["room"] = room
        else:
            room = Room.objects.get(name = room).pk
            data["room"] = room
        data["author"] = self.request.user.pk

        request.data._mutable = _mutable
        return super().create(request, *args, **kwargs)

class RoomApi(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        room_name = request.data.get("name", False)
        product_id = request.data.get("product", False)
        if room_name and product_id:
            product = Product.objects.get(pk = product_id)
            room = Room.objects.get_or_create(name = room_name, product =product)[0]
            return Response({"data":RoomSerializer(room).data})
        return super().create(self, request, *args, **kwargs)
    
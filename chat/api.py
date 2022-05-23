from rest_framework.viewsets import ModelViewSet
from myshop.models import Product
from .models import Messages, Room
from .serializers import RoomSerializer, MessagesSerializer
from rest_framework.response import Response
from myshop.serializers import UserSerializer
from django.utils.text import slugify
from myshop.permissions.permissions_api import IsOwnerOrReadOnlyComent
from myshop.additionally.decorators import currentUser

class MessagesApi(ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
    permission_classes = (IsOwnerOrReadOnlyComent,)

    @currentUser
    def create(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True

        data = self.request.data
        room = data.get("room", False)
        if isinstance(room, int) and int(room):
            data["room"] = room
        else:
            room = Room.objects.get(name = room).pk
            data["room"] = room
        data["author"] = self.request.user.pk

        request.data._mutable = _mutable
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        room = Room.objects.get(pk = request.query_params['room'])
        return Response({'room':RoomSerializer(room).data})

class RoomApi(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    @currentUser
    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product", False)
        if product_id:
            product = Product.objects.get(pk = product_id)
            room_name = f'{product_id}-{request.user.id}-{slugify(product.salesman.username)}-{slugify(request.user.username)}-{slugify(product.name)}'
            room = Room.objects.get_or_create(name = room_name, product =product, user = request.user, salesman = product.salesman)[0]
            return Response({"data":RoomSerializer(room).data})
        return super().create(self, request, *args, **kwargs)

    @currentUser
    def list(self, request, *args, **kwargs):
        if not request.user.is_salesman:
            user_chats = Room.objects.filter(user = request.user)
        else:
            user_chats = Room.objects.filter(salesman = request.user)
        return Response({'user_chats': RoomSerializer(user_chats, many = True).data,
                        'current_user':UserSerializer(request.user).data})
    
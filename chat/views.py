from django.shortcuts import render
from myshop.serializers import ProductSerializer
from myshop.models import Product
from .models import Messages

def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    pk = int(request.path.split('/')[2].split("-")[0])

    product =ProductSerializer(Product.objects.get(pk = pk)).data

    messages = Messages.objects.filter(room__name = room_name)
    context = {
        'room_name': room_name,
        "product":product,
        "message":messages,
        "chatjs":True,
        'chatcss':True
    }
    return render(request, 'chat/room.html', context)
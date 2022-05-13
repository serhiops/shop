from rest_framework.serializers import ModelSerializer
from .models import Messages, Room
from myshop.serializers import UserSerializer, ProductSerializer

class MessagesSerializer(ModelSerializer):
    class Meta:
        model = Messages
        fields = "__all__"

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product'] = ProductSerializer(instance.product).data
        response['salesman'] = UserSerializer(instance.product.salesman).data
        response['user'] = UserSerializer(instance.user).data
        response['messages'] = MessagesSerializer(Messages.objects.filter(room = instance), many = True).data
        return response
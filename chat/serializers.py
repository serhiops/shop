from rest_framework.serializers import ModelSerializer
from .models import Messages, Room


class MessagesSerializer(ModelSerializer):
    class Meta:
        model = Messages
        fields = "__all__"

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
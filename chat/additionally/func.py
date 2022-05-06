from myshop.serializers import UserSerializer 
from chat.models import Room, Messages
from chat.serializers import MessagesSerializer

def serializer_user(user):
    return UserSerializer(user).data

def create_message(message, author, room_name):
    room = Room.objects.get(name = room_name)
    message = Messages.objects.create(room = room, message = message, author = author)
    return MessagesSerializer(message).data

def update_message(message_text, id):
    message = Messages.objects.get(pk = id)
    message.message = message_text
    message.save(update_fields=['message', 'updated'])
    return MessagesSerializer(message).data

def delete_message(id):
    message = Messages.objects.get(pk = id)
    message.is_active = False
    message.save()
    return MessagesSerializer(message).data
    
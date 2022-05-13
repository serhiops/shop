import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import get_user
from asgiref.sync import sync_to_async

from .additionally import func

REACT = False

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data, bytes_data = None):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == 'POST':
            data = {'type': 'chat_message','message': text_data_json['message']}
        elif type == 'PATCH':
            data = {'type':'update_chat_message', 'message': text_data_json['message'], 'message_id':text_data_json['message_id']}
        elif type == 'DELETE':
            data = {'type':'delete_chat_message', 'message_id':text_data_json["message_id"]}

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,data)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        if REACT:
            current_user = await sync_to_async(func.get_user_react,thread_sensitive=True)()
            user = await sync_to_async(func.get_serializer_user_react,thread_sensitive=True)()
        else:
            current_user = await get_user(self.scope)
            user = await sync_to_async(func.serializer_user,thread_sensitive=True)(current_user)
        message_api = await sync_to_async(func.create_message, thread_sensitive=True)(message,current_user, self.room_name)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            "message_api":message_api,
            'type':'POST'
        }))

    async def update_chat_message(self, data):
        message = await sync_to_async(func.update_message, thread_sensitive=True)(data["message"], int(data["message_id"]))
        if REACT:
            user = await sync_to_async(func.get_serializer_user_react,thread_sensitive=True)()
        else:
            user = await sync_to_async(func.serializer_user,thread_sensitive=True)(await get_user(self.scope))

        await self.send(text_data=json.dumps({
            'message':message,
            'type':'PATCH',
            'user': user,
        }))

    async def delete_chat_message(self, data):
        message_id = data["message_id"]
        
        message = await sync_to_async(func.delete_message, thread_sensitive=True)(message_id)
        if REACT:
            user = await sync_to_async(func.get_serializer_user_react,thread_sensitive=True)()
        else:
            user = await sync_to_async(func.serializer_user,thread_sensitive=True)(await get_user(self.scope))
        await self.send(text_data=json.dumps({
            'message':message,
            'type':'DELETE',
            'user':user
        }))



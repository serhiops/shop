import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import get_user
from asgiref.sync import sync_to_async
from .additionally import func, decorators


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data, bytes_data = None):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == 'POST':
            data = {'type': 'chat_message','message': text_data_json['message']}
        elif type == 'PATCH':
            data = {'type':'update_chat_message', 'message': text_data_json['message'], 'message_id':text_data_json['message_id']}
        elif type == 'DELETE':
            data = {'type':'delete_chat_message', 'message_id':text_data_json["message_id"]}

        await self.channel_layer.group_send(
            self.room_group_name,data)

    @decorators.currentUserAsync
    async def chat_message(self, event):
        message = event['message']
        message_api = await sync_to_async(func.create_message, thread_sensitive=True)(message,await get_user(self.scope), self.room_name)

        await self.send(text_data=json.dumps({
            'message': message,
            'user': event['current_user'],
            "message_api":message_api,
            'type':'POST'
        }))
        
    @decorators.currentUserAsync
    async def update_chat_message(self, data):
        message = await sync_to_async(func.update_message, thread_sensitive=True)(data["message"], int(data["message_id"]))
        await self.send(text_data=json.dumps({
            'message':message,
            'type':'PATCH',
            'user': data['current_user'],
        }))

    @decorators.currentUserAsync
    async def delete_chat_message(self, data):
        message_id = data["message_id"]
        message = await sync_to_async(func.delete_message, thread_sensitive=True)(message_id)
        await self.send(text_data=json.dumps({
            'message':message,
            'type':'DELETE',
            'user':data['current_user']
        }))



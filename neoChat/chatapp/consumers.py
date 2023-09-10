import json
import redis

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.contrib.auth import get_user_model

from .models import Message

conn = redis.Redis('localhost')

class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def save_message(self, sender, message, thread_name):
        Message.objects.create(sender=sender, message=message, thread_name=thread_name)

    @database_sync_to_async
    def get_user(self, username):
        return get_user_model().objects.filter(username=username).first()

    @database_sync_to_async
    def update_user_on_connect(self, id):
        user = get_user_model().objects.filter(id=id).first()
        user.email = '1'
        user.save()

    @database_sync_to_async
    def update_user_on_disconnect(self, id):
        user = get_user_model().objects.filter(id=id).first()
        user.email = ''
        user.save()


    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name'] 
        self.room_group_name = f'chat_{self.room_name}' 
        
        # await self.update_user_on_connect(self.scope['user'].id)
        conn.rpush('UserList',self.scope['user'].username)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name) 
        await self.accept()     

    async def disconnect(self, close_code):

        # await self.update_user_on_disconnect(self.scope['user'].id)
        conn.lrem('UserList',0,self.scope['user'].username)
        
        await self.channel_layer.group_discard(self.room_group_name, self.channel_layer)
        await self.disconnect(close_code)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)          # from Javascript chatsocket.send()
        message = text_data_json["message"]
        sender = text_data_json["username"]
        thread_name = text_data_json["thread_name"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'thread_name': thread_name,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        thread_name = event["thread_name"]

        

        sender_user_object = (await self.get_user(sender))

        await self.save_message(sender_user_object,message,thread_name)

        await self.send(text_data=json.dumps({"message": message,"sender":sender,"thread_name":thread_name}))



        # docker run --rm -p 6379:6379 redis:7
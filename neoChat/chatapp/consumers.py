import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.contrib.auth import get_user_model

from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def save_message(self, sender, message, thread_name):
        Message.objects.create(sender=sender, message=message, thread_name=thread_name)

    @database_sync_to_async
    def get_user(self, username):
        return get_user_model().objects.filter(username=username).first()

    @database_sync_to_async
    def get_messages(self, thread_name):

        messages = Message.objects.all()

        content = {
            'messages':self.messages_to_json(messages)
        }

        return content
    
    def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    
    def message_to_json(self,message):
        return {
            'sender': message.sender.username,
            'message': message.message,
            'timestamp': str(message.timestamp),
        }

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name'] 
        self.room_group_name = f'chat_{self.room_name}' 

        await self.channel_layer.group_add(self.room_group_name, self.channel_name) 

        # prev_messages = await self.get_messages(self.room_name)
        # print(prev_messages)

        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': prev_messages,
                
        #     },
        # ) 

        await self.accept()     

    async def disconnect(self, close_code):
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
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from pprint import pprint
from .models import Conversation, Message
from channels.db import database_sync_to_async
from django.contrib.auth.models import User



class ChatConsumer(AsyncWebsocketConsumer):
    
    # Function to connect to the websocket
    async def connect(self):
       # Checking if the User is logged in
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()

        else:
            # print(self.scope["user"])   # Can access logged in user details by using self.scope.user, Can only be used if AuthMiddlewareStack is used in the routing.py
            self.group_name = "test"  # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    # Function to disconnet the Socket
    async def disconnect(self, close_code):
        await self.close()
        # pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user']
        user = await self.get_user(user_id)
        conversation = await self.get_or_create_conversation(self.group_name)
        print(conversation)
        try: 
            await self.save_message(message, user, conversation)
        except:
            print('failed')
        # Send message to room group
        await self.channel_layer.group_send(
            'test',
            {
                'type': 'send_message',
                'text': {'message':message, 'user':user.username},
            }
        )


    async def send_message(self, event):
        await self.send(text_data=json.dumps(event["text"]))


    @database_sync_to_async
    def save_message(self, msg_body, user, conversation):
        return Message.objects.create(conversation=conversation, sender=user, body=msg_body)

    @database_sync_to_async
    def get_user(self, user_id):
        user_id = int(user_id)
        return User.objects.get(id=user_id)
                
    @database_sync_to_async
    def get_or_create_conversation(self, name):
        try:
            conversation = Conversation.objects.get(name=name)
            print('conversation exists')

        except:
            conversation = Conversation.objects.create(name=name)
            print('conversation created')
        
        return conversation

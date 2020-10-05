from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from pprint import pprint

class NotificationConsumer(AsyncWebsocketConsumer):
    
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
        user = text_data_json['user']

        # Send message to room group
        await self.channel_layer.group_send(
            'test',
            {
                'type': 'send_message',
                'text': {'message':message, 'user':user},
            }
        )

    # Custom Notify Function which can be called from Views or api to send message to the frontend
    async def send_message(self, event):
        await self.send(text_data=json.dumps(event["text"]))


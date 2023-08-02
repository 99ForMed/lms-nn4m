from channels.generic.websocket import AsyncWebsocketConsumer
import json

class LiveClassConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # This method is called when the websocket is handshaking as part of the connection process.
        await self.channel_layer.group_add(
            "live_class_1",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # This method is called when the WebSocket closes for any reason.
        pass

    async def receive(self, text_data):
        # This method is called when the WebSocket receives a message
        text_data_json = json.loads(text_data)
        response = ''
        # message = text_data_json['message']
        signal = text_data_json.get('signal', None)
        if not signal == None:
            response = 'LCSS'

            if text_data_json.get('signal') == 'action':
                response = {
                    'sourceUser': text_data_json['sourceUser'],
                    'type': 'change',
                    'presentingPerson': text_data_json['presentingPerson'],
                    'feedback': text_data_json['feedback']
                }
        
        # Send a message to the WebSocket
        await self.send(text_data=json.dumps({
            'signal': response
        }))
    
    async def signal(self, event):
        

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'meeting_join_url': event['meeting_join_url']
        }))

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            f"dashboard_{self.user.id}",  # Unique group for this user
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"dashboard_{self.user.id}", 
            self.channel_name
        )

    # Handles messages from WebSocket
    async def receive(self, text_data):
        pass  # No messages are expected from WebSocket in this example
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # user came online
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_status",
                "status": "online",
                "user": self.scope["user"].id,
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_status",
                "status": "offline",
                "user": self.scope["user"].id,
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_indicator",
                    "user": self.scope["user"].id,
                }
            )

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "user": str(event["user"]),
        }))

    async def user_status(self, event):
        await self.send(text_data=json.dumps({
            "type": "status",
            "user": str(event["user"]),
            "status": event["status"],
        }))

    async def chat_message(self, event):
        """Send message data as JSON to the client"""
        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "sender_id": event["sender_id"],
            "html": event["html"]
        }))

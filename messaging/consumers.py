import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

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
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_status",
                    "status": "online",
                    "user": str(self.scope["user"].id),
                }
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_status",
                    "status": "offline",
                    "user": str(self.scope["user"].id),
                }
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            print(f"Failed to decode WebSocket message: {text_data}")
            return

        message_type = data.get("type")
        
        if message_type == "typing":
            if self.scope["user"].is_authenticated:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "typing_indicator",
                        "user": str(self.scope["user"].id),
                    }
                )
        elif message_type == "chat_message":
            message_content = data.get("message")
            if message_content and self.scope["user"].is_authenticated:
                try:
                    # Save to DB asynchronously
                    db_message = await self.save_message(message_content)
                    
                    if db_message:
                        # Broadcast to group
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                "type": "chat_message",
                                "id": str(db_message['id']),
                                # Crucial: sender_id must match the frontend user.id (which is Profile ID)
                                "sender_id": str(db_message['sender_profile_id']),
                                "message": message_content,
                                "timestamp": db_message['timestamp'],
                            }
                        )
                except Exception as e:
                    print(f"Error in chat_message receive: {str(e)}")
        else:
            print(f"Unknown message type: {message_type}")

    @database_sync_to_async
    def save_message(self, content):
        from .models import Conversation, Message
        try:
            user = self.scope["user"]
            profile = user.profile
            conversation = Conversation.objects.get(id=self.room_id)
            
            db_message = Message.objects.create(
                conversation=conversation,
                sender=profile,
                body=content
            )
            return {
                'id': db_message.id,
                'sender_profile_id': profile.id,
                'timestamp': db_message.created_at.isoformat()
            }
        except Exception as e:
            print(f"Error saving message to DB: {str(e)}")
            return None

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
        data = {
            "type": "chat_message",
            "id": event.get("id"),
            "sender_id": event["sender_id"],
            "message": event.get("message", ""),
            "timestamp": event.get("timestamp"),
        }
        await self.send(text_data=json.dumps(data))

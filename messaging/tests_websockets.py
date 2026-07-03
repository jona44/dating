import json
import asyncio
from django.test import TransactionTestCase
from channels.testing import WebsocketCommunicator
from core.asgi import application
from django.contrib.auth import get_user_model
from accounts.models import Profile, User
from messaging.models import Conversation

class WebSocketConnectionTest(TransactionTestCase):
    def test_websocket_connectivity(self):
        """Testing websocket connectivity using sync-wrapper for async."""
        user = get_user_model().objects.create_user(email='ws_test@example.com', password='password123')
        profile = Profile.objects.get(user=user)
        conv = Conversation.objects.create()
        conv.participants.add(profile)

        async def run_test(user_id, conv_id):
            user = await get_user_model().objects.aget(id=user_id)
            communicator = WebsocketCommunicator(application, f"/ws/chat/{conv_id}/")
            communicator.scope['user'] = user
            
            connected, subprotocol = await communicator.connect()
            if not connected:
                return "Failed to connect"
            
            # Receive online status
            response = await communicator.receive_from()
            data = json.loads(response)
            
            # Send typing
            await communicator.send_to(text_data=json.dumps({"type": "typing"}))
            response = await communicator.receive_from()
            data = json.loads(response)
            
            await communicator.disconnect()
            return "Success"

        result = asyncio.run(run_test(user.id, conv.id))
        self.assertEqual(result, "Success")

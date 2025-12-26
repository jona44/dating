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
        async def run_test():
            user = await get_user_model().objects.create_user(email='ws_test@example.com', password='password123')
            profile = await Profile.objects.aget(user=user)
            conv = await Conversation.objects.acreate()
            await conv.participants.aadd(profile)

            communicator = WebsocketCommunicator(application, f"/ws/chat/{conv.id}/")
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

        # Explicitly setting a new event loop for this thread if needed, 
        # but TransactionTestCase is usually sync.
        result = asyncio.run(run_test())
        self.assertEqual(result, "Success")

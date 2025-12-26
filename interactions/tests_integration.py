from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Profile
from interactions.models import Like, Match
from messaging.models import Conversation

User = get_user_model()

class LikeMatchIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create two users
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123')
        
        # Complete their profiles to allow matching/discovery
        self.p1 = Profile.objects.get(user=self.user1)
        self.p1.is_complete = True
        self.p1.display_name = "User One"
        self.p1.save()
        
        self.p2 = Profile.objects.get(user=self.user2)
        self.p2.is_complete = True
        self.p2.display_name = "User Two"
        self.p2.save()

    def test_like_then_match_flow(self):
        """Test that user1 liking user2, then user2 liking user1, creates a match and conversation."""
        
        # 1. Login user1
        self.client.login(email='user1@example.com', password='password123')
        
        # 2. User1 likes User2
        like_url = reverse('like_profile', kwargs={'profile_id': self.p2.id})
        response = self.client.post(like_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Liked!")
        
        # Verify Like exists, but no Match yet
        self.assertTrue(Like.objects.filter(from_profile=self.p1, to_profile=self.p2).exists())
        self.assertFalse(Match.objects.filter(profile1=self.p1, profile2=self.p2).exists())
        self.assertFalse(Match.objects.filter(profile1=self.p2, profile2=self.p1).exists())
        
        self.client.logout()
        
        # 3. Login user2
        self.client.login(email='user2@example.com', password='password123')
        
        # 4. User2 likes User1
        like_url = reverse('like_profile', kwargs={'profile_id': self.p1.id})
        response = self.client.post(like_url)
        self.assertEqual(response.status_code, 200)
        
        # Should now be a Match and a Conversation
        self.assertContains(response, "It's a Match!")
        
        # Verify Match existence
        match = Match.objects.filter(
            (models.Q(profile1=self.p1, profile2=self.p2) | models.Q(profile1=self.p2, profile2=self.p1))
        ).first()
        self.assertIsNotNone(match)
        
        # Verify Conversation existence
        conv = Conversation.objects.filter(participants=self.p1).filter(participants=self.p2).first()
        self.assertIsNotNone(conv)
        self.assertEqual(conv.participants.count(), 2)

import django.db.models as models

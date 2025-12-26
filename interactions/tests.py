from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Profile
from interactions.models import Like, Match, Block, Report, Skip
from interactions.services import handle_like, block_user, report_user, is_blocked, skip_user
from messaging.models import Conversation

User = get_user_model()

class InteractionsServiceTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(email="user1@example.com", password="password")
        self.user2 = User.objects.create_user(email="user2@example.com", password="password")
        self.user3 = User.objects.create_user(email="user3@example.com", password="password")
        
        # Profiles are created by signals
        self.profile1 = self.user1.profile
        self.profile2 = self.user2.profile
        self.profile3 = self.user3.profile
        
        # Give them display names for better identification
        self.profile1.display_name = "User 1"
        self.profile1.save()
        self.profile2.display_name = "User 2"
        self.profile2.save()
        self.profile3.display_name = "User 3"
        self.profile3.save()

    def test_handle_like_creates_like(self):
        """Test that handle_like creates a Like object"""
        handle_like(self.profile1, self.profile2)
        self.assertTrue(Like.objects.filter(from_profile=self.profile1, to_profile=self.profile2).exists())
        self.assertFalse(Match.objects.exists())

    def test_handle_like_mutual_creates_match(self):
        """Test that mutual likes create a Match object"""
        handle_like(self.profile1, self.profile2)
        match = handle_like(self.profile2, self.profile1)
        
        self.assertIsNotNone(match)
        self.assertTrue(Match.objects.filter(profile1__in=[self.profile1, self.profile2], 
                                            profile2__in=[self.profile1, self.profile2]).exists())

    def test_handle_like_creates_conversation(self):
        """Test that a match automatically creates a Conversation with both profiles as participants"""
        handle_like(self.profile1, self.profile2)
        handle_like(self.profile2, self.profile1)
        
        self.assertEqual(Conversation.objects.count(), 1)
        conv = Conversation.objects.first()
        self.assertIn(self.profile1, conv.participants.all())
        self.assertIn(self.profile2, conv.participants.all())

    def test_handle_like_prevent_self_like(self):
        """Test that a user cannot like themselves"""
        result = handle_like(self.profile1, self.profile1)
        self.assertIsNone(result)
        self.assertEqual(Like.objects.count(), 0)

    def test_handle_like_duplicate_like(self):
        """Test that duplicate likes are handled gracefully and don't create multiple objects"""
        handle_like(self.profile1, self.profile2)
        result = handle_like(self.profile1, self.profile2)
        self.assertIsNone(result)
        self.assertEqual(Like.objects.count(), 1)

    def test_block_user_removes_existing_likes(self):
        """Test that blocking a user deletes any existing likes between them"""
        handle_like(self.profile1, self.profile2)
        handle_like(self.profile2, self.profile3) # Unrelated
        
        self.assertEqual(Like.objects.count(), 2)
        block_user(self.profile1, self.profile2)
        
        self.assertEqual(Like.objects.count(), 1)
        self.assertFalse(Like.objects.filter(from_profile=self.profile1, to_profile=self.profile2).exists())

    def test_block_user_removes_existing_matches(self):
        """Test that blocking a user deletes any existing matching between them"""
        handle_like(self.profile1, self.profile2)
        handle_like(self.profile2, self.profile1) # Match created
        
        self.assertEqual(Match.objects.count(), 1)
        block_user(self.profile1, self.profile2)
        
        self.assertEqual(Match.objects.count(), 0)
        self.assertEqual(Like.objects.count(), 0)

    def test_handle_like_prevents_blocked_likes(self):
        """Test that a user cannot like someone they have blocked or who has blocked them"""
        block_user(self.profile1, self.profile2)
        
        result = handle_like(self.profile1, self.profile2)
        self.assertIsNone(result)
        self.assertEqual(Like.objects.count(), 0)
        
        # Test reverse direction
        result = handle_like(self.profile2, self.profile1)
        self.assertIsNone(result)
        self.assertEqual(Like.objects.count(), 0)

    def test_is_blocked_symmetry(self):
        """Test that is_blocked returns True regardless of who did the blocking"""
        block_user(self.profile1, self.profile2)
        self.assertTrue(is_blocked(self.profile1, self.profile2))
        self.assertTrue(is_blocked(self.profile2, self.profile1))

    def test_report_user_creates_report(self):
        """Test that report_user creates a Report object"""
        report = report_user(self.profile1, self.profile2, reason="spam", description="Bot account")
        self.assertIsNotNone(report)
        self.assertEqual(Report.objects.count(), 1)
        self.assertEqual(report.reason, "spam")
        self.assertEqual(report.reported, self.profile2)


class SkipServiceTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="s1@example.com", password="password")
        self.user2 = User.objects.create_user(email="s2@example.com", password="password")
        self.profile1 = self.user1.profile
        self.profile2 = self.user2.profile

    def test_skip_user_creates_skip(self):
        skip = skip_user(self.profile1, self.profile2)
        self.assertIsNotNone(skip)
        self.assertTrue(Skip.objects.filter(from_profile=self.profile1, to_profile=self.profile2).exists())

    def test_skip_user_uniqueness(self):
        skip_user(self.profile1, self.profile2)
        skip_user(self.profile1, self.profile2)
        self.assertEqual(Skip.objects.count(), 1)


class DiscoverySelectorTests(TestCase):
    def setUp(self):
        from discovery.models import Preference
        from datetime import date
        self.user1 = User.objects.create_user(email="d1@example.com", password="password")
        self.user2 = User.objects.create_user(email="d2@example.com", password="password")
        self.user3 = User.objects.create_user(email="d3@example.com", password="password")
        
        self.p1 = self.user1.profile
        self.p2 = self.user2.profile
        self.p3 = self.user3.profile
        
        # Make them complete and visible
        for p in [self.p1, self.p2, self.p3]:
            p.is_complete = True
            p.is_visible = True
            p.birth_date = date(1990, 1, 1) # ~35 years old
            p.save()
            Preference.objects.get_or_create(profile=p, show_me=True)

    def test_discovery_excludes_skipped(self):
        from discovery.selectors import get_discovery_profiles
        
        # Initial: p1 sees p2 and p3
        profiles = get_discovery_profiles(self.p1)
        self.assertIn(self.p2, profiles)
        self.assertIn(self.p3, profiles)
        
        # p1 skips p2
        skip_user(self.p1, self.p2)
        
        # Now: p1 only sees p3
        profiles = get_discovery_profiles(self.p1)
        self.assertNotIn(self.p2, profiles)
        self.assertIn(self.p3, profiles)

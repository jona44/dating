from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Profile
from accounts.middleware import ProfileCompletionMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware

User = get_user_model()

class ProfileCompletionMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='test@example.com', password='password123')
        self.profile = Profile.objects.get(user=self.user)
        # Ensure profile starts incomplete
        self.profile.is_complete = False
        self.profile.onboarding_step = 1
        self.profile.save()

    def get_response(self, request):
        return None

    def test_authenticated_user_incomplete_profile_redirects(self):
        """Authenticated user with incomplete profile should be redirected to onboarding."""
        middleware = ProfileCompletionMiddleware(self.get_response)
        
        # Test a random path that is not onboarding or excluded
        request = self.factory.get('/discover/')
        request.user = self.user
        
        response = middleware(request)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('onboarding_step', kwargs={'step': 1}))

    def test_authenticated_user_complete_profile_no_redirect(self):
        """Authenticated user with complete profile should not be redirected."""
        self.profile.is_complete = True
        self.profile.save()
        
        middleware = ProfileCompletionMiddleware(lambda r: 'success')
        
        request = self.factory.get('/discover/')
        # Refresh user from DB to ensure no stale profile cache is used
        request.user = User.objects.get(id=self.user.id)
        
        response = middleware(request)
        
        self.assertEqual(response, 'success')

    def test_unauthenticated_user_no_redirect(self):
        """Unauthenticated user should not be redirected by this middleware."""
        from django.contrib.auth.models import AnonymousUser
        
        middleware = ProfileCompletionMiddleware(lambda r: 'success')
        
        request = self.factory.get('/discover/')
        request.user = AnonymousUser()
        
        response = middleware(request)
        
        self.assertEqual(response, 'success')

    def test_onboarding_path_no_redirect(self):
        """Onboarding paths themselves should not cause further redirects (avoid loops)."""
        middleware = ProfileCompletionMiddleware(lambda r: 'success')
        
        request = self.factory.get(reverse('onboarding_step', kwargs={'step': 1}))
        request.user = self.user
        
        response = middleware(request)
        
        self.assertEqual(response, 'success')

    def test_admin_path_no_redirect(self):
        """Admin paths should not be redirected, even for users with incomplete profiles (if they have perms)."""
        # Note: Middleware specifically allows is_admin_path or is_staff/is_superuser
        self.user.is_staff = True
        self.user.save()
        
        middleware = ProfileCompletionMiddleware(lambda r: 'success')
        
        request = self.factory.get('/admin/')
        request.user = self.user
        
        response = middleware(request)
        
        self.assertEqual(response, 'success')

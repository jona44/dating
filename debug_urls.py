
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
from django.urls import reverse
from django.test import RequestFactory

def debug_urls():
    rf = RequestFactory()
    request = rf.get('/', HTTP_HOST='localhost:8000')
    
    print(f"DEBUG: {settings.DEBUG}")
    print(f"ACCOUNT_DEFAULT_HTTP_PROTOCOL: {settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL}")
    print(f"SECURE_SSL_REDIRECT: {getattr(settings, 'SECURE_SSL_REDIRECT', False)}")
    
    callback_url = reverse('facebook_callback')
    print(f"Facebook callback path: {callback_url}")
    
    abs_url = request.build_absolute_uri(callback_url)
    print(f"Absolute callback URL (default): {abs_url}")
    
    # Check if allauth would force https
    from allauth.account.adapter import get_adapter
    adapter = get_adapter()
    print(f"Account Adapter Protocol: {adapter.get_protocol(request)}")

if __name__ == "__main__":
    debug_urls()

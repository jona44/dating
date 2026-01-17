import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

email = 'testuser3@gmail.com'
try:
    user = User.objects.get(email=email)
    print(f"User found: {user.email}")
    print(f"Active: {user.is_active}")
    print(f"Has usable password: {user.has_usable_password()}")
    print(f"Last login: {user.last_login}")
except User.DoesNotExist:
    print(f"User {email} not found")

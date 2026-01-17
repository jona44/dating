import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

email = 'testuser3@gmail.com'
try:
    user = User.objects.get(email=email)
    user.set_password('Password123!')
    user.save()
    print(f"Password for {email} reset to 'Password123!'")
except User.DoesNotExist:
    print(f"User {email} not found")

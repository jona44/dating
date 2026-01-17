import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

print("--- User List ---")
for u in User.objects.all():
    print(f"ID: {u.id} | Email: {u.email} | Active: {u.is_active}")
print("--- End ---")

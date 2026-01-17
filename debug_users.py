import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

print(f"User Model: {User}")
print(f"USERNAME_FIELD: {User.USERNAME_FIELD}")

users = User.objects.all()
print(f"Total users: {users.count()}")
for u in users:
    print(f"Email: {u.email} | Active: {u.is_active} | Staff: {u.is_staff} | ID: {u.id}")

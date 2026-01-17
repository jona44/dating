import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError

data = {
    'username': 'testuser6@gmail.com',
    'password': 'Password123!'
}

serializer = CustomTokenObtainPairSerializer(data=data)
try:
    if serializer.is_valid():
        print("Serializer is valid!")
        print(f"Tokens: {serializer.validated_data}")
    else:
        print(f"Serializer errors: {serializer.errors}")
except Exception as e:
    print(f"Error during validation: {e}")

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.serializers import CustomTokenObtainPairSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

print(f"User.USERNAME_FIELD: {User.USERNAME_FIELD}")

data = {
    "username": "testuser700@gmail.com",
    "email": "testuser700@gmail.com",
    "password": "Password123!"
}

serializer = CustomTokenObtainPairSerializer(data=data)
print(f"Is valid: {serializer.is_valid()}")
if not serializer.is_valid():
    print(f"Errors: {serializer.errors}")
else:
    print(f"Serializer username_field: {serializer.username_field}")
    print(f"Fields: {list(serializer.fields.keys())}")
    print(f"Validated data: {serializer.validated_data}")
    
    try:
        attrs = serializer.validated_data.copy()
        print("Calling validate...")
        result = serializer.validate(attrs)
        print("Validation successful")
    except Exception as e:
        import traceback
        traceback.print_exc()

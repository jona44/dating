import requests
import json
import random

email = f"testuser_{random.randint(1000, 9999)}@example.com"
password = "Password123!"

# 1. Register
reg_url = "http://127.0.0.1:8000/api/auth/register/"
reg_data = {
    "email": email,
    "password": password,
    "password2": password
}
reg_resp = requests.post(reg_url, json=reg_data)
print(f"Registration Status: {reg_resp.status_code}")
print(f"Registration Response: {reg_resp.text}")

if reg_resp.status_code == 201:
    # 2. Login
    login_url = "http://127.0.0.1:8000/api/auth/token/"
    login_data = {
        "email": email,
        "password": password
    }
    login_resp = requests.post(login_url, json=login_data)
    print(f"Login Status: {login_resp.status_code}")
    print(f"Login Response: {login_resp.text}")

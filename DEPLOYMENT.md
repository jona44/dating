# Deployment Guide - DatingApp

This guide covers the steps required to deploy the DatingApp to a production environment.

## 📋 Prerequisites
- Python 3.10+
- Redis (for Channels/WebSockets)
- PostgreSQL (Recommended for production)
- Nginx or similar web server
- Gunicorn or Daphne (ASGI server)

## 🛠️ Step-by-Step Installation

### 1. Environment Setup
Clone the repository and create a virtual environment:
```bash
git clone <repository-url>
cd dating
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```
Update the `.env` file with your production secrets, database URL, and Redis configuration.

### 3. Database Migrations
```bash
python manage.py migrate
```

### 4. Static Files
Collect static files for the web server to serve:
```bash
python manage.py collectstatic
```

### 5. Running the Application
For production, use **Daphne** as the ASGI server (required for WebSockets):
```bash
daphne -b 0.0.0.0 -p 8000 core.asgi:application
```

### 6. Process Management
It is recommended to use **Supervisor** or **systemd** to keep the Daphne process running.

#### Example systemd service file (`/etc/systemd/system/datingapp.service`):
```ini
[Unit]
Description=DatingApp ASGI Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/dating
ExecStart=/path/to/dating/venv/bin/daphne -b 0.0.0.0 -p 8000 core.asgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🔒 Security Checklist
- [ ] Set `DEBUG=False` in `.env`
- [ ] Ensure `SECRET_KEY` is a long, random string
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up HTTPS using Let's Encrypt (Certbot)
- [ ] Configure firewall to only allow ports 80 and 443

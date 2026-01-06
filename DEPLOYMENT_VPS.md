# Linux VPS Deployment Guide

**Target OS:** Ubuntu 22.04 / 24.04 LTS
**Specs:** 2 CPU, 4GB RAM

## 1. Initial Server Setup
SSH into your server:
```bash
ssh root@your-server-ip
```

Update system:
```bash
apt update && apt upgrade -y
```

Install dependencies:
```bash
apt install -y python3-venv python3-dev libmysqlclient-dev build-essential mysql-server redis-server nginx git
```

## 2. Database Setup via Terminal (MySQL)
Secure installation:
```bash
mysql_secure_installation
# Answer Y to everything, set a strong root password.
```

Create Database and User:
```bash
sudo mysql
```
Inside MySQL prompt:
```sql
CREATE DATABASE dating_db CHARACTER SET utf8mb4;
CREATE USER 'dating_user'@'localhost' IDENTIFIED BY 'STRONG_PASSWORD_HERE';
GRANT ALL PRIVILEGES ON dating_db.* TO 'dating_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## 3. Application Setup
Clone your repository (assumes you have pushed your code to GitHub/GitLab):
```bash
cd /var/www
git clone https://github.com/yourusername/dating.git
cd dating
```

Create Virtual Environment:
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Create `.env` file:
```bash
cp .env.example .env
nano .env
```
> **Edit .env**: Set `DEBUG=False`, `DATABASE_URL` (mysql://dating_user:STRONG_PASSWORD_HERE@localhost:3306/dating_db), and `ALLOWED_HOSTS` (your domain or IP).

Run Migrations and Collect Static:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## 4. Configure Systemd (Keep App Running)
Copy the service file:
```bash
cp deployment/daphne.service /etc/systemd/system/
systemctl daemon-reload
systemctl start daphne
systemctl enable daphne
```
*Check status:* `systemctl status daphne`

## 5. Configure Nginx (Web Server)
Copy config and enable:
```bash
cp deployment/nginx.conf /etc/nginx/sites-available/dating
ln -s /etc/nginx/sites-available/dating /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t  # Test config
systemctl restart nginx
```

## 6. HTTPS (SSL)
Install Certbot:
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 7. Troubleshooting
- **App Logs:** `journalctl -u daphne -f`
- **Nginx Logs:** `tail -f /var/log/nginx/error.log`

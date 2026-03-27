# 🚀 GUÍA DE DESPLIEGUE - A-Space Shop en VPS

## 1. REQUISITOS PREVIOS

### En tu máquina local (preparación):
- ✅ Python 3.10+ instalado
- ✅ Archivo `.env` configurado con credenciales
- ✅ Base de datos MySQL 5.7+ lista

### En el VPS (Linux, Ubuntu 20.04 o superior):
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.10 python3.10-venv python3-pip mysql-server nginx supervisor redis-server git certbot python3-certbot-nginx
```

---

## 2. PREPARAR LA APP LOCALMENTE

### Actualizar `.env` con valores REALES:
```bash
# Variables críticas para producción
SECRET_KEY=tu-clave-segura-muy-larga-y-aleatoria-cambiar-en-produccion
DATABASE_URI=mysql+mysqlconnector://usuario:password@localhost:3306/ecommerce
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-password-seguro
STRIPE_SECRET_KEY=sk_live_xxxxxxx  # De https://dashboard.stripe.com/
STRIPE_PUBLISHABLE_KEY=pk_live_xxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxx  # Genera en Stripe webhook
POSTAL_NINJA_API_KEY=tu-token
COPOMEX_TOKEN=tu-token
FLASK_ENV=production
FLASK_DEBUG=0
PORT=8000
```

### Actualizar `requirements.txt` si es necesario:
```bash
pip install -r requirements.txt
pip freeze > requirements.txt
```

---

## 3. DESPLEGAR EN VPS

### 3.1 Conectar al VPS:
```bash
ssh usuario@tu-vps.com
```

### 3.2 Crear estructura de directorios:
```bash
sudo mkdir -p /var/www/ecommerce
sudo chown $USER:$USER /var/www/ecommerce
cd /var/www/ecommerce
```

### 3.3 Clonar o subir código:
```bash
# Opción A: Clonar desde Git
git clone https://github.com/tuusuario/ecommerce.git .

# Opción B: Subir archivos via rsync/scp
rsync -avz ~/Desktop/Ecommerce/ usuario@tu-vps:/var/www/ecommerce/
```

### 3.4 Crear base de datos:
```bash
sudo mysql -u root -p < ecommerce_produccion.sql
```

O manualmente:
```bash
mysql -u root -p
> CREATE DATABASE ecommerce CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
> CREATE USER 'ecommerce'@'localhost' IDENTIFIED BY 'password-seguro';
> GRANT ALL PRIVILEGES ON ecommerce.* TO 'ecommerce'@'localhost';
> FLUSH PRIVILEGES;
> EXIT;
```

### 3.5 Crear y activar venv:
```bash
cd /var/www/ecommerce
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install gunicorn  # Para producción
```

### 3.6 Crear archivo `.env` en VPS:
```bash
nano /var/www/ecommerce/.env
```

Pega las variables del paso 2. Guarda con `Ctrl+X`, `Y`, `Enter`.

### 3.7 Permisos de carpetas:
```bash
sudo chown -R www-data:www-data /var/www/ecommerce
sudo chmod -R 755 /var/www/ecommerce
sudo chmod -R 775 /var/www/ecommerce/static/comprobantes
sudo chmod -R 775 /var/www/ecommerce/uploads
```

---

## 4. CONFIGURAR GUNICORN (WSGI Server)

### 4.1 Crear archivo de servicio:
```bash
sudo nano /etc/systemd/system/ecommerce.service
```

Pega esto:
```ini
[Unit]
Description=A-Space Shop Flask App
After=network.target mysql.service redis.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/ecommerce
Environment="PATH=/var/www/ecommerce/venv/bin"
ExecStart=/var/www/ecommerce/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind unix:/var/www/ecommerce/ecommerce.sock \
    --timeout 30 \
    --access-logfile /var/log/ecommerce/access.log \
    --error-logfile /var/log/ecommerce/error.log \
    wsgi:application

Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

### 4.2 Crear directorio de logs:
```bash
sudo mkdir -p /var/log/ecommerce
sudo chown www-data:www-data /var/log/ecommerce
```

### 4.3 Iniciar servicio:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ecommerce
sudo systemctl start ecommerce
sudo systemctl status ecommerce
```

Verifica logs:
```bash
sudo tail -f /var/log/ecommerce/error.log
```

---

## 5. CONFIGURAR NGINX (Reverse Proxy + HTTPS)

### 5.1 Crear configuración Nginx:
```bash
sudo nano /etc/nginx/sites-available/ecommerce
```

Pega esto:
```nginx
upstream ecommerce_app {
    server unix:/var/www/ecommerce/ecommerce.sock fail_timeout=0;
}

# Redirigir HTTP a HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name tu-dominio.com www.tu-dominio.com;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# Servidor HTTPS principal
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;
    client_max_body_size 20M;

    # Certificados SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Headers de seguridad
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://ecommerce_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /static/ {
        alias /var/www/ecommerce/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 5.2 Habilitar sitio:
```bash
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/ecommerce
sudo rm /etc/nginx/sites-enabled/default  # Desactivar default
sudo nginx -t  # Verificar sintaxis
sudo systemctl restart nginx
```

### 5.3 Certificado SSL (Let's Encrypt):
```bash
sudo certbot certonly --webroot -w /var/www/certbot -d tu-dominio.com -d www.tu-dominio.com
```

Para renovación automática:
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## 6. CONFIGURAR REDIS (Cache y Rate Limiting)

```bash
# Iniciar Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Verificar
redis-cli ping  # Debe responder PONG
```

---

## 7. CONFIGURAR SUPERVISOR (Monitoreo)

### 7.1 Crear archivo:
```bash
sudo nano /etc/supervisor/conf.d/ecommerce.conf
```

Pega:
```ini
[program:ecommerce]
command=/var/www/ecommerce/venv/bin/gunicorn --workers 4 --bind unix:/var/www/ecommerce/ecommerce.sock wsgi:application
directory=/var/www/ecommerce
user=www-data
environment=PATH="/var/www/ecommerce/venv/bin"
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/ecommerce/supervisor.log
```

### 7.2 Activar:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start ecommerce
sudo supervisorctl status
```

---

## 8. VERIFICAR DESPLIEGUE

```bash
# Ver estado de la app
sudo systemctl status ecommerce

# Ver logs
sudo tail -50 /var/log/ecommerce/error.log

# Probar conexión a BD
mysql -u ecommerce -p ecommerce -e "SELECT COUNT(*) FROM usuarios;"

# Acceder a tu dominio
curl https://tu-dominio.com
```

---

## 9. MONITOREO Y MANTENIMIENTO

### Backup de base de datos (cron):
```bash
# Crear script
sudo nano /usr/local/bin/backup-ecommerce.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/backups/ecommerce"
DATE=$(date +%Y-%m-%d_%H:%M:%S)
mysqldump -u ecommerce -p$MYSQL_PASS ecommerce > $BACKUP_DIR/db_$DATE.sql
gzip $BACKUP_DIR/db_$DATE.sql
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete  # Borrar backups > 30 días
```

```bash
sudo chmod +x /usr/local/bin/backup-ecommerce.sh

# Agregar a crontab
sudo crontab -e
# Agregar: 0 2 * * * /usr/local/bin/backup-ecommerce.sh  (2 AM diarios)
```

### Actualizar código (Git):
```bash
cd /var/www/ecommerce
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart ecommerce
```

---

## 10. CHECKLIST FINAL

- [ ] Domain apunta a VPS IP
- [ ] `.env` con credenciales reales
- [ ] BD creada con `ecommerce_produccion.sql`
- [ ] Certificado SSL activo
- [ ] Nginx escucha 80/443
- [ ] Gunicorn/Systemd activo
- [ ] Redis corriendo
- [ ] STRIPE_WEBHOOK_SECRET configurado
- [ ] MAIL_USERNAME/PASSWORD funcionando
- [ ] Logs monitoreados
- [ ] Backups automatizados

---

## 🆘 TROUBLESHOOTING

### App no inicia:
```bash
cd /var/www/ecommerce
source venv/bin/activate
python wsgi.py  # Ver error directo
```

### Nginx 502 Bad Gateway:
```bash
# Verificar socket
ls -la /var/www/ecommerce/ecommerce.sock

# Reiniciar gunicorn
sudo systemctl restart ecommerce
```

### Base de datos rechaza conexión:
```bash
mysql -u ecommerce -p ecommerce -e "SELECT 1;"
# Ver error en /var/log/ecommerce/error.log
```

### SSL no funciona:
```bash
sudo certbot renew --dry-run  # Simular renovación
sudo systemctl restart nginx
```

---

**¡Despliegue completado! Tu app está lista para producción.** 🎉

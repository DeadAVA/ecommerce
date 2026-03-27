# Checklist de Despliegue a Producción

## Fase Pre-Despliegue (Antes de Subir a Servidor)

### ✅ Código y Repositorio
- [ ] Todos los cambios están en Git
- [ ] No hay credenciales en el código
- [ ] `.env` está en `.gitignore`
- [ ] `requirements.txt` está actualizado (`pip freeze > requirements.txt`)
- [ ] Código está cleanado (sin debugging prints)
- [ ] No hay archivos temporales o de desarrollo
- [ ] Se ejecutó `pip install --upgrade -r requirements.txt` al menos una vez

### ✅ Testing
- [ ] Toda la funcionalidad fue testeada en desarrollo
- [ ] El registro de usuarios funciona
- [ ] El login y logout funcionan
- [ ] Se puede agregar productos al carrito
- [ ] Checkout completo funciona
- [ ] PayPal integración testeada (Sandbox)
- [ ] Admin panel es accesible
- [ ] El sistema de emails funciona en desarrollo

### ✅ Configuración Segura
- [ ] `SECRET_KEY` es fuerte y aleatorio
- [ ] `DEBUG=False` en producción
- [ ] `FLASK_ENV=production`
- [ ] Variables de entorno están definidas correctamente
- [ ] PayPal en modo `live` (NO sandbox)
- [ ] SSL/HTTPS configurado
- [ ] Cookies tienen `SECURE=True` y `HTTPONLY=True`

### ✅ Base de Datos
- [ ] Base de datos MySQL creada en servidor
- [ ] Usuario de BD con permisos mínimos necesarios
- [ ] Backup de BD de desarrollo existe
- [ ] Migraciones ejecutadas si existen
- [ ] Índices creados en columnas clave

### ✅ Dependencias Externas
- [ ] Llave de API de PayPal verificada
- [ ] Credenciales de API Zonas verificadas
- [ ] Servidor SMTP de email configurado y testeado
- [ ] Certificado SSL adquirido o automático (Let's Encrypt)
- [ ] Dominios apuntan correctamente

### ✅ Documentación
- [ ] README.md actualizado
- [ ] Instrucciones de despliegue documentadas
- [ ] Secrets/Credenciales documentadas en lugar seguro
- [ ] Procedimiento de rollback documentado
- [ ] Contactos de emergencia listados

---

## Fase de Despliegue

### 🔧 Servidor y Networking
- [ ] VPS/Servidor seleccionado y configurado
- [ ] Firewall configurado (puertos 80, 443 abiertos)
- [ ] Dominio apunta al servidor
- [ ] DNS propagado correctamente
- [ ] SSH configurado sin contraseña (key-based auth)
- [ ] Actualizar sistema: `sudo apt update && sudo apt upgrade -y`

### 🔐 Seguridad de Servidor
- [ ] Fail2ban instalado
- [ ] SSH en puerto no estándar
- [ ] Passwordless sudo deshabilitado
- [ ] Firewall UFW configurado
- [ ] Certificado SSL instalado (Let's Encrypt)
- [ ] Auto-renovación de certificados configurada
- [ ] Headers HTTP de seguridad configurados

### 📦 Dependencias del Servidor
- [ ] Python 3.10+ instalado
- [ ] MySQL 8.0+ instalado y securizado
- [ ] Nginx instalado y configurado
- [ ] Gunicorn instalado en venv
- [ ] Git instalado

### 🚀 Despliegue de Aplicación
- [ ] Directorio de aplicación creado (`/var/www/ecommerce`)
- [ ] Repositorio clonado
- [ ] Entorno virtual configurado
- [ ] `pip install -r requirements.txt` ejecutado
- [ ] `.env` configurado con valores de producción
- [ ] Gunicorn systemd service creado
- [ ] Nginx proxy configurado
- [ ] Static files collectados (si uso Flask Assets)

### 🌐 Nginx Configuration
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name ecommerce.com www.ecommerce.com;
    
    # Redirect HTTP a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name ecommerce.com www.ecommerce.com;
    
    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/ecommerce.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ecommerce.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Static files
    location /static/ {
        alias /var/www/ecommerce/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Uploads
    location /uploads/ {
        alias /var/www/ecommerce/uploads/;
        expires 7d;
    }
}
```

### 🗄️ Base de Datos
- [ ] BD creada en MySQL
- [ ] Tablas creadas (`python` → `from app import db; db.create_all()`)
- [ ] Usuario de BD creado con permisos limitados
- [ ] Backup automático configurado
- [ ] Replica/Failover configurado (si needed)

### 📊 Monitoreo y Logging
- [ ] Logs de Nginx configurados
- [ ] Logs de Gunicorn configurados
- [ ] Logs de la aplicación configurados
- [ ] Log rotation configurado (logrotate)
- [ ] Monitoreo de CPU/RAM configurado
- [ ] Health checks configurados

---

## Verificaciones Post-Despliegue

### ✅ Acceso y Funcionalidad
- [ ] Sitio está accesible en el dominio
- [ ] HTTPS funciona sin warnings
- [ ] HTTP redirige a HTTPS
- [ ] Registro de usuario funciona
- [ ] Login/Logout funciona
- [ ] Carrito funciona
- [ ] Checkout funciona
- [ ] PayPal integración funciona (modo live)
- [ ] Emails se envían
- [ ] Admin panel accesible

### ✅ Performance
- [ ] Home page carga en < 2s
- [ ] Catálogo carga rápido
- [ ] Búsqueda es rápida
- [ ] Checkout no tiene lag
- [ ] No hay errores 500 en logs

### ✅ Seguridad
- [ ] SSL se valida (A+ en ssllabs.com)
- [ ] Security headers presentes
- [ ] CSRF protection funciona
- [ ] XSS protection funciona
- [ ] SQL injection no es posible
- [ ] No hay credenciales expuestas
- [ ] Contraseñas están hasheadas
- [ ] JWT tokens funcionan

### ✅ Datos
- [ ] Base de datos está íntegra
- [ ] Backups se están haciendo
- [ ] Disaster recovery plan está documentado
- [ ] Datos sensibles están encriptados

### ✅ Logs y Monitoreo
- [ ] Error logs están limpios
- [ ] No hay warnings importantes
- [ ] Monitoreo está activo
- [ ] Alertas funcionan
- [ ] Estadísticas de acceso son razonables

---

## Mantenimiento Operacional

### 📅 Tareas Diarias
- [ ] Revisar error logs
- [ ] Verificar uptime
- [ ] Chequear backups completaron

### 📅 Tareas Semanales
- [ ] Revisar estadísticas de uso
- [ ] Verificar parámetros de performance
- [ ] Revisar logs de seguridad
- [ ] Testear backup restoration

### 📅 Tareas Mensuales
- [ ] Actualizar paquetes de seguridad (`apt update && apt upgrade`)
- [ ] Analizar logs de acceso y errores
- [ ] Revisión de seguridad completa
- [ ] Reunión de revisión del proyecto

### 📅 Tareas Trimestrales
- [ ] Disaster recovery drill
- [ ] Actualización de dependencias (Python packages)
- [ ] Auditoría de seguridad completa
- [ ] Revisión de certificados SSL
- [ ] Análisis de rendimiento y escalabilidad

---

## Rollback Plan (En caso de problemas)

### Procedimiento de Rollback Rápido

```bash
# 1. Detener aplicación
sudo systemctl stop ecommerce

# 2. Revertir código a versión anterior
cd /var/www/ecommerce
git log --oneline | head -20  # Ver commits
git checkout <commit-hash-anterior>

# 3. Reinstalar dependencias (si necesario)
source venv/bin/activate
pip install -r requirements.txt

# 4. Ejecutar migraciones revertidas (si aplica)
# python manage.py db downgrade

# 5. Reiniciar aplicación
sudo systemctl start ecommerce

# 6. Verificar logs
sudo tail -f /var/log/syslog | grep ecommerce
```

### Rollback de Base de Datos

```bash
# 1. Restaurar backup anterior
mysql -u ecommerce_user -p ecommerce_db < backup_anterior.sql

# 2. Verificar integridad
mysql -u ecommerce_user -p ecommerce_db
> CHECK TABLE user, product, order, ...

# 3. Reiniciar aplicación
sudo systemctl restart ecommerce
```

---

## Escalabilidad Futura

- [ ] Plan de scaling horizontal documentado
- [ ] Load balancer identificado (Nginx o HAProxy)
- [ ] Caching layer planeado (Redis)
- [ ] CDN para static files considerado (CloudFlare)
- [ ] Database replication planeada
- [ ] Cluster de aplicación considerado

---

## Checklist Final de Seguridad

```bash
# Verificar no hay archivos sensibles
find . -name ".env" -o -name "*.key" -o -name "*.pem"

# Verificar no hay debugging
grep -r "print(" --include="*.py" | grep -v "^Binary"
grep -r "DEBUG\s*=\s*True" --include="*.py"

# Verificar .gitignore
cat .gitignore | grep -E ".env|__pycache__|venv|.env"

# Verificar permisos
ls -la /var/www/ecommerce
# Debe ser: drwxr-xr-x usuario:usuario

# Verificar base de datos
mysql -u root -p -e "SELECT user, host FROM mysql.user;"
# No debe haber usuario root con password vacía

# Verificar SSL
openssl s_client -connect ecommerce.com:443 -tls1_2

# Verificar Nginx
nginx -t  # Debe mostrar "successful"
```

---

## Contactos de Emergencia

| Rol | Nombre | Teléfono | Email |
|-----|--------|----------|-------|
| Administrador | [Nombre] | [Número] | [Email] |
| DevOps | [Nombre] | [Número] | [Email] |
| Soporte | [Nombre] | [Número] | [Email] |

---

## Documentación de Referencia

- Servidor: [Dirección IP / Dominio]
- Panel de Control: [URL del hosting]
- Base de Datos: [Host / Puerto]
- DNS: [Proveedor]
- SSL: [Certificado / Renovación]
- Backups: [Ubicación / Schedule]

---

**Último Despliegue:** [Fecha/Hora]  
**Versión Actual:** [X.X.X]  
**Status:** [Producción / En Mantenimiento]

---

✅ Cuando hayas completado todos los checkpoints, el proyecto está listo para producción.

**Recuerda:** La seguridad es un proceso continuo, no un evento único. Realiza revisiones periódicas.

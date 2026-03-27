# Guía de HTTPS para la Aplicación Ecommerce

## 🔒 Configuración de HTTPS

La aplicación Flask ahora está configurada para soportar HTTPS de forma segura.

### Opciones de Ejecución

#### 1. **Desarrollo Local (HTTP)**
```bash
python app.py
```
La aplicación se ejecutará en `http://localhost:5000` si no hay certificados.

#### 2. **Desarrollo con HTTPS (Certificados Autofirmados)**

Primero, genera certificados autofirmados:
```bash
python generate_certs.py
```

Esto creará:
- `certs/cert.pem` - Certificado
- `certs/key.pem` - Clave privada

Luego ejecuta la aplicación:
```bash
python app.py
```

La aplicación se ejecutará en `https://localhost:443` (o `https://localhost`)

### 3. **Producción (Certificados Válidos)**

Para producción, necesitas certificados de una autoridad certificadora confiable:

#### Opciones:
- **Let's Encrypt** (Gratis): https://letsencrypt.org/
- **AWS Certificate Manager**: Para aplicaciones en AWS
- **DigiCert, Comodo, etc.**: Certificados pagos de confianza

#### Con Let's Encrypt (Linux/Mac):
```bash
sudo apt-get install certbot
sudo certbot certonly --standalone -d tudominio.com
```

#### Con Docker + Let's Encrypt:
```bash
docker run --rm -it certbot/certbot certonly --standalone -d tudominio.com
```

### Cambios Realizados en la Aplicación

#### 1. **Imports Agregados**
```python
import os
import ssl
import logging
```

#### 2. **Configuración de Seguridad en app.py**
```python
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

#### 3. **Headers de Seguridad Mejorados**
- `Strict-Transport-Security` (HSTS): Fuerza HTTPS
- `Content-Security-Policy`: Protege contra XSS
- `X-Frame-Options`: Protege contra clickjacking
- `X-Content-Type-Options`: Previene MIME sniffing
- `X-Permitted-Cross-Domain-Policies`: Seguridad adicional

#### 4. **Manejo de Certificados en app.py**
```python
try:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain('certs/cert.pem', 'certs/key.pem')
    app.run(debug=True, ssl_context=ssl_context, host='0.0.0.0', port=443)
except (FileNotFoundError, OSError):
    logger.warning("Certificados SSL no encontrados. Ejecutando en HTTP")
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Errores Comunes

#### ❌ "Permission denied" al usar puerto 443
**Solución**: 
- En Windows: Ejecutar como Administrador
- En Linux/Mac: `sudo python app.py`
- Alternativa: Usar puerto 8443: `app.run(port=8443)`

#### ❌ "No such file or directory: certs/cert.pem"
**Solución**: 
```bash
python generate_certs.py
```

#### ❌ Navegador muestra "conexión no segura"
**Causa**: Los certificados autofirmados no son confiables
**Solución**: En Chrome/Firefox, acepta la excepción (solo desarrollo) o usa certificados válidos en producción

### Variables de Entorno (.env)

Crea un archivo `.env` en la raíz del proyecto:
```env
SECRET_KEY=tu_clave_secreta_super_segura_aqui
DATABASE_URI=mysql+mysqlconnector://usuario:contraseña@localhost/ecommerce
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app_gmail
POSTAL_NINJA_API_KEY=tu_api_key_aqui
```

### Checklist de Seguridad

- [x] Importar `os`, `ssl`, `logging`
- [x] Configurar HTTPS en config.py
- [x] Headers de seguridad mejorados (HSTS, CSP, etc.)
- [x] Validación de inputs mejorada
- [x] Try-catch en rutas críticas
- [x] Logging de errores
- [x] Manejo de certificados SSL
- [x] Actualización de contraseñas en variables de entorno
- [x] Validación de stock antes de crear pedidos

### Próximos Pasos Recomendados

1. **Generar certificados** para desarrollo:
   ```bash
   python generate_certs.py
   ```

2. **Crear archivo .env** con variables seguras

3. **Actualizar credentials** en variables de entorno

4. **Testear HTTPS** con la aplicación:
   ```bash
   python app.py
   ```

5. **En producción**: Obtener certificados válidos de Let's Encrypt o una CA confiable

### Referencias

- [Flask HTTPS](https://flask.palletsprojects.com/en/2.3.x/deploying/wsgi-eventlet/)
- [OWASP Security Headers](https://owasp.org/www-project-secure-headers/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)

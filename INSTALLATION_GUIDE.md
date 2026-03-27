# Instalación y Configuración Paso a Paso - GUÍA COMPLETA

## 📋 Índice
1. [Pre-requisitos](#pre-requisitos)
2. [Instalación en Windows](#instalación-en-windows)
3. [Instalación en Linux/Mac](#instalación-en-linuxmac)
4. [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
5. [Configuración de Base de Datos](#configuración-de-base-de-datos)
6. [Verificación de Instalación](#verificación-de-instalación)
7. [Primeros Pasos](#primeros-pasos)
8. [Solución de Problemas](#solución-de-problemas)

---

## Pre-requisitos

Antes de comenzar, verifica que tienes:

### Software Requerido
- [ ] Python 3.8 o superior
- [ ] Git
- [ ] Un editor de código (VS Code recomendado)
- [ ] Terminal/Command Prompt
- [ ] Navegador web moderno

### Verificar Instalación Existente

**Windows (PowerShell):**
```powershell
# Verificar Python
python --version

# Verificar Git
git --version

# Si no están instalados, descargar desde:
# Python: https://www.python.org/downloads/
# Git: https://git-scm.com/download/win
```

**Linux/Mac (Terminal):**
```bash
# Verificar Python
python3 --version

# Verificar Git
git --version

# Instalar si no existen (Ubuntu/Debian)
sudo apt-get install python3.10 git
```

---

## Instalación en Windows

### Paso 1: Descargar el Proyecto

```powershell
# Abrir PowerShell como usuario normal

# Ir a la carpeta donde quieres el proyecto
cd C:\Users\TuUsuario\Desktop

# Clonar repositorio
git clone https://github.com/DeadAVA/ecommerce.git

# Entrar al directorio
cd ecommerce

# Ver contenido descargado
ls
```

**Salida esperada:**
```
    Directory: C:\Users\alanv\Desktop\ecommerce

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         3/27/2026   10:30 AM                admin
d-----         3/27/2026   10:30 AM                api_zonas
d-----         3/27/2026   10:30 AM                models
d-----         3/27/2026   10:30 AM                static
d-----         3/27/2026   10:30 AM                templates
d-----         3/27/2026   10:30 AM                uploads
d-----         3/27/2026   10:30 AM                utils
-a----         3/27/2026   10:30 AM           5420 app.py
-a----         3/27/2026   10:30 AM           1200 config.py
-a----         3/27/2026   10:30 AM            2300 requirements.txt
```

### Paso 2: Crear Entorno Virtual

```powershell
# Crear carpeta venv
python -m venv venv

# Debería aparecer:
# (Creará la carpeta venv automáticamente)
```

### Paso 3: Activar Entorno Virtual

```powershell
# Ejecutar script de activación
.\venv\Scripts\Activate.ps1

# Si recibes error de políticas de ejecución:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Después de activado, deberías ver "(venv)" antes del prompt
# Ejemplo: (venv) PS C:\Users\TuUsuario\Desktop\ecommerce>
```

**¡Importante!** El entorno virtual debe estar siempre activado cuando trabajes en el proyecto.

### Paso 4: Actualizar pip

```powershell
# Asegurar que pip está actualizado
python -m pip install --upgrade pip

# Salida esperada:
# Successfully installed pip-X.X.X
```

### Paso 5: Instalar Dependencias

```powershell
# Instalar todas las dependencias del proyecto
pip install -r requirements.txt

# Esto puede tomar 2-5 minutos dependiendo de tu conexión
# Verás líneas como:
# Collecting flask==2.3.2
# Downloading flask-2.3.2-py3-none-any.whl (101.8 MB)
# ...
# Successfully installed [lista de paquetes]
```

**Si ocurren errores en Windows:**
```powershell
# Reinstalar con upgrade
pip install --upgrade -r requirements.txt

# Si sigue fallando, instalar individual
pip install Flask==2.3.2
pip install Flask-SQLAlchemy==3.0.5
# ... etc
```

### Paso 6: Verificar Instalación

```powershell
# Verificar que todos los paquetes instalaron correctamente
pip list

# Debería mostrar (al menos):
# Flask                    2.3.2
# Flask-Login              0.6.2
# Flask-SQLAlchemy         3.0.5
# PyJWT                    2.8.0
# python-dotenv            1.0.0
# ... y más
```

### Paso 7: Crear Archivo .env

```powershell
# Crear archivo .env
New-Item .env -ItemType File

# Abrir con editor (notepad)
notepad .env
```

En el archivo `.env` que se abre, copia y modifica:

```env
# CONFIGURACIÓN FLASK
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_SECRET_KEY=mi_clave_secreta_super_segura_cambiar_123456

# BASE DE DATOS
DATABASE_URL=sqlite:///ecommerce.db

# PAYPAL (Usar credenciales sandbox para testing)
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=AZx_x1xX1x1Xx1x
PAYPAL_SECRET=xxx

# EMAIL
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app_google

# JWT
JWT_SECRET_KEY=tu_jwt_key_cambiar

# API ZONAS
API_ZONAS_USER=tu_usuario
API_ZONAS_PASSWORD=tu_contraseña
```

Guardar con Ctrl+S y cerrar.

### Paso 8: Inicializar Base de Datos

```powershell
# Ejecutar aplicación Python para crear la BD
python app.py
```

Cuando ves esto, significa que está funcionando:
```
WARNING in app.run_with_reloader: This is a development server.
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
 * Restarting with reloader
```

**¡IMPORTANTE!** No cierres esta ventana aún. Abre otra terminal.

### Paso 9: Crear Cuenta Admin

En una **nueva** ventana PowerShell:

```powershell
# Navegar al proyecto
cd C:\Ruta\a\tu\proyecto\ecommerce

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Abrir Python
python

# Ejecutar estos comandos en Python:
# (Copia y pega línea por línea)
```

```python
from app import app, db
from models.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    user = User(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('Admin123!'),
        is_admin=True,
        is_active=True
    )
    db.session.add(user)
    db.session.commit()
    print("✓ Usuario admin creado exitosamente")
    print("Usuario: admin")
    print("Contraseña: Admin123!")

exit()
```

### Paso 10: Acceder a la Aplicación

1. Ten ejecutándose `python app.py` en una terminal
2. Abre navegador web
3. Dirígete a: `http://localhost:5000`
4. Deberías ver la página principal de la tienda
5. Haz clic en Login y usa:
   - USERNAME: `admin`
   - PASSWORD: `Admin123!`

---

## Instalación en Linux/Mac

### Paso 1: Descargar el Proyecto

```bash
# Ir a la carpeta deseada
cd ~/Desktop

# Clonar repositorio
git clone https://github.com/DeadAVA/ecommerce.git

# Entrar al directorio
cd ecommerce

# Ver contenido
ls -la
```

### Paso 2: Crear Entorno Virtual

```bash
# Python 3 (recomendado)
python3 -m venv venv

# O si tienes Python 3.10+ específicamente
python3.10 -m venv venv
```

### Paso 3: Activar Entorno Virtual

```bash
# Activar
source venv/bin/activate

# Debería mostrar:
# (venv) usuario@computadora:~/Desktop/ecommerce$
```

### Paso 4: Actualizar pip

```bash
# Actualizar pip
pip install --upgrade pip

# Verificar
pip --version
```

### Paso 5: Instalar Dependencias

```bash
# Instalar todos los requirements
pip install -r requirements.txt

# Puede tomar 2-5 minutos
```

### Paso 6: Crear Archivo .env

```bash
# Crear archivo
touch .env

# Editar
nano .env
```

Pega este contenido (adaptar valores):

```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_SECRET_KEY=mi_clave_secreta_super_segura_cambiar_123456
DATABASE_URL=sqlite:///ecommerce.db
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=AZx_x1xX1x1Xx1x
PAYPAL_SECRET=xxx
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app_google
JWT_SECRET_KEY=tu_jwt_key_cambiar
API_ZONAS_USER=tu_usuario
API_ZONAS_PASSWORD=tu_contraseña
```

Guardar con `Ctrl+O`, Enter, `Ctrl+X`.

### Paso 7: Inicializar Base de Datos

```bash
# Ejecutar aplicación
python app.py

# Debería mostrar:
# WARNING in app.run_with_reloader: This is a development server.
#  * Running on http://127.0.0.1:5000
#  * Press CTRL+C to quit

# NO CIERRES ESTA VENTANA
```

### Paso 8: Crear Cuenta Admin

En otra terminal:

```bash
# Navegar al proyecto
cd ~/Desktop/ecommerce

# Activar entorno
source venv/bin/activate

# Abrir Python
python3

# Ejecutar:
```

```python
from app import app, db
from models.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    user = User(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('Admin123!'),
        is_admin=True,
        is_active=True
    )
    db.session.add(user)
    db.session.commit()
    print("✓ Usuario admin creado exitosamente")

exit()
```

### Paso 9: Acceder a la Aplicación

```bash
# En el navegador:
http://localhost:5000
```

---

## Configuración de Variables de Entorno

### Credenciales PayPal

1. Ir a https://developer.paypal.com
2. Crear cuenta o iniciar sesión
3. Ir a "Dashboard"
4. Buscar "Apps & Credentials"
5. Copiar "Client ID" y "Secret"
6. Agregar a .env:

```env
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=paste_client_id_aqui
PAYPAL_SECRET=paste_secret_aqui
```

### Configurar Gmail para Emails

1. Ir a https://myaccount.google.com
2. Seguridad -> Contraseñas de aplicación
3. Generar contraseña para "Mail"
4. Copiar contraseña generada
5. Agregar a .env:

```env
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=contraseña_de_app_generada
```

### Credenciales API Zonas

1. Registrarse en https://www.zonasapi.com
2. Obtener credenciales
3. Agregar a .env:

```env
API_ZONAS_USER=tu_usuario
API_ZONAS_PASSWORD=tu_contraseña
API_ZONAS_MODE=sandbox
```

---

## Configuración de Base de Datos

### SQLite (Desarrollo)

```env
DATABASE_URL=sqlite:///ecommerce.db
```

Ventajas:
- No requiere servidor
- Perfecto para desarrollo
- Archivo único

Desventajas:
- No para producción
- Limitado concurrencia

### MySQL (Producción)

#### Paso 1: Instalar MySQL

**Windows:**
- Descargar desde https://dev.mysql.com/downloads/mysql/
- Ejecutar instalador

**Linux:**
```bash
sudo apt-get install mysql-server mysql-client
```

**Mac:**
```bash
brew install mysql
brew services start mysql
```

#### Paso 2: Crear Base de Datos

```bash
mysql -u root -p

# Luego:
```

```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'password_segura_123';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### Paso 3: Configurar en .env

```env
DATABASE_URL=mysql+pymysql://ecommerce_user:password_segura_123@localhost:3306/ecommerce_db
```

#### Paso 4: Instalar driver

```bash
pip install PyMySQL
```

---

## Verificación de Instalación

### Checklist Completo

```python
# Crear archivo test_installation.py

import sys
print(f"✓ Python version: {sys.version}")

try:
    import flask
    print(f"✓ Flask: {flask.__version__}")
except: print("✗ Flask no instalado")

try:
    import flask_sqlalchemy
    print(f"✓ Flask-SQLAlchemy")
except: print("✗ Flask-SQLAlchemy no instalado")

try:
    import flask_login
    print(f"✓ Flask-Login")
except: print("✗ Flask-Login no instalado")

try:
    import jwt
    print(f"✓ PyJWT")
except: print("✗ PyJWT no instalado")

try:
    import paypalrestsdk
    print(f"✓ PayPal SDK")
except: print("✗ PayPal SDK no instalado")

try:
    import dotenv
    print(f"✓ python-dotenv")
except: print("✗ python-dotenv no instalado")

try:
    from app import app
    print("✓ Aplicación Flask carga correctamente")
except Exception as e:
    print(f"✗ Error al cargar app: {e}")

print("\n✓ Instalación completada!")
```

Ejecutar:
```bash
python test_installation.py
```

---

## Primeros Pasos

### 1. Crear Algunos Productos de Prueba

```bash
python

# En Python:
```

```python
from app import app, db
from models.models import Category, Product

with app.app_context():
    # Crear categoría
    cat = Category(name='Electrónica', description='Productos electrónicos')
    db.session.add(cat)
    db.session.flush()  # Necesario para obtener el ID
    
    # Crear producto
    prod = Product(
        name='Laptop Ejemplo',
        description='Laptop de prueba',
        price=999.99,
        category_id=cat.id,
        stock=10,
        sku='LAPTOP-001'
    )
    db.session.add(prod)
    db.session.commit()
    
    print("✓ Producto creado!")

exit()
```

### 2. Habilitar Panel Admin

Cuando inices sesión como admin:
- Haz clic en "Admin Panel"
- O ve a `/admin/dashboard`

### 3. Explorar la Aplicación

- **Página de inicio:** `/`
- **Catálogo:** `/shop`
- **Carrito:** `/cart`
- **Checkout:** `/checkout`
- **Perfil:** `/user/profile`
- **Admin:** `/admin/dashboard`

---

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask'"

```bash
# Solución 1: Verificar entorno activado
# Debería mostrar (venv) al inicio del prompt

# Solución 2: Reinstalar dependencias
pip install -r requirements.txt

# Solución 3: Usar pip de ese entorno
# Windows
.\venv\Scripts\pip list

# Linux/Mac
venv/bin/pip list
```

### Error: "Port 5000 already in use"

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <numero> /F

# Linux/Mac
lsof -i :5000
kill -9 <numero>

# O usar otro puerto
python app.py --port 5001
```

### Error: ".env variables not loading"

```bash
# 1. Verificar archivo existe
ls -la .env  # Linux/Mac
dir .env     # Windows

# 2. Verificar contenido
cat .env     # Linux/Mac
type .env    # Windows

# 3. Reinstalar python-dotenv
pip install --force-reinstall python-dotenv

# 4. Reiniciar servidor
# Ctrl+C en la terminal de Flask
# Ejecutar: python app.py
```

### Error: "database is locked"

```bash
# Si usas SQLite:
# Cerrar todas las instancias de la app
# Ctrl+C en terminales abiertas

# Eliminar archivo .db-journal si existe
rm ecommerce.db-journal

# Reiniciar
python app.py
```

---

## Comandos Útiles de Referencia Rápida

```bash
# Activar entorno
# Windows
.\venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate

# Instalar paquete nuevo
pip install nombre_paquete

# Desinstalar paquete
pip uninstall nombre_paquete

# Ver paquetes instalados
pip list

# Actualizar paquete
pip install --upgrade nombre_paquete

# Generar requirements.txt (después de instalar algo nuevo)
pip freeze > requirements.txt

# Ejecutar aplicación
python app.py

# Ejecutar con puerto diferente
python app.py --port 5001

# Salir del entorno virtual
deactivate

# Ver logs de errores
# Ctrl+Shift+` en VS Code para abrir terminal integrada
# Los errores aparecen en la salida de Flask
```

---

¡Listo! Ahora tu ecommerce está instalado y listo para usar. 🎉

Si encuentras problemas, revisa la sección de [Troubleshooting](#solución-de-problemas).

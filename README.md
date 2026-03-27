# 🛒 Ecommerce Platform - Plataforma de Comercio Electrónico Profesional

[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/DeadAVA/ecommerce)
[![License](https://img.shields.io/badge/License-Private-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-darkgreen.svg)](https://flask.palletsprojects.com/)

Un **sistema de comercio electrónico completo y profesional** desarrollado con Flask, diseñado para manejar catálogos de productos, gestión de pedidos, procesamiento de pagos y un panel administrativo avanzado.

> **⚠️ Repositorio Privado** - Este código es mantenido solo por el propietario del proyecto.

---

## 📋 Tabla de Contenidos

- [Características Principales](#características-principales)
- [Stack Tecnológico](#stack-tecnológico)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación Detallada](#instalación-detallada)
- [Configuración](#configuración)
- [Uso de la Aplicación](#uso-de-la-aplicación)
- [Panel Administrativo](#panel-administrativo)
- [API y Endpoints](#api-y-endpoints)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Integraciones Externas](#integraciones-externas)
- [Guía de Despliegue](#guía-de-despliegue)
- [Troubleshooting](#troubleshooting)
- [Contribución](#contribución)
- [Licencia](#licencia)

---

## ✨ Características Principales

### 🔐 Autenticación y Seguridad
- **Sistema de registro completo** con validación de email
- **Autenticación JWT** para APIs
- **Recuperación de contraseña** vía email
- **Roles y permisos** (Usuario, Admin)
- **Protección CSRF** en formularios
- **Encriptación bcrypt** de contraseñas
- **HTTPS/SSL** en producción

### 📦 Gestión de Productos
- **Catálogo dinámico** con múltiples categorías
- **Búsqueda y filtrado avanzado** con paginación
- **Imágenes de productos** con almacenamiento optimizado
- **Inventario en tiempo real**
- **Precios dinámicos** y promociones
- **Cross-selling** y productos relacionados
- **Reseñas y calificaciones** de clientes

### 🛍️ Carrito y Checkout
- **Persistencia de carrito** en sesión y base de datos
- **Cálculo automático** de impuestos y envío
- **Múltiples métodos de pago** (PayPal, tarjeta)
- **Direcciones de envío** múltiples
- **Cupones y códigos de descuento**
- **Carrito guardado** para compras futuras
- **Resumen visual** del pedido

### 📊 Gestión de Pedidos
- **Creación automática de órdenes**
- **Estados de pedido** en tiempo real (Pendiente, Confirmado, Enviado, Entregado)
- **Seguimiento de envíos** con rastreo
- **Historial completo** de compras por usuario
- **Devoluciones y cambios** gestionados
- **Facturas automáticas** en PDF
- **Notificaciones por email** en cada estado

### 🗺️ Sistema de Zonas y Envíos
- **Integración API Zonas** para cálculo de costos
- **Validación COPOMEX** de códigos postales
- **Múltiples métodos de envío**
- **Seguimiento en tiempo real**
- **Costos dinámicos** según zona
- **Alertas de disponibilidad** de envío

### 📱 Panel Administrativo Completo
- **Dashboard ejecutivo** con métricas clave
- **Gestión de productos** (CRUD completo)
- **Gestión de categorías**
- **Gestión de usuarios** y permisos
- **Análisis de ventas** con gráficos
- **Reporte de compras**
- **Gestión de comprobantes**
- **Log de actividades** del sistema
- **Gestión de envíos**
- **Direcciones de clientes**

### 💳 Integraciones de Pago
- **Integración PayPal** (Sandbox y Producción)
- **Procesamiento de tarjetas** seguro
- **Confirmación de pago** automática
- **Reembolsos** gestionados
- **Notificaciones** de transacciones

### 👥 Gestión de Usuarios
- **Perfil de usuario** completo
- **Múltiples direcciones** de envío
- **Historial de compras**
- **Wishlist** de productos favoritos
- **Preferencias personales**
- **Notificaciones** por email

### 📈 Reportes y Estadísticas
- **Ventas por período**
- **Productos más vendidos**
- **Clientes más activos**
- **Ingresos y proyecciones**
- **Tasas de conversión**
- **Análisis de abandono de carrito**

---

## 🛠️ Stack Tecnológico

### Backend
| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Framework | **Flask** | 2.0+ |
| ORM | **SQLAlchemy** | 1.4+ |
| Autenticación | **Flask-Login**, **PyJWT** | Latest |
| Base de Datos | **SQLite** (dev) / **MySQL** (prod) | Latest |
| Validación | **WTForms** | Latest |
| Email | **Flask-Mail** | Latest |
| CORS | **Flask-CORS** | Latest |
| Criptografía | **Werkzeug**, **bcrypt** | Latest |

### Frontend
| Componente | Tecnología |
|-----------|-----------|
| HTML | HTML5 semantántico |
| CSS | Bootstrap 5, SCSS personalizado |
| JavaScript | Vanilla JS + jQuery |
| Formularios | Bootstrap Forms |
| Gráficos | Chart.js |
| Tablas | DataTables |
| Templates | Jinja2 |

### DevOps
| Componente | Tecnología |
|-----------|-----------|
| Control de Versiones | **Git** |
| Servidor | **Gunicorn** (WSGI) |
| Reverse Proxy | **Nginx** |
| SSL/TLS | **Let's Encrypt** |
| Contenerización | **Docker** (opcional) |
| Base de Datos | **MySQL** 8.0+ |

---

## 📋 Requisitos del Sistema

### Mínimos
- **Python** >= 3.8
- **pip** o **conda**
- **Git** >= 2.0
- **RAM** >= 2GB
- **Espacio en disco** >= 1GB

### Recomendados (Producción)
- **Python** 3.10+
- **MySQL** 8.0+
- **RAM** >= 4GB
- **SSD** >= 20GB
- **Nginx** o similar
- **SSL Certificate** (Let's Encrypt)

### Dependencias de Sistema

**Windows:**
```bash
# Instalar desde Microsoft Store o Chocolatey
choco install python git mysql
```

**macOS:**
```bash
# Usando Homebrew
brew install python@3.10 git mysql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3.10 python3.10-venv git mysql-server
```

---

## 🚀 Instalación Detallada

### Paso 1: Clonar el Repositorio

```bash
# Clonar desde GitHub
git clone https://github.com/DeadAVA/ecommerce.git

# Entrar al directorio
cd ecommerce

# Ver contenido
ls -la
```

**Salida esperada:**
```
app.py
config.py
requirements.txt
templates/
static/
models/
admin/
api_zonas/
utils/
...
```

### Paso 2: Crear Entorno Virtual

#### Windows (PowerShell)
```powershell
# Crear entorno virtual
python -m venv venv

# Activar (PowerShell)
.\venv\Scripts\Activate.ps1

# Verificar que esté activado (debería mostrar "(venv)" al inicio)
echo "Environment: $env:VIRTUAL_ENV"
```

#### Linux/macOS
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar
source venv/bin/activate

# Verificar
echo $VIRTUAL_ENV
```

### Paso 3: Instalar Dependencias

```bash
# Actualizar pip, setuptools y wheel
pip install --upgrade pip setuptools wheel

# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

**Dependencias principales:**
```
Flask==2.3.2
Flask-Login==0.6.2
Flask-SQLAlchemy==3.0.5
Flask-Mail==0.9.1
Flask-CORS==4.0.0
PyJWT==2.8.0
python-dotenv==1.0.0
requests==2.31.0
paypalrestsdk==1.13.1
WTForms==3.0.1
...
```

### Paso 4: Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```bash
# Crear archivo .env
touch .env  # Linux/Mac
# o
New-Item .env -ItemType File  # Windows
```

Completar con las siguientes variables:

```env
# ============================================
# CONFIGURACIÓN FLASK
# ============================================
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_SECRET_KEY=tu_clave_secreta_super_segura_cambiar_en_produccion_1234567890

# ============================================
# BASE DE DATOS
# ============================================
# Para SQLite (desarrollo)
DATABASE_URL=sqlite:///ecommerce.db

# Para MySQL (producción - descomenta)
# DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/ecommerce_db
# SQLALCHEMY_TRACK_MODIFICATIONS=False

# ============================================
# PAYPAL SANDBOX
# ============================================
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=tu_paypal_client_id_sandbox
PAYPAL_SECRET=tu_paypal_secret_sandbox

# Para producción, cambiar a:
# PAYPAL_MODE=live
# PAYPAL_CLIENT_ID=tu_paypal_client_id_produccion
# PAYPAL_SECRET=tu_paypal_secret_produccion

# ============================================
# CORREO ELECTRÓNICO
# ============================================
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app_google  # Contraseña de app específica para Gmail

# Para otros proveedores:
# MAIL_SERVER=smtp.outlook.com (Outlook)
# MAIL_SERVER=smtp.zoho.com (Zoho)
# MAIL_SERVER=mail.example.com (Servidor personalizado)

MAIL_DEFAULT_SENDER=noreply@ecommerce.com
SUPPORT_EMAIL=soporte@ecommerce.com

# ============================================
# AUTENTICACIÓN JWT
# ============================================
JWT_SECRET_KEY=tu_jwt_secret_key_super_segura_cambiar_1234567890
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# ============================================
# API ZONAS DE ENVÍO
# ============================================
API_ZONAS_USER=tu_usuario_api_zonas
API_ZONAS_PASSWORD=tu_contraseña_api_zonas
API_ZONAS_MODE=sandbox  # Cambiar a 'production' cuando esté listo

# ============================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================
WTF_CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=None
SESSION_COOKIE_SECURE=False  # Cambiar a True en HTTPS
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# ============================================
# OTRAS CONFIGURACIONES
# ============================================
ITEMS_PER_PAGE=12
MAX_CONTENT_LENGTH=16777216  # 16MB máximo para uploads
UPLOAD_FOLDER=uploads/
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,pdf

# Admin
ADMIN_PANEL_ENABLED=True
ADMIN_PASSWORD_RESET_REQUIRED=True

# Características
ENABLE_WISHLIST=True
ENABLE_REVIEWS=True
ENABLE_COUPONS=True
ENABLE_REFERRAL=False  # Para programas de referencia futuros
```

### Paso 5: Inicializar la Base de Datos

```bash
# Opción 1: Ejecutar app.py (crea DB automáticamente si no existe)
python app.py

# Opción 2: Crear y popular base de datos manualmente
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>>     print("Base de datos creada exitosamente")
>>> exit()
```

### Paso 6: Crear Usuario Administrador

```python
# En Python shell o crear archivo init_admin.py
python

from app import app, db
from models.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Verificar si ya existe admin
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        admin = User(
            username='admin',
            email='admin@ecommerce.com',
            password_hash=generate_password_hash('cambiar_contraseña_123'),
            is_admin=True,
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Usuario administrador creado: admin / cambiar_contraseña_123")
    else:
        print("✓ El usuario admin ya existe")

exit()
```

### Paso 7: Ejecutar la Aplicación

```bash
# Activar entorno virtual (si no está activado)
# Windows
.\venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate

# Ejecutar servidor Flask
python app.py

# Salida esperada:
# WARNING in app.run_with_reloader: This is a development server.
#  * Running on http://127.0.0.1:5000
#  * Press CTRL+C to quit
#  * Restarting with reloader
```

### Paso 8: Acceder a la Aplicación

Abrir navegador y acceder a:

```
http://localhost:5000
```

**URLs útiles:**
| Sección | URL | Descripción |
|---------|-----|-----------|
| Inicio | `/` | Página principal |
| Tienda | `/shop` | Catálogo de productos |
| Carrito | `/cart` | Ver carrito |
| Checkout | `/checkout` | Procesar compra |
| Perfil | `/user/profile` | Mi perfil |
| Mis Compras | `/user/orders` | Historial de órdenes |
| Admin Dashboard | `/admin/dashboard` | Panel administrativo |
| Login | `/login` | Iniciar sesión |
| Registro | `/register` | Crear cuenta |

---

## ⚙️ Configuración

### Archivo `config.py`

El archivo de configuración principal:

```python
import os
from datetime import timedelta

class Config:
    """Configuración base"""
    FLASK_APP = os.getenv('FLASK_APP', 'app.py')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-key-cambiar')
    SQLALCHEMY_ECHO = True
    
    # Base de Datos
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'sqlite:///ecommerce.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # True en producción
    SESSION_COOKIE_HTTPONLY = True
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-key-cambiar')
    JWT_ALGORITHM = 'HS256'
    
    # Paginación
    ITEMS_PER_PAGE = 12
    
    # Upload
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    SQLALCHEMY_ECHO = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

### Configuración de PayPal

En `paypal_client.py`:

```python
import paypalrestsdk
import os

# Configurar PayPal SDK
paypalrestsdk.configure({
    "mode": os.getenv('PAYPAL_MODE', 'sandbox'),
    "client_id": os.getenv('PAYPAL_CLIENT_ID'),
    "client_secret": os.getenv('PAYPAL_SECRET')
})

def create_payment(amount, description, return_url, cancel_url):
    """Crear pago en PayPal"""
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url
        },
        "transactions": [{
            "amount": {
                "total": str(amount),
                "currency": "MXN"
            },
            "description": description
        }]
    })
    
    if payment.create():
        return payment
    else:
        return None
```

---

## 📱 Uso de la Aplicación

### Como Cliente

#### 1. Registro e Inicio de Sesión

```
1. Ir a /register
2. Completar formulario:
   - Nombre de usuario
   - Email
   - Contraseña (mínimo 8 caracteres)
3. Hacer clic en "Registrarse"
4. Verificar email
5. Iniciar sesión con credenciales
```

#### 2. Explorar Productos

```
1. Ir a /shop
2. Buscar o filtrar por:
   - Categoría
   - Precio
   - Calificación
3. Hacer clic en producto para ver detalles
4. Ver reseñas y calificaciones
5. Ver productos relacionados
```

#### 3. Realizar Compra

```
1. Agregar producto al carrito (/cart)
2. Modificar cantidad o remover items
3. Ingresar código de cupón (opcional)
4. Ir a checkout (/checkout)
5. Seleccionar o crear dirección de envío
6. Elegir método de pago
7. Confirmar orden
8. Completar pago en PayPal
9. Ver confirmación
```

#### 4. Gestionar Orden

```
1. Ir a /user/orders
2. Ver lista de órdenes
3. Hacer clic en orden para detalles
4. Rastrear envío
5. Descargar factura
6. Solicitar cambio o devolución
```

### Como Administrador

#### 1. Acceder al Panel

```
1. Iniciar sesión como usuario admin
2. Ir a /admin/dashboard
3. Ver métricas principales:
   - Ventas del mes
   - Órdenes pendientes
   - Productos activos
   - Usuarios registrados
```

#### 2. Gestionar Productos

```
/admin/productos:
- Ver lista de productos
- Crear nuevo producto
- Editar detalles
- Actualizar precio
- Cambiar estado (activo/inactivo)
- Eliminar producto
- Ver imagen y descripción
- Gestionar categorías
```

#### 3. Gestionar Órdenes

```
/admin/compras:
- Ver todas las órdenes
- Cambiar estado
- Ver detalles del cliente
- Ver artículos de la orden
- Generar factura
- Procesar devoluciones
- Añadir notas internas
```

#### 4. Gestionar Usuarios

```
/admin/usuarios:
- Ver lista de usuarios
- Ver detalles (perfil, órdenes, etc)
- Cambiar estatus (activo/suspendido)
- Editar información
- Log de actividad del usuario
- Gestionar permisos
```

#### 5. Gestionar Envíos

```
/admin/envios:
- Ver envíos pendientes
- Cambiar estado
- Generar etiqueta de envío
- Rastrear paquete
- Marcar como entregado
- Ver costos por zona
```

#### 6. Ver Reportes

```
/admin/dashboard/reportes:
- Gráficos de ventas por período
- Top 10 productos más vendidos
- Clientes más activos
- Ingresos vs proyección
- Tasa de conversión
- Análisis de abandono de carrito
- Exportar a PDF/Excel
```

---

## 🔌 API y Endpoints

### Autenticación

#### POST `/api/auth/register`
Registrar nuevo usuario
```json
{
    "username": "nuevo_usuario",
    "email": "user@example.com",
    "password": "Password123!"
}
```
**Respuesta:**
```json
{
    "status": "success",
    "message": "Usuario registrado correctamente",
    "user_id": 1
}
```

#### POST `/api/auth/login`
Iniciar sesión
```json
{
    "email": "user@example.com",
    "password": "Password123!"
}
```
**Respuesta:**
```json
{
    "status": "success",
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
        "id": 1,
        "username": "usuario",
        "email": "user@example.com"
    }
}
```

#### POST `/api/auth/logout`
Cerrar sesión
```bash
curl -X POST http://localhost:5000/api/auth/logout \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Productos

#### GET `/api/products`
Listar productos con paginación
```bash
curl "http://localhost:5000/api/products?page=1&limit=12&category=electronics&sort=price_asc"
```
**Parámetros:**
- `page` (int): Número de página
- `limit` (int): Items por página (default: 12)
- `category` (str): Filtrar por categoría
- `search` (str): Búsqueda de texto
- `sort` (str): price_asc, price_desc, newest, popular

**Respuesta:**
```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "name": "Producto Ejemplo",
            "price": 99.99,
            "category": "Electrónica",
            "stock": 50,
            "rating": 4.5,
            "image": "/static/images/product1.jpg"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 12,
        "total": 45,
        "pages": 4
    }
}
```

#### GET `/api/products/<product_id>`
Obtener detalles de un producto
```bash
curl http://localhost:5000/api/products/1
```

#### POST `/api/products` (Admin)
Crear nuevo producto
```json
{
    "name": "Nuevo Producto",
    "description": "Descripción del producto",
    "price": 99.99,
    "category_id": 1,
    "stock": 100,
    "sku": "PROD-001"
}
```

### Carrito

#### GET `/api/cart`
Obtener carrito actual
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/cart
```

#### POST `/api/cart/add`
Agregar producto al carrito
```json
{
    "product_id": 1,
    "quantity": 2
}
```

#### PUT `/api/cart/update/<item_id>`
Actualizar cantidad en carrito
```json
{
    "quantity": 5
}
```

#### DELETE `/api/cart/remove/<item_id>`
Remover item del carrito
```bash
curl -X DELETE http://localhost:5000/api/cart/remove/1
```

### Órdenes

#### GET `/api/orders`
Obtener órdenes del usuario autenticado
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/orders
```

#### GET `/api/orders/<order_id>`
Obtener detalles de una orden
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/orders/12345
```

#### POST `/api/orders`
Crear nueva orden
```json
{
    "address_id": 1,
    "shipping_method": "standard",
    "coupon_code": "DISCOUNT10"
}
```

#### GET `/api/orders/<order_id>/track`
Rastrear envío de una orden
```bash
curl http://localhost:5000/api/orders/12345/track
```
**Respuesta:**
```json
{
    "order_id": "12345",
    "status": "shipped",
    "ship_date": "2024-03-25",
    "estimated_delivery": "2024-03-28",
    "tracking_number": "1Z999AA10123456784",
    "carrier": "UPS",
    "events": [
        {
            "date": "2024-03-25T10:30:00",
            "status": "Picked up",
            "location": "Mexico City, MX"
        }
    ]
}
```

### Admin API

#### GET `/api/admin/dashboard/stats`
Obtener estadísticas del dashboard
```bash
curl -H "Authorization: Bearer ADMIN_TOKEN" \
  http://localhost:5000/api/admin/dashboard/stats
```

#### GET `/api/admin/sales/report`
Reporte de ventas
```bash
curl -H "Authorization: Bearer ADMIN_TOKEN" \
  "http://localhost:5000/api/admin/sales/report?start_date=2024-01-01&end_date=2024-03-31"
```

#### POST `/api/admin/orders/<order_id>/status`
Actualizar estado de orden
```json
{
    "status": "shipped",
    "tracking_number": "1Z999AA10123456784"
}
```

---

## 📁 Estructura del Proyecto

```
ecommerce/
│
├── 📄 app.py                          # Aplicación principal Flask
├── 📄 config.py                       # Configuración por ambiente
├── 📄 extensions.py                   # Inicialización de extensiones
├── 📄 wsgi.py                         # Entry point para servidor
├── 📄 requirements.txt                # Dependencias Python
├── 📄 .env                            # Variables de entorno (no versionar)
├── 📄 .gitignore                      # Archivos ignorados por Git
├── 📄 .gitattributes                  # Atributos Git (line endings, LFS)
│
├── 📁 admin/                          # Panel Administrativo
│   ├── 📄 __init__.py
│   ├── 📄 routes.py                   # Rutas del panel admin
│   └── 📄 log.py                      # Sistema de logging
│
├── 📁 api_zonas/                      # Integración API Zonas
│   ├── 📄 __init__.py
│   ├── 📄 routes.py                   # Endpoints de zonas
│   ├── 📄 zones_api.py                # Lógica de integración
│   └── 📁 data/
│       └── 📄 CPdescarga.xml          # Base COPOMEX (63MB)
│
├── 📁 models/                         # Definición de Modelos
│   ├── 📄 __init__.py
│   ├── 📄 models.py                   # ORM SQLAlchemy
│   │   ├── User                       # Usuarios
│   │   ├── Product                    # Productos
│   │   ├── Category                   # Categorías
│   │   ├── Order                      # Órdenes
│   │   ├── OrderItem                  # Items de orden
│   │   ├── Cart                       # Carrito
│   │   ├── Address                    # Direcciones
│   │   ├── Payment                    # Pagos
│   │   ├── Shipment                   # Envíos
│   │   ├── Review                     # Reseñas
│   │   └── ActivityLog                # Log de actividades
│   ├── 📄 forms.py                    # Formularios WTForms
│   ├── 📄 estados.py                  # Estados y enumerables
│   └── 📄 message.py                  # Modelos de mensajes
│
├── 📁 utils/                          # Utilidades
│   ├── 📄 __init__.py
│   ├── 📄 auth.py                     # Funciones de autenticación
│   ├── 📄 decorators.py               # Decoradores personalizados
│   └── 📄 email_sender.py             # Envío de emails
│
├── 📁 static/                         # Archivos Estáticos
│   ├── 📁 css/
│   │   ├── 📄 style.css               # Estilos personalizados
│   │   ├── 📄 sb-admin-2.css          # Template admin
│   │   ├── 📄 professional.css        # Estilos profesionales
│   │   └── 📄 responsive.css          # Diseño responsive
│   │
│   ├── 📁 js/
│   │   ├── 📄 app.js                  # JavaScript principal
│   │   ├── 📄 custom.js               # Personalizaciones
│   │   ├── 📄 admin-custom.js         # Scripts del admin
│   │   ├── 📄 zones-api.js            # Integración zonas
│   │   ├── 📄 cart.js                 # Lógica del carrito
│   │   ├── 📄 checkout.js             # Validación checkout
│   │   └── 📁 vendor/                 # Librerías externas
│   │       ├── bootstrap/
│   │       ├── jquery/
│   │       ├── datatables/
│   │       ├── chart.js/
│   │       └── fontawesome-free/
│   │
│   ├── 📁 images/                     # Imágenes del sitio
│   │   ├── 📄 logo.png
│   │   ├── 📄 banner.jpg
│   │   └── ...
│   │
│   ├── 📁 img/                        # Iconos y gráficos
│   │   └── ...
│   │
│   └── 📁 comprobantes/               # Comprobantes ups (uploads)
│
├── 📁 templates/                      # Plantillas HTML Jinja2
│   ├── 📄 base.html                   # Plantilla base
│   ├── 📄 index.html                  # Página inicio
│   ├── 📄 shop.html                   # Catálogo
│   ├── 📄 product_detail.html         # Detalles de producto
│   ├── 📄 cart.html                   # Carrito
│   ├── 📄 checkout.html               # Checkout
│   ├── 📄 login.html                  # Login
│   ├── 📄 register.html               # Registro
│   ├── 📄 about.html                  # Acerca de
│   ├── 📄 contact.html                # Contacto
│   ├── 📄 privacidad.html             # Privacidad
│   ├── 📄 terminos.html               # Términos de servicio
│   ├── 📄 soporte.html                # Soporte
│   ├── 📄 thankyou.html               # Confirmación de pago
│   │
│   ├── 📁 admin/                      # Templates admin
│   │   ├── 📄 base.html               # Base admin
│   │   ├── 📄 dashboard.html          # Dashboard principal
│   │   ├── 📄 usuarios.html           # Gestión usuarios
│   │   ├── 📄 productos.html          # Gestión productos
│   │   ├── 📄 categorias.html         # Gestión categorías
│   │   ├── 📄 compras.html            # Historial compras
│   │   ├── 📄 detalles_compra.html    # Detalles compra
│   │   ├── 📄 envios.html             # Gestión envíos
│   │   ├── 📄 comprobantes.html       # Gestión comprobantes
│   │   ├── 📄 direcciones.html        # Direcciones
│   │   ├── 📄 activity_log.html       # Log de actividades
│   │   └── 📁 vistas/                 # Componentes parciales
│   │
│   ├── 📁 user/                       # Templates usuario
│   │   ├── 📄 profile.html            # Perfil usuario
│   │   ├── 📄 orders.html             # Mis órdenes
│   │   ├── 📄 purchases.html          # Compras
│   │   └── 📄 rastreo.html            # Rastreo
│   │
│   └── 📁 vistas/                     # Componentes reutilizables
│       ├── 📄 navbar.html
│       ├── 📄 footer.html
│       ├── 📄 pagination.html
│       └── ...
│
├── 📁 uploads/                        # Archivos cargados (dinámico)
│   ├── 📁 comprobantes/               # Comprobantes de pago
│   └── 📁 products/                   # Imágenes de productos
│
├── 📁 venv/                           # Entorno virtual (no versionar)
│
├── 🔒 ecommerce.db                    # Base de datos SQLite
│
├── 📚 Documentación
│   ├── 📄 README.md                   # Este archivo
│   ├── 📄 README_GITHUB.md            # Referencia GitHub
│   ├── 📄 QUICK_START.md              # Guía rápida
│   ├── 📄 PROJECT_STRUCTURE.md        # Estructura detallada
│   ├── 📄 CONTRIBUTING.md             # Guía contribución
│   ├── 📄 GUIA_DESPLIEGUE.md          # Despliegue producción
│   ├── 📄 HTTPS_SETUP.md              # Configuración SSL
│   ├── 📄 JWT_AUTHENTICATION.md       # JWT explicado
│   ├── 📄 IMPLEMENTACION_API_ZONAS.md # API Zonas
│   ├── 📄 CAMBIOS_REALIZADOS.md       # Historial cambios
│   └── 📄 API_ZONAS_README.md         # Documentación API
│
└── 📋 Configuración
    └── 📄 .env.example                # Variables de entorno ejemplo
```

---

## 🔗 Integraciones Externas

### PayPal

**Flujo de pago:**
```
1. Usuario selecciona "Pagar con PayPal"
2. Redirección a PayPal Sandbox/Production
3. Usuario completa autenticación
4. Confirmación de monto y detalles
5. Regresa a la aplicación con approval_id
6. APP ejecuta payment.execute()
7. Pago confirmado
8. Orden marcada como pagada
9. Email de confirmación enviado
```

**Configuración:**
```python
# .env
PAYPAL_MODE=sandbox  # Cambiar a 'live' para producción
PAYPAL_CLIENT_ID=xxx
PAYPAL_SECRET=xxx
```

**Testing PayPal:**
- Email de prueba: sb-test@personal.example.com
- Contraseña: cualquier contraseña

### API Zonas

**Funcionalidades:**
- Cálculo de costos de envío por código postal
- Validación de códigos postales (COPOMEX)
- Estimación de tiempo de entrega
- Múltiples transportistas

**Endpoints utilizados:**
```
GET /cp/:cp                      # Información de CP
POST /cotizacion                 # Cotización de envío
GET /rastreo/:tracking           # Rastreo de envío
```

**Configuración:**
```python
# .env
API_ZONAS_USER=tu_usuario
API_ZONAS_PASSWORD=tu_contraseña
API_ZONAS_MODE=sandbox
```

### Servicio de Email

**Proveedores soportados:**
- Gmail (SMTP)
- Outlook
- Zoho Mail
- Servidor personalizado

**Configuración Gmail:**
```python
# .env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app  # Usar contraseña de app específica
```

**Emails enviados automáticamente:**
- Confirmación de registro
- Reset de contraseña
- Confirmación de orden
- Notificación de envío
- Entrega completada
- Notificaciones administrativas

---

## 🚀 Guía de Despliegue

### Opción 1: Despliegue Manual (VPS/Servidor)

#### 1. Preparar Servidor

```bash
# Ubuntu 20.04 LTS
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.10 python3.10-venv python3-pip
sudo apt install -y nginx mysql-server git
sudo apt install -y certbot python3-certbot-nginx
```

#### 2. Configurar MySQL

```bash
# Crear base de datos
sudo mysql -u root

mysql> CREATE DATABASE ecommerce_prod;
mysql> CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'strong_password_123';
mysql> GRANT ALL PRIVILEGES ON ecommerce_prod.* TO 'ecommerce_user'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> EXIT;
```

#### 3. Clonar y configurar aplicación

```bash
# Crear directorio
mkdir -p /var/www/ecommerce
cd /var/www/ecommerce

# Clonar repo
git clone https://github.com/DeadAVA/ecommerce.git .

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install gunicorn

# Crear .env
cp .env.example .env
# Editar .env con configuraciones de producción
nano .env
```

#### 4. Configurar Gunicorn

Crear `/etc/systemd/system/ecommerce.service`:

```ini
[Unit]
Description=Ecommerce Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/ecommerce
ExecStart=/var/www/ecommerce/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:8000 \
    wsgi:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 5. Configurar Nginx

Crear `/etc/nginx/sites-available/ecommerce`:

```nginx
server {
    listen 80;
    server_name ecommerce.com www.ecommerce.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/ecommerce/static/;
        expires 30d;
    }

    location /uploads/ {
        alias /var/www/ecommerce/uploads/;
    }
}
```

#### 6. Habilitar HTTPS (Let's Encrypt)

```bash
# Validar y obtener certificado
sudo certbot --nginx -d ecommerce.com -d www.ecommerce.com

# Renovación automática
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

#### 7. Iniciar servicios

```bash
# Activar y iniciar Gunicorn
sudo systemctl enable ecommerce
sudo systemctl start ecommerce

# Activar y iniciar Nginx
sudo systemctl enable nginx
sudo systemctl restart nginx

# Verificar status
sudo systemctl status ecommerce
sudo systemctl status nginx
```

### Opción 2: Docker

Crear `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

Crear `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: ecommerce_db
      MYSQL_ROOT_PASSWORD: root_password
    volumes:
      - db_data:/var/lib/mysql

  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      DATABASE_URL: mysql+pymysql://root:root_password@db:3306/ecommerce_db
    volumes:
      - .:/app

volumes:
  db_data:
```

Ejecutar:
```bash
docker-compose up -d
```

### Opción 3: PaaS (Heroku/Render)

```bash
# Crear Procfile
echo "web: gunicorn wsgi:app" > Procfile

# Crear runtime.txt
echo "python-3.10.13" > runtime.txt

# Desplegar
git push heroku main
```

---

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. Error: ModuleNotFoundError

```bash
# Solución:
# 1. Verificar entorno virtual activado
echo $VIRTUAL_ENV

# 2. Reinstalar dependencias
pip install --no-cache-dir -r requirements.txt

# 3. Verificar Python version
python --version  # Debe ser 3.8+
```

#### 2. Error: "Port 5000 is already in use"

```bash
# Windows - Encontrar y matar proceso
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>

# O usar otro puerto
python app.py --port 5001
```

#### 3. Error: Base de datos corrupta

```bash
# 1. Hacer backup
cp ecommerce.db ecommerce.db.backup

# 2. Eliminar DB actual
rm ecommerce.db

# 3. Recrear
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
```

#### 4. Error: Variables de entorno no cargadas

```bash
# Verificar archivo .env existe
ls -la .env

# Verificar contenido
cat .env

# Reinstalar python-dotenv
pip install --force-reinstall python-dotenv

# Reiniciar servidor
```

####5. Error: Email no se envía

```bash
# 1. Verificar credenciales en .env
# Para Gmail: usar contraseña de app específica
# https://myaccount.google.com/apppasswords

# 2. Testear conexión SMTP
python
>>> import smtplib
>>> server = smtplib.SMTP('smtp.gmail.com', 587)
>>> server.starttls()
>>> server.login('tu_email@gmail.com', 'tu_contraseña_app')
>>> print("✓ SMTP conectado correctamente")
```

#### 6. Error: PayPal transacciones fallando

```bash
# 1. Verificar modo
# PAYPAL_MODE debe ser 'sandbox' o 'live'

# 2. Verificar credenciales
# CLIENT_ID y SECRET deben coincidir con el modo

# 3. Testear en Sandbox primero
# Email: sb-test@personal.example.com

# 4. Ver logs
tail -f app.log
```

#### 7. Error: API Zonas no calcula costos

```python
# Verificar credenciales
print(os.getenv('API_ZONAS_USER'))
print(os.getenv('API_ZONAS_PASSWORD'))

# Testear llamada API
import requests
response = requests.get(
    'https://api.zonas.com/cp/28000',
    auth=(user, password)
)
print(response.json())
```

#### 8. Error: 500 Internal Server Error

```bash
# Ver logs detallados
# En desarrollo (FLASK_DEBUG=1):
# - Errores mostrados en navegador

# En producción:
# Ver logs de Gunicorn
sudo tail -f /var/log/syslog | grep ecommerce

# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log
```

---

## 🤝 Contribución

**Este es un repositorio privado del propietario.** Solo se aceptan contribuciones internas.

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para:
- Estándares de código
- Flujo de Git
- Testing
- Documentación

---

## 📄 Licencia

**Licencia Privada** - Este software es propiedad privada. No se permite reproducción, distribución o uso sin permiso explícito del propietario.

---

## 📞 Soporte

Para reportar bugs, preguntas o solicitudes:
- Email: soporte@ecommerce.com
- GitHub Issues: https://github.com/DeadAVA/ecommerce/issues

---

## 🎯 Hoja de Ruta (Roadmap)

### v1.0 (Actual)
- ✅ Catálogo de productos
- ✅ Carrito y checkout
- ✅ Autenticación de usuarios
- ✅ Integración PayPal
- ✅ Panel administrativo

### v1.1 (Próximo)
- 🔲 Sistema de cupones avanzado
- 🔲 Programa de referencia
- 🔲 Reviews y calificaciones mejoradas
- 🔲 Wishlist compartible
- 🔲 APP móvil

### v1.2 (Futuro)
- 🔲 Suscripciones y membresías
- 🔲 Marketplace multi-vendedor
- 🔲 Inteligencia artificial (recomendaciones)
- 🔲 Sistema de puntos/rewards
- 🔲 Integración con más métodos de pago

---

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| Líneas de código | ~15,000+ |
| Modelos | 12 |
| Rutas/Endpoints | 50+ |
| Plantillas HTML | 25+ |
| Archivos estáticos | 100+ |
| Dependencias | 25+ |
| Base de datos | SQLite/MySQL |
| Última actualización | 27 de marzo de 2026 |

---

**© 2024-2026 DeadAVA | Ecommerce Platform v1.0**  
**Repositorio Privado - Acceso Restringido**

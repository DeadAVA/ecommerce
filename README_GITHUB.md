# Ecommerce Platform

Un proyecto completo de plataforma de comercio electrónico desarrollado con **Flask** como backend, con integraciones de pagos, gestión de usuarios, órdenes y un panel administrativo robusto.

## Características Principales

✅ **Autenticación y Autorización**
- Sistema de registro e inicio de sesión
- Recuperación de contraseña
- Autenticación JWT

✅ **Catálogo de Productos**
- Gestión de productos y categorías
- Sistema de carritos de compra
- Búsqueda y filtrado avanzado

✅ **Gestión de Pedidos**
- Creación y seguimiento de órdenes
- Estados de envío en tiempo real
- Historial completo de compras

✅ **Panel Administrativo**
- Dashboard con métricas y estadísticas
- Gestión de usuarios y productos
- Registro de actividades (Activity Log)
- Gestión de comprobantes y envíos

✅ **Integraciones Externas**
- PayPal para procesamiento de pagos
- API Zonas para cálculo de costos de envío
- COPOMEX para validación de códigos postales

✅ **Seguridad**
- HTTPS/SSL
- Protección CSRF
- Validación de datos
- Encriptación de contraseñas

## Stack Tecnológico

- **Backend**: Flask
- **Base de Datos**: SQLite / MySQL
- **Autenticación**: Flask-Login, PyJWT
- **Pagos**: PayPal SDK
- **Frontend**: HTML5, CSS3, JavaScript
- **Admin Template**: SB Admin 2

## Requisitos Previos

- Python 3.8+
- pip o conda
- Git

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/DeadAVA/ecommerce.git
cd ecommerce
```

### 2. Crear y activar el entorno virtual

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Flask
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta_aqui

# Base de Datos
DATABASE_URL=sqlite:///ecommerce.db

# PayPal
PAYPAL_CLIENT_ID=tu_client_id
PAYPAL_SECRET=tu_secret_key

# Mail (opcional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app

# JWT
JWT_SECRET_KEY=tu_jwt_secret_key
```

### 5. Inicializar la base de datos

```bash
python app.py
# O si tienes CLI configurado:
flask db upgrade
```

### 6. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## Estructura del Proyecto

```
ecommerce/
├── admin/                 # Panel administrativo
│   ├── routes.py
│   ├── log.py
│   └── __init__.py
├── api_zonas/            # API de zonas de envío
│   ├── routes.py
│   ├── zones_api.py
│   └── data/
├── models/               # Modelos de base de datos
│   ├── models.py
│   ├── forms.py
│   ├── estados.py
│   └── message.py
├── static/               # Archivos estáticos
│   ├── css/
│   ├── js/
│   ├── images/
│   └── vendor/
├── templates/            # Plantillas HTML
│   ├── admin/
│   ├── user/
│   └── base.html
├── utils/                # Utilidades
│   ├── auth.py
│   ├── decorators.py
│   └── __init__.py
├── app.py               # Aplicación principal
├── config.py            # Configuración
├── extensions.py        # Extensiones de Flask
├── requirements.txt     # Dependencias
└── README.md
```

## Uso del Panel Administrativo

1. Acceder a `/admin/dashboard`
2. Las rutas administrativas están protegidas - requieren autenticación
3. Funcionalidades:
   - Visualizar métricas de ventas
   - Gestionar productos y categorías
   - Administrar usuarios
   - Ver registro de actividades
   - Procesar envíos y devoluciones

## API Zonas

La integración con API Zonas permite:
- Cálculo automático de costos de envío
- Validación de códigos postales
- Seguimiento de envíos

Configurar credenciales en `config.py`:

```python
API_ZONAS_USER = "tu_usuario"
API_ZONAS_PASSWORD = "tu_contraseña"
```

## Seguridad HTTPS

Para producción, generar certificados SSL:

```bash
python generate_certs.py
```

Ver documentación completa en `HTTPS_SETUP.md`

## Autenticación JWT

Los endpoints API utilizan JWT para autenticación. Incluir en headers:

```
Authorization: Bearer <tu_token_jwt>
```

Más detalles en `JWT_AUTHENTICATION.md`

## Troubleshooting

### Error de variables de entorno
```bash
# Asegurar que .env existe y tiene las variables necesarias
# Reiniciar el servidor después de cambios en .env
```

### Base de datos corrupta
```bash
# Respaldar base de datos actual
cp ecommerce.db ecommerce.db.backup

# Recrear base de datos
rm ecommerce.db
python app.py
```

### Problemas de CORS
Verificar la configuración en `config.py` y ajustar orígenes permitidos.

## Archivos de Documentación

- **GUIA_DESPLIEGUE.md** - Guía completa de despliegue en producción
- **HTTPS_SETUP.md** - Configuración de certificados SSL
- **JWT_AUTHENTICATION.md** - Documentación de JWT
- **IMPLEMENTACION_API_ZONAS.md** - Detalles de API Zonas
- **CAMBIOS_REALIZADOS.md** - Historial de cambios y mejoras

## Contribuir

1. Crear una rama para tu feature: `git checkout -b feature/mifeature`
2. Hacer commit: `git commit -am 'Agregar mifeature'`
3. Hacer push: `git push origin feature/mifeature`
4. Abrir Pull Request

## Licencia

Este proyecto es privado. Solo visible para el propietario.

## Soporte

Para reportar bugs o solicitar mejoras, contactar al administrador del proyecto.

---

**Última actualización**: 27 de marzo de 2026  
**Estado**: Producción Ready

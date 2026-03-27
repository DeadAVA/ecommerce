# Estructura del Proyecto

## Descripción de Carpetas y Archivos

### `/admin`
Panel administrativo privado para gestión de la plataforma.

```
admin/
├── __init__.py
├── routes.py          # Rutas del panel admin
└── log.py            # Sistema de log de actividades
```

**Rutas principales:**
- `/admin/dashboard` - Dashboard principal
- `/admin/usuarios` - Gestión de usuarios
- `/admin/productos` - Gestión de productos
- `/admin/compras` - Historial de compras
- `/admin/envios` - Gestión de envíos
- `/admin/comprobantes` - Comprobantes de pago

---

### `/api_zonas`
Integración con API Zonas para cálculo de envíos y validación de códigos postales.

```
api_zonas/
├── __init__.py
├── routes.py         # Endpoints de la API
├── zones_api.py      # Lógica de integración
└── data/
    └── CPdescarga.xml   # Base de datos de códigos postales (COPOMEX)
```

**Funcionalidades:**
- Calcular costo de envío por zona
- Validar códigos postales
- Obtener información de localidades

---

### `/models`
Definición de estructuras de datos y modelos.

```
models/
├── __init__.py
├── models.py        # Modelos principales (User, Order, Product, etc)
├── forms.py         # Formularios WTForms
├── estados.py       # Estados de órdenes y envíos
└── message.py       # Mensajes de notificación
```

**Modelos principales:**
- `User` - Usuarios del sistema
- `Product` - Productos en venta
- `Category` - Categorías de productos
- `Order` - Órdenes de compra
- `OrderItem` - Items dentro de una orden
- `Cart` - Carrito de compras
- `Shipment` - Envíos

---

### `/static`
Archivos estáticos: CSS, JavaScript, imágenes, fuentes.

```
static/
├── css/
│   ├── style.css           # Estilos personalizados
│   ├── sb-admin-2.css      # Template admin
│   └── professional.css    # Estilos profesionales
├── js/
│   ├── app.js              # JavaScript principal
│   ├── custom.js           # Personalizaciones
│   ├── zones-api.js        # Integración con API Zonas
│   ├── admin-custom.js     # Scripts admin
│   └── vendor/             # Librerías externas (jQuery, etc)
├── images/                 # Imágenes del proyecto
├── img/                    # Iconos y gráficos
├── vendor/                 # Dependencias externas
│   ├── bootstrap/
│   ├── fontawesome-free/
│   ├── jquery/
│   ├── datatables/
│   └── chart.js/
└── comprobantes/          # Comprobantes de pago (uploads)
```

---

### `/templates`
Plantillas HTML Jinja2.

```
templates/
├── base.html               # Plantilla base
├── index.html              # Página de inicio
├── shop.html               # Catálogo de productos
├── cart.html               # Carrito
├── checkout.html           # Proceso de pago
├── login.html              # Iniciar sesión
├── register.html           # Registro
├── about.html              # Acerca de
├── contact.html            # Contacto
├── privacidad.html         # Política de privacidad
├── terminos.html           # Términos de servicio
├── soporte.html            # Página de soporte
│
├── admin/                  # Templates del panel admin
│   ├── dashboard.html      # Dashboard principal
│   ├── usuarios.html       # Gestión de usuarios
│   ├── productos.html      # Gestión de productos
│   ├── categorias.html     # Gestión de categorías
│   ├── compras.html        # Historial de compras
│   ├── detalles_compra.html # Detalles de una compra
│   ├── envios.html         # Gestión de envíos
│   ├── comprobantes.html   # Gestión de comprobantes
│   ├── direcciones.html    # Direcciones de usuarios
│   ├── activity_log.html   # Log de actividades
│   └── vistas/             # Componentes reutilizables
│
├── user/                   # Templates del usuario
│   ├── profile.html        # Perfil del usuario
│   ├── orders.html         # Mis órdenes
│   ├── purchases.html      # Historial de compras
│   └── rastreo.html        # Rastreo de envíos
│
└── vistas/                 # Componentes parciales
```

---

### `/utils`
Funciones y utilidades reutilizables.

```
utils/
├── __init__.py
├── auth.py           # Funciones de autenticación
└── decorators.py     # Decoradores personalizados
```

**Decoradores:**
- `@login_required` - Requiere usuario autenticado
- `@admin_required` - Requiere usuario admin
- `@api_key_required` - Requiere API key

---

### `/uploads`
Carpeta para archivos cargados por usuarios (dinámico, no se debe versionar).

```
uploads/
└── comprobantes/     # Comprobantes de pago subidos
```

---

## Archivos Raíz Principales

### Configuración y Servidor

| Archivo | Propósito |
|---------|-----------|
| `app.py` | Punto de entrada de la aplicación Flask |
| `config.py` | Configuración según ambiente |
| `extensions.py` | Inicialización de extensiones (DB, Mail, etc) |
| `wsgi.py` | Entry point para servidor WSGI (producción) |
| `requirements.txt` | Dependencias Python |

### Base de Datos

| Archivo | Propósito |
|---------|-----------|
| `ecommerce.db` | Base de datos SQLite (local) |
| `ecommerce.sql` | Dump de DB para respaldo |
| `ecommerce_produccion.sql` | Backup de producción |

### Documentación

| Archivo | Contenido |
|---------|----------|
| `README_GITHUB.md` | Documentación principal |
| `QUICK_START.md` | Guía rápida de inicio |
| `GUIA_DESPLIEGUE.md` | Despliegue a producción |
| `HTTPS_SETUP.md` | Configuración SSL/TLS |
| `JWT_AUTHENTICATION.md` | Documentación de JWT |
| `IMPLEMENTACION_API_ZONAS.md` | Detalles API Zonas |
| `CAMBIOS_REALIZADOS.md` | Historial de cambios |
| `LEEME_PRIMERO.txt` | Instrucciones iniciales |

### Seguridad y Certificados

| Archivo | Propósito |
|---------|-----------|
| `generate_certs.py` | Script para generar certificados SSL |
| `.env` | Variables de entorno (NO versionar) |

### Scripts

| Archivo | Propósito |
|---------|-----------|
| `setup.ps1` | Script de setup para Windows |
| `verify_changes.py` | Verifica cambios en sistema |
| `test_cp_22785.py` | Tests específicos |
| `paypal_client.py` | Cliente PayPal |

---

## Flujo de Datos

```
USER BROWSER
    ↓
[FRONTEND] (templates/)
    ↓
  app.py (routes/views)
    ↓
[MODELS] (models/models.py)
    ↓
[DATABASE] (ecommerce.db)
    ↓
[STATIC] (CSS, JS, Images)
```

---

## Jerarquía de Carpetas

```
ecommerce/
├── .git/                    # Git repository
├── venv/                    # Virtual environment
│
├── admin/                   # Admin panel
├── api_zonas/              # API Zones integration
├── models/                 # Data models
├── utils/                  # Utilities
├── static/                 # Static files
├── templates/              # HTML templates
├── uploads/                # User uploads
│
├── app.py                  # Main application
├── config.py              # Configuration
├── extensions.py          # Extensions
├── wsgi.py                # WSGI interface
│
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── .gitignore             # Git ignore rules
├── .gitattributes        # Git attributes
├── README_GITHUB.md      # Documentation
└── [otros archivos]
```

---

## Notas Importantes

### 🔒 No Versionar
- `.env` - Credenciales (incluido en .gitignore)
- `venv/` - Entorno virtual
- `__pycache__/` - Archivos compilados
- `*.db` en desarrollo (considerar en Git LFS para prod)
- `uploads/` - Archivos dinámicos del usuario

### 📦 Archivos Grandes
- `api_zonas/data/CPdescarga.xml` (63.22 MB) - Registrado en Git LFS
- Otros XMLs o archivos binarios > 50MB

### 🔐 Seguridad
- Nunca comitear credenciales o tokens
- Usar variables de entorno (.env)
- Mantener keys en config.py seguras

---

**Última actualización**: 27 de marzo de 2026

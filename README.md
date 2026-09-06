# Ecommerce Platform

Plataforma de comercio electrónico full-stack en Flask: catálogo de productos, carrito, checkout con pago vía PayPal o comprobante de transferencia, cálculo de envío por zonas (con validación de códigos postales vía COPOMEX) y panel administrativo.

> Full-stack Flask ecommerce platform: product catalog, cart, checkout with PayPal or manual bank-transfer proof, zone-based shipping costs (with Mexican postal-code validation via COPOMEX), and an admin dashboard.

## Características

- **Catálogo y carrito** — Productos por categoría, carrito persistente y checkout.
- **Pagos** — Integración con PayPal (`paypal_client.py`) y flujo alterno de comprobante de transferencia.
- **Envíos por zonas** — Módulo `api_zonas/` que calcula costos de envío según código postal, validado contra el servicio COPOMEX.
- **Cuentas de usuario** — Registro, login, recuperación de contraseña por correo y direcciones de envío múltiples.
- **Panel administrativo** — Blueprint `admin/` con gestión de productos, pedidos, comprobantes y bitácora de actividad (`ActivityLog`).
- **Seguridad** — CSRF, hashing de contraseñas con bcrypt, cabeceras vía Flask-Talisman, límite de tasa con Flask-Limiter.

## Stack técnico

Flask · SQLAlchemy · MySQL · Flask-Login · Flask-WTF · Flask-Mail · Flask-Limiter · Flask-Talisman · PayPal API

## Modelo de datos

`Usuario`, `Categoria`, `Producto`, `Carrito`, `DireccionEnvio`, `Pedido`, `PedidoDetalle`, `ComprobanteTransferencia`, `Envio`, `ActivityLog` — ver [`models/models.py`](./models/models.py).

## Estructura

```
ecommerce/
├── app.py                 # App Flask + registro de blueprints
├── admin/                 # Panel administrativo
├── api_zonas/             # Cálculo de zonas de envío + validación COPOMEX
├── models/                # Modelos SQLAlchemy y formularios
├── templates/ · static/   # Vistas y assets
├── paypal_client.py       # Integración de pagos
└── ecommerce.sql          # Esquema de base de datos
```

## Puesta en marcha

```bash
pip install -r requirements.txt
cp .env.example .env      # configurar credenciales de BD, correo y PayPal
python app.py
```

## Documentación adicional

El repositorio incluye documentación detallada por tema: [`INSTALLATION_GUIDE.md`](./INSTALLATION_GUIDE.md), [`API_REFERENCE.md`](./API_REFERENCE.md), [`DATABASE_MODELS.md`](./DATABASE_MODELS.md), [`JWT_AUTHENTICATION.md`](./JWT_AUTHENTICATION.md), [`GUIA_DESPLIEGUE.md`](./GUIA_DESPLIEGUE.md) y [`API_ZONAS_README.md`](./API_ZONAS_README.md).

---

## English summary

A full-stack Flask ecommerce platform with product catalog, cart/checkout, PayPal payments, zone-based shipping cost calculation backed by COPOMEX postal-code validation, and an admin dashboard for products, orders and payment proofs. See `models/models.py` for the data model and the topic-specific docs listed above for deployment and API details.

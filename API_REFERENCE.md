# API Reference y Snippets de Código

## Tabla de Contenidos
1. [Autenticación](#autenticación)
2. [Productos](#productos)
3. [Carrito](#carrito)
4. [Órdenes](#órdenes)
5. [Pagos](#pagos)
6. [Envíos](#envíos)
7. [Admin](#admin)
8. [Snippets útiles](#snippets-útiles)

---

## Autenticación

### Registro de Usuario

**Endpoint:** `POST /register`

**HTML Form:**
```html
<form method="POST" action="/register">
    <input type="text" name="username" required>
    <input type="email" name="email" required>
    <input type="password" name="password" required>
    <input type="password" name="password_confirm" required>
    <button type="submit">Registrarse</button>
</form>
```

**cURL:**
```bash
curl -X POST http://localhost:5000/register \
  -d "username=juan_perez" \
  -d "email=juan@example.com" \
  -d "password=Password123!"
```

**Python:**
```python
import requests

data = {
    'username': 'juan_perez',
    'email': 'juan@example.com',
    'password': 'Password123!'
}

response = requests.post('http://localhost:5000/register', data=data)
print(response.status_code)
print(response.json())
```

**Respuesta exitosa (302 Redirect a login):**
```
HTTP/1.1 302 FOUND
Location: /login?next=/
```

### Iniciar Sesión

**Endpoint:** `POST /login`

**HTML Form:**
```html
<form method="POST" action="/login">
    <input type="email" name="email" required>
    <input type="password" name="password" required>
    <button type="submit">Iniciar Sesión</button>
</form>
```

**cURL:**
```bash
curl -X POST http://localhost:5000/login \
  -d "email=juan@example.com" \
  -d "password=Password123!" \
  -c cookies.txt
```

**Python:**
```python
import requests

session = requests.Session()

login_data = {
    'email': 'juan@example.com',
    'password': 'Password123!'
}

response = session.post('http://localhost:5000/login', data=login_data)
# La sesión mantiene las cookies automáticamente
print("✓ Sesión iniciada" if response.status_code == 302 else "✗ Error de login")
```

### Obtener JWT Token

**Endpoint:** `POST /api/auth/token` (si está implementado)

**cURL:**
```bash
curl -X POST http://localhost:5000/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "Password123!"
  }'
```

**Respuesta:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 86400
}
```

### Cerrar Sesión

**Endpoint:** `POST /logout`

```bash
curl -X POST http://localhost:5000/logout \
  -b cookies.txt
```

---

## Productos

### Listar Productos

**Endpoint:** `GET /shop` o `GET /api/products`

**Parámetros:**
- `page` (int): Número de página (default: 1)
- `limit` (int): Productos por página (default: 12)
- `category` (str): Filtrar por categoría
- `search` (str): Búsqueda de texto
- `sort` (str): Ordenar por (price_asc, price_desc, newest, popular)
- `min_price` (float): Precio mínimo
- `max_price` (float): Precio máximo

**cURL:**
```bash
# Obtener productos de la categoría electrónica, página 1
curl "http://localhost:5000/api/products?category=electronica&page=1&limit=12"

# Buscar "laptop" y ordenar por precio ascendente
curl "http://localhost:5000/api/products?search=laptop&sort=price_asc"

# Productos con precio entre 100 y 1000
curl "http://localhost:5000/api/products?min_price=100&max_price=1000"
```

**Python:**
```python
import requests

params = {
    'page': 1,
    'limit': 12,
    'category': 'electronica',
    'sort': 'price_asc'
}

response = requests.get('http://localhost:5000/api/products', params=params)
products = response.json()['data']

for product in products:
    print(f"{product['name']}: ${product['price']}")
```

### Ver Detalles de Producto

**Endpoint:** `GET /product/<product_id>` o `GET /api/products/<product_id>`

**cURL:**
```bash
curl http://localhost:5000/api/products/5
```

**Respuesta:**
```json
{
    "id": 5,
    "name": "Laptop Pro 15",
    "description": "Una potente laptop...",
    "price": 1299.99,
    "category": "Electrónica",
    "stock": 25,
    "rating": 4.5,
    "review_count": 12,
    "sku": "LAPTOP-001",
    "images": [
        "/static/images/product1.jpg",
        "/static/images/product2.jpg"
    ],
    "reviews": [
        {
            "user": "juan_perez",
            "rating": 5,
            "comment": "Excelente producto!",
            "created_at": "2024-03-01T10:30:00"
        }
    ]
}
```

### Crear Producto (Admin)

**Endpoint:** `POST /admin/producto/crear`

```html
<form method="POST" enctype="multipart/form-data">
    <input type="text" name="name" placeholder="Nombre">
    <textarea name="description"></textarea>
    <input type="number" name="price" step="0.01">
    <input type="number" name="stock">
    <input type="text" name="sku">
    <select name="category_id">
        <!-- opciones dinámicas -->
    </select>
    <input type="file" name="image">
    <button type="submit">Crear</button>
</form>
```

**cURL:**
```bash
curl -X POST http://localhost:5000/admin/producto/crear \
  -F "name=Nuevo Laptop" \
  -F "price=1499.99" \
  -F "stock=10" \
  -F "category_id=2" \
  -F "image=@imagen.jpg" \
  -b cookies.txt
```

---

## Carrito

### Agregar al Carrito

**Endpoint:** `POST /cart/add` o `POST /api/cart/add`

**HTML Form:**
```html
<form method="POST" action="/cart/add">
    <input type="hidden" name="product_id" value="5">
    <input type="number" name="quantity" value="1" min="1">
    <button type="submit">Agregar al Carrito</button>
</form>
```

**cURL:**
```bash
curl -X POST http://localhost:5000/cart/add \
  -d "product_id=5" \
  -d "quantity=2" \
  -b cookies.txt
```

**JavaScript:**
```javascript
// Agregar al carrito con AJAX
function addToCart(productId, quantity) {
    fetch('/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `product_id=${productId}&quantity=${quantity}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`✓ ${data.message}`);
            updateCartCount();
        } else {
            alert(`✗ ${data.error}`);
        }
    });
}

// Llamar función
addToCart(5, 2);
```

### Ver Carrito

**Endpoint:** `GET /cart` o `GET /api/cart`

**cURL:**
```bash
curl http://localhost:5000/api/cart -b cookies.txt
```

**Respuesta:**
```json
{
    "items": [
        {
            "product_id": 5,
            "product_name": "Laptop Pro 15",
            "price": 1299.99,
            "quantity": 2,
            "subtotal": 2599.98
        }
    ],
    "cart_total": 2599.98,
    "item_count": 2,
    "tax": 415.99,
    "total_with_tax": 3015.97
}
```

### Actualizar Cantidad en Carrito

**Endpoint:** `PUT /cart/<item_id>` o `POST /cart/update`

```bash
curl -X PUT http://localhost:5000/cart/1 \
  -d "quantity=5" \
  -b cookies.txt
```

### Remover del Carrito

**Endpoint:** `DELETE /cart/<item_id>` o `POST /cart/remove`

```bash
curl -X DELETE http://localhost:5000/cart/1 -b cookies.txt
```

### Vaciar Carrito

**Endpoint:** `DELETE /cart` o `POST /cart/clear`

```bash
curl -X DELETE http://localhost:5000/cart -b cookies.txt
```

---

## Órdenes

### Crear Orden desde Carrito

**Endpoint:** `POST /checkout`

**HTML Form:**
```html
<form method="POST" action="/checkout">
    <!-- Dirección de envío -->
    <select name="address_id">
        <option value="">Seleccionar dirección</option>
        <!-- opciones dinámicas -->
    </select>
    
    <!-- Método de envío -->
    <select name="shipping_method">
        <option value="standard">Estándar (5-7 días) - $50</option>
        <option value="express">Express (2-3 días) - $100</option>
    </select>
    
    <!-- Código de cupón -->
    <input type="text" name="coupon_code" placeholder="Código de descuento (opcional)">
    
    <button type="submit">Proceder al Pago</button>
</form>
```

**cURL:**
```bash
curl -X POST http://localhost:5000/checkout \
  -d "address_id=1" \
  -d "shipping_method=standard" \
  -d "coupon_code=SUMMER10" \
  -b cookies.txt
```

### Ver Órdenes del Usuario

**Endpoint:** `GET /user/orders`

**cURL:**
```bash
curl http://localhost:5000/api/orders -b cookies.txt
```

**Respuesta:**
```json
{
    "orders": [
        {
            "id": 1,
            "order_number": "ORD-20240326-001",
            "total": 1557.98,
            "status": "delivered",
            "created_at": "2024-03-26T10:30:00",
            "items_count": 1
        }
    ]
}
```

### Ver Detalles de Orden

**Endpoint:** `GET /order/<order_id>` o `GET /api/orders/<order_id>`

```bash
curl http://localhost:5000/api/orders/1 -b cookies.txt
```

**Respuesta:**
```json
{
    "id": 1,
    "order_number": "ORD-20240326-001",
    "status": "delivered",
    "payment_status": "completed",
    "subtotal": 1299.99,
    "tax": 207.99,
    "shipping": 50.00,
    "discount": 0,
    "total": 1557.98,
    "created_at": "2024-03-26T10:30:00",
    "items": [
        {
            "product_name": "Laptop Pro 15",
            "quantity": 1,
            "price": 1299.99,
            "subtotal": 1299.99
        }
    ],
    "shipping_address": {
        "street": "Calle Principal 123",
        "city": "Ciudad de México",
        "postal_code": "28000",
        "country": "México"
    },
    "shipment": {
        "tracking_number": "1Z999AA10123456784",
        "carrier": "UPS",
        "status": "delivered",
        "shipped_date": "2024-03-26T15:00:00",
        "delivered_at": "2024-03-29T16:00:00"
    }
}
```

---

## Pagos

### Iniciar Pago con PayPal

**Endpoint:** `POST /checkout/paypal`

```html
<form method="POST" action="/checkout/paypal">
    <input type="hidden" name="order_id" value="1">
    <button type="submit">Pagar con PayPal</button>
</form>
```

### Callback de PayPal (Ejecutar Pago)

**Endpoint:** `GET /checkout/paypal/execute`

**Parámetros en URL:**
- `paymentId`: ID del pago de PayPal
- `PayerID`: ID del pagador
- `token`: Token del pago

Esto ocurre automáticamente después de que el usuario apruebe en PayPal.

### Ver Estado de Pago

```bash
curl http://localhost:5000/api/orders/1/payment -b cookies.txt
```

**Respuesta:**
```json
{
    "payment": {
        "method": "paypal",
        "amount": 1557.98,
        "status": "completed",
        "transaction_id": "PAYID-XXXXXXXXXXXX",
        "payer_email": "juan@example.com",
        "created_at": "2024-03-26T10:35:00"
    }
}
```

---

## Envíos

### Rastrear Envío

**Endpoint:** `GET /track/<tracking_number>` o `GET /api/orders/<order_id>/track`

**cURL:**
```bash
curl http://localhost:5000/api/orders/1/track
```

**Respuesta:**
```json
{
    "tracking_number": "1Z999AA10123456784",
    "carrier": "UPS",
    "status": "in_transit",
    "shipped_date": "2024-03-26T15:00:00",
    "estimated_delivery": "2024-03-28T23:59:59",
    "events": [
        {
            "date": "2024-03-26T15:00:00",
            "status": "Picked up",
            "location": "Centro de Distribución Ciudad de México"
        },
        {
            "date": "2024-03-27T08:30:00",
            "status": "In Transit",
            "location": "Centro de Distribución Guadalajara"
        },
        {
            "date": "2024-03-28T12:00:00",
            "status": "Out for Delivery",
            "location": "Local de Distribución Guadalajara"
        }
    ]
}
```

### Actualizar Envío (Admin)

**Endpoint:** `POST /admin/shipment/<shipment_id>/update`

```bash
curl -X POST http://localhost:5000/admin/shipment/1/update \
  -d "status=delivered" \
  -d "tracking_number=1Z999AA10123456784" \
  -b cookies.txt
```

---

## Admin

### Dashboard de Admin

**Endpoint:** `GET /admin/dashboard`

Acceso automatizado:
```bash
curl http://localhost:5000/admin/dashboard -b cookies.txt
```

Los datos se obtienen mediante AJAX del API.

### Obtener Estadísticas

**Endpoint:** `GET /api/admin/stats`

```bash
curl http://localhost:5000/api/admin/stats \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

**Respuesta:**
```json
{
    "total_orders": 125,
    "total_revenue": 45230.50,
    "orders_this_month": 23,
    "revenue_this_month": 8940.25,
    "active_users": 542,
    "avg_order_value": 361.84,
    "conversion_rate": 3.2,
    "top_products": [
        {
            "name": "Laptop Pro 15",
            "sales": 12,
            "revenue": 15599.88
        }
    ]
}
```

### Listar Todas las Órdenes (Admin)

**Endpoint:** `GET /admin/orders` o `GET /api/admin/orders`

```bash
curl "http://localhost:5000/api/admin/orders?status=pending&page=1" \
  -H "Authorization: Bearer TOKEN"
```

### Cambiar Estado de Orden (Admin)

**Endpoint:** `PUT /admin/orders/<order_id>`

```bash
curl -X PUT http://localhost:5000/admin/orders/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped"}' \
  -H "Authorization: Bearer TOKEN"
```

### Generar Reportes

**Endpoint:** `GET /admin/reports`

```bash
# Reporte de ventas por período
curl "http://localhost:5000/admin/reports/sales?start_date=2024-01-01&end_date=2024-03-31" \
  -H "Authorization: Bearer TOKEN"
```

---

## Snippets Útiles

### Script Python para Crear Órdenes de Prueba

```python
from app import app, db
from models.models import User, Product, Order, OrderItem, Address
from datetime import datetime, timedelta
import random

with app.app_context():
    # Obtener usuario
    user = User.query.first()
    
    # Crear 10 órdenes de prueba
    for i in range(10):
        # Crear orden
        order = Order(
            user_id=user.id,
            status=random.choice(['pending', 'confirmed', 'shipped', 'delivered']),
            payment_status='completed'
        )
        order.generate_order_number()
        
        # Agregar items aleatorios
        products = Product.query.limit(3).all()
        for product in products:
            order_item = OrderItem(
                product_id=product.id,
                product_name=product.name,
                product_sku=product.sku,
                price_at_purchase=product.price,
                quantity=random.randint(1, 3)
            )
            order.items.append(order_item)
        
        # Calcular totales
        order.calculate_total()
        
        # Fecha aleatoria
        days_ago = random.randint(1, 90)
        order.created_at = datetime.utcnow() - timedelta(days=days_ago)
        
        db.session.add(order)
    
    db.session.commit()
    print("✓ 10 órdenes de prueba creadas")
```

### JavaScript para Mostrar Cartilla de Productos

```javascript
// Obtener productos y mostrar en página
async function loadProducts(page = 1) {
    try {
        const response = await fetch(`/api/products?page=${page}&limit=12`);
        const data = await response.json();
        
        const container = document.getElementById('products-container');
        container.innerHTML = '';
        
        data.data.forEach(product => {
            const html = `
                <div class="product-card">
                    <img src="${product.image}" alt="${product.name}">
                    <h3>${product.name}</h3>
                    <p class="price">$${product.price.toFixed(2)}</p>
                    <div class="rating">
                        ⭐ ${product.rating}/5 (${product.review_count} reseñas)
                    </div>
                    <button onclick="addToCart(${product.id}, 1)">
                        Agregar al Carrito
                    </button>
                </div>
            `;
            container.innerHTML += html;
        });
        
        // Actualizar paginación
        updatePagination(data.pagination);
        
    } catch (error) {
        console.error('Error cargando productos:', error);
    }
}

// Llamar al cargar página
loadProducts(1);
```

### Python para Enviar Email de Confirmación de Orden

```python
from flask_mail import Message
from app import mail

def send_order_confirmation(order):
    """Envía email de confirmación de orden"""
    
    email_body = f"""
    Hola {order.user.first_name},
    
    Tu orden {order.order_number} ha sido confirmada.
    
    Detalles:
    - Total: ${order.total_amount}
    - Estado: {order.status}
    - Fecha: {order.created_at.strftime('%d/%m/%Y %H:%M')}
    
    Items:
    """
    
    for item in order.items:
        email_body += f"\n- {item.product_name} x{item.quantity} = ${item.get_subtotal()}"
    
    email_body += f"""
    
    Rastrear tu envío: {url_for('track_order', order_id=order.id, _external=True)}
    
    ¡Gracias por tu compra!
    Ecommerce Team
    """
    
    msg = Message(
        subject=f"Confirmación de Orden {order.order_number}",
        recipients=[order.user.email],
        body=email_body
    )
    
    mail.send(msg)
    print(f"✓ Email enviado a {order.user.email}")

# Usar en routes
send_order_confirmation(order)
```

---

¡Toda la documentación API completa! 📚

Para más ayuda, ver README.md o INSTALLATION_GUIDE.md.

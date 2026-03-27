# Documentación Completa de Modelos y Base de Datos

## Índice
- [Visión General](#visión-general)
- [Diagrama ER](#diagrama-er)
- [Modelos Detallados](#modelos-detallados)
- [Relaciones](#relaciones)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## Visión General

Base de datos relacional que maneja:
- **Usuarios y Autenticación**
- **Productos y Categorías**
- **Órdenes y Items**
- **Carritos de Compra**
- **Direcciones de Envío**
- **Pagos y Transacciones**
- **Envíos y Rastreo**
- **Reseñas y Calificaciones**
- **Logs de Actividades**

---

## Diagrama ER

```
┌─────────────────┐         ┌──────────────────┐
│     USER        │         │    CATEGORY      │
├─────────────────┤         ├──────────────────┤
│ id (PK)         │         │ id (PK)          │
│ username        │         │ name             │
│ email           │         │ description      │
│ password_hash   │         │ created_at       │
│ is_admin        │         └──────────────────┘
│ is_active       │                  ▲
│ created_at      │                  │
└─────────────────┘                  │ FK
        ▲                            │
        │ FK                    ┌──────────────────┐
        │                       │    PRODUCT       │
        │                       ├──────────────────┤
        │                       │ id (PK)          │
        │                       │ name             │
        │                       │ description      │
        │                       │ price            │
        │                       │ category_id (FK) │
        │                       │ stock            │
        │                       │ sku              │
        │                       │ created_at       │
        │                       └──────────────────┘
        │                               ▲
        ├─────────────────────┬─────────┘
        │                     │ (1..*)
        │                 ┌───────────────────────┐
        │                 │   CART_ITEM           │
        │                 ├───────────────────────┤
        │                 │ id (PK)               │
        │                 │ user_id (FK)         │
        │                 │ product_id (FK)      │
        │                 │ quantity              │
        │                 │ added_at              │
        │                 └───────────────────────┘
        │
        │ FK (1..*)
        │
    ┌───────────────────┐      ┌──────────────────┐
    │     ORDER         │      │  ORDER_ITEM      │
    ├───────────────────┤  (1)─┤──────────────────┤
    │ id (PK)           │──────│ id (PK)          │
    │ user_id (FK)      │ (*)  │ order_id (FK)    │
    │ total_amount      │      │ product_id (FK)  │
    │ status            │      │ price_at_purchase│
    │ created_at        │      │ quantity         │
    │ updated_at        │      │ subtotal         │
    └───────────────────┘      └──────────────────┘
            │
            │ FK
            ▼
    ┌───────────────────┐
    │    ADDRESS        │
    ├───────────────────┤
    │ id (PK)           │
    │ user_id (FK)      │
    │ street            │
    │ city              │
    │ state             │
    │ postal_code       │
    │ country           │
    │ is_default        │
    └───────────────────┘

    ┌──────────────────┐       ┌─────────────────┐
    │    PAYMENT       │       │   SHIPMENT      │
    ├──────────────────┤       ├─────────────────┤
    │ id (PK)          │       │ id (PK)         │
    │ order_id (FK)    │       │ order_id (FK)   │
    │ amount           │       │ address_id (FK) │
    │ method           │       │ status          │
    │ transaction_id   │       │ tracking_number │
    │ status           │       │ carrier         │
    │ created_at       │       │ shipped_date    │
    └──────────────────┘       │ delivered_date  │
                               └─────────────────┘

    ┌──────────────────┐       ┌─────────────────┐
    │    REVIEW        │       │ ACTIVITY_LOG    │
    ├──────────────────┤       ├─────────────────┤
    │ id (PK)          │       │ id (PK)         │
    │ product_id (FK)  │       │ user_id (FK)    │
    │ user_id (FK)     │       │ action          │
    │ rating (1-5)     │       │ description     │
    │ comment          │       │ ip_address      │
    │ created_at       │       │ timestamp       │
    └──────────────────┘       └─────────────────┘
```

---

## Modelos Detallados

### 1. USER (Usuarios)

Almacena información de usuarios y administradores del sistema.

```python
class User(db.Model):
    __tablename__ = 'user'
    
    # Campos primarios
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Información personal
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    
    # Estado y roles
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    addresses = db.relationship('Address', backref='user', lazy=True, cascade='all,delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all,delete-orphan')
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all,delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all,delete-orphan')
    activity_logs = db.relationship('ActivityLog', backref='user', lazy=True, cascade='all,delete-orphan')
    
    def verify_password(self, password):
        """Verifica contraseña contra el hash"""
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        """Establece nueva contraseña con hash bcrypt"""
        self.password_hash = generate_password_hash(password)
    
    def is_authenticated(self):
        """Para Flask-Login"""
        return True
    
    def is_active(self):
        """Para Flask-Login"""
        return self.is_active
    
    def get_id(self):
        """Para Flask-Login"""
        return str(self.id)
```

**Ejemplo de uso:**
```python
# Crear usuario
new_user = User(
    username='juan_perez',
    email='juan@example.com',
    first_name='Juan',
    last_name='Pérez'
)
new_user.set_password('Password123!')
db.session.add(new_user)
db.session.commit()

# Buscar usuario
user = User.query.filter_by(email='juan@example.com').first()

# Verificar contraseña
if user and user.verify_password('Password123!'):
    print("✓ Contraseña correcta")

# Hacer admin
user.is_admin = True
db.session.commit()
```

---

### 2. CATEGORY (Categorías)

Agrupa productos en categorías.

```python
class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    slug = db.Column(db.String(100), unique=True)
    image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación
    products = db.relationship('Product', backref='category', lazy=True, cascade='all,delete-orphan')
    
    def get_product_count(self):
        """Retorna cantidad de productos activos en esta categoría"""
        return Product.query.filter_by(category_id=self.id, is_active=True).count()
```

**Ejemplo de uso:**
```python
# Crear categoría
cat = Category(
    name='Electrónica',
    description='Productos electrónicos diversos',
    slug='electronica'
)
db.session.add(cat)
db.session.commit()

# Obtener todos los productos de una categoría
electronics = Category.query.filter_by(slug='electronica').first()
products = electronics.products
```

---

### 3. PRODUCT (Productos)

Almacena información de productos disponibles.

```python
class Product(db.Model):
    __tablename__ = 'product'
    
    # Identificadores
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True)
    
    # Información del producto
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    short_description = db.Column(db.String(500))
    
    # Precios e inventario
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float)  # Precio de costo
    stock = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=10)
    
    # Media y estado
    image = db.Column(db.String(255))
    images = db.Column(db.JSON)  # Array de URLs de imágenes
    rating = db.Column(db.Float, default=0)
    review_count = db.Column(db.Integer, default=0)
    
    # Categorización
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # Estados
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_new = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True, cascade='all,delete-orphan')
    
    def update_rating(self):
        """Actualiza rating basado en reseñas"""
        if self.reviews:
            avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(product_id=self.id).scalar()
            self.rating = round(avg_rating, 1) if avg_rating else 0
            self.review_count = len(self.reviews)
            db.session.commit()
    
    def is_in_stock(self):
        """Verifica si hay stock disponible"""
        return self.stock > 0
    
    def get_discount_price(self, discount_percent):
        """Calcula precio con descuento"""
        return self.price * (1 - discount_percent / 100)
```

**Ejemplo de uso:**
```python
# Crear producto
laptop = Product(
    sku='LAPTOP-001',
    name='Laptop Pro 15',
    description='Laptop profesional...',
    price=1299.99,
    cost=900.00,
    stock=25,
    category_id=1
)
db.session.add(laptop)
db.session.commit()

# Buscar productos activos
active_products = Product.query.filter_by(is_active=True).all()

# Productos sin stock
out_of_stock = Product.query.filter(Product.stock == 0).all()
```

---

### 4. CART_ITEM (Items del Carrito)

Almacena items temporales en carritos de compra.

```python
class CartItem(db.Model):
    __tablename__ = 'cart_item'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    quantity = db.Column(db.Integer, minimum=1, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_subtotal(self):
        """Calcula subtotal del item"""
        return self.product.price * self.quantity
    
    def get_line_total_with_tax(self, tax_rate=0.16):
        """Subtotal con impuesto (16% en México)"""
        subtotal = self.get_subtotal()
        return subtotal * (1 + tax_rate)
```

**Ejemplo de uso:**
```python
# Agregar al carrito
cart_item = CartItem(
    user_id=1,
    product_id=5,
    quantity=2
)
db.session.add(cart_item)
db.session.commit()

# Obtener carrito del usuario
user_cart = CartItem.query.filter_by(user_id=1).all()

# Calcular total del carrito
cart_total = sum(item.get_subtotal() for item in user_cart)
```

---

### 5. ORDER (Órdenes)

Registra cada pedido realizado.

```python
class Order(db.Model):
    __tablename__ = 'order'
    
    # Identificadores
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)  # ORD-2024-001234
    
    # Usuario
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Montos
    subtotal = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, default=0)
    shipping_cost = db.Column(db.Float, default=0)
    discount_amount = db.Column(db.Float, default=0)
    total_amount = db.Column(db.Float, nullable=False)
    
    # Estado
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, shipped, delivered, cancelled
    payment_status = db.Column(db.String(50), default='pending')  # pending, completed, failed, refunded
    
    # Notas
    notes = db.Column(db.Text)
    admin_notes = db.Column(db.Text)
    
    # Fechas
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estimated_delivery = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    
    # Relaciones
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all,delete-orphan')
    payment = db.relationship('Payment', backref='order', uselist=False, lazy=True)
    shipment = db.relationship('Shipment', backref='order', uselist=False, lazy=True)
    
    def calculate_total(self):
        """Recalcula el total de la orden"""
        self.subtotal = sum(item.get_subtotal() for item in self.items)
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_cost - self.discount_amount
        return self.total_amount
    
    def mark_as_paid(self):
        """Marca orden como pagada"""
        self.payment_status = 'completed'
        self.status = 'confirmed'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def generate_order_number(self):
        """Genera número de orden único"""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        self.order_number = f"ORD-{timestamp}-{self.user_id}"
```

**Ejemplo de uso:**
```python
# Crear orden
order = Order(
    user_id=1,
    subtotal=1299.99,
    tax_amount=207.99,
    shipping_cost=50.00,
    total_amount=1557.98
)
order.generate_order_number()
db.session.add(order)
db.session.commit()

# Cambiar estado
order.status = 'shipped'
order.updated_at = datetime.utcnow()
db.session.commit()

# Calcular total
order.calculate_total()
```

---

### 6. ORDER_ITEM (Items de Orden)

Detalle de cada producto en una orden.

```python
class OrderItem(db.Model):
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    # Información del producto al momento de compra
    product_name = db.Column(db.String(200), nullable=False)
    product_sku = db.Column(db.String(100), nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)  # Precio que pagó
    quantity = db.Column(db.Integer, nullable=False)
    
    def get_subtotal(self):
        """Subtotal de este item"""
        return self.price_at_purchase * self.quantity
```

---

### 7. ADDRESS (Direcciones)

Almacena direcciones de envío de usuarios.

```python
class Address(db.Model):
    __tablename__ = 'address'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Información
    label = db.Column(db.String(100))  # "Casa", "Oficina", etc
    street = db.Column(db.String(200), nullable=False)
    street_number = db.Column(db.String(20), nullable=False)
    apartment = db.Column(db.String(50))  # Apt, Dpto, etc
    
    # Geolocalización
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), default='México', nullable=False)
    
    # Contacto
    phone = db.Column(db.String(20))
    
    # Preferencias
    is_default = db.Column(db.Boolean, default=False)
    is_billing_address = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_full_address(self):
        """Retorna dirección formateada"""
        return f"{self.street} {self.street_number}, {self.apartment}, {self.city}, {self.state} {self.postal_code}"
```

---

### 8. PAYMENT (Pagos)

Registro de pagos procesados.

```python
class Payment(db.Model):
    __tablename__ = 'payment'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, unique=True)
    
    method = db.Column(db.String(50), nullable=False)  # 'paypal', 'credit_card', 'cash'
    amount = db.Column(db.Float, nullable=False)
    
    # PayPal info
    transaction_id = db.Column(db.String(100))
    payer_id = db.Column(db.String(100))
    payer_email = db.Column(db.String(120))
    
    status = db.Column(db.String(50), default='pending')  # pending, completed, failed, refunded
    
    receipt_url = db.Column(db.String(255))  # URL del recibo
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

---

### 9. SHIPMENT (Envíos)

Información de envíos y rastreo.

```python
class Shipment(db.Model):
    __tablename__ = 'shipment'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    
    # Información de envío
    tracking_number = db.Column(db.String(100), unique=True, nullable=False)
    carrier = db.Column(db.String(100))  # 'UPS', 'FedEx', 'DHL', 'Estafeta'
    method = db.Column(db.String(100))  # 'standard', 'express', 'overnight'
    cost = db.Column(db.Float, nullable=False)
    
    # Estado
    status = db.Column(db.String(50), default='pending')  # pending, picked_up, in_transit, out_for_delivery, delivered
    
    # Fechas
    shipped_date = db.Column(db.DateTime)
    estimated_delivery = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    
    # Notas
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def mark_as_delivered(self):
        """Marca envío como entregado"""
        self.status = 'delivered'
        self.delivered_at = datetime.utcnow()
        self.order.status = 'delivered'
        db.session.commit()
```

---

### 10. REVIEW (Reseñas)

Reseñas y calificaciones de productos.

```python
class Review(db.Model):
    __tablename__ = 'review'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    title = db.Column(db.String(200))
    comment = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 estrellas
    
    helpful_count = db.Column(db.Integer, default=0)
    
    is_verified_purchase = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def mark_as_verified(self):
        """Marca como compra verificada"""
        # Verificar que el usuario compró este producto
        has_purchased = OrderItem.query.join(Order).filter(
            OrderItem.product_id == self.product_id,
            Order.user_id == self.user_id,
            Order.payment_status == 'completed'
        ).first()
        
        self.is_verified_purchase = bool(has_purchased)
        db.session.commit()
```

---

### 11. ACTIVITY_LOG (Log de Actividades)

Auditoría de todas las acciones importantes.

```python
class ActivityLog(db.Model):
    __tablename__ = 'activity_log'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    action = db.Column(db.String(100), nullable=False)  # 'login', 'logout', 'create_order', etc
    description = db.Column(db.Text)
    entity_type = db.Column(db.String(50))  # 'order', 'product', 'user'
    entity_id = db.Column(db.Integer)  # ID de la entidad afectada
    
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def log_action(user_id, action, description='', entity_type=None, entity_id=None):
        """Método auxiliar para registrar acciones"""
        log = ActivityLog(
            user_id=user_id,
            action=action,
            description=description,
            entity_type=entity_type,
            entity_id=entity_id,
            ip_address=request.remote_addr if request else None,
            user_agent=request.user_agent.string if request else None
        )
        db.session.add(log)
        db.session.commit()
        return log
```

---

## Relaciones

### User → Order (1 a Muchos)
```python
# Un usuario puede tener múltiples órdenes
user = User.query.get(1)
for order in user.orders:
    print(f"Orden: {order.order_number}")
```

### User → Address (1 a Muchos)
```python
# Un usuario puede tener múltiples direcciones
user = User.query.get(1)
for address in user.addresses:
    print(address.get_full_address())
```

### Category → Product (1 a Muchos)
```python
# Una categoría puede tener múltiples productos
category = Category.query.get(1)
for product in category.products:
    print(f"{product.name}: ${product.price}")
```

### Product → Review (1 a Muchos)
```python
# Un producto puede tener múltiples reseñas
product = Product.query.get(1)
for review in product.reviews:
    print(f"{review.user.username}: {review.rating}/5 - {review.comment}")
```

### Order → OrderItem (1 a Muchos)
```python
# Una orden contiene múltiples items
order = Order.query.get(1)
for item in order.items:
    print(f"{item.product_name}: {item.quantity} x ${item.price_at_purchase}")
```

### Order → Payment (1 a 1)
```python
# Una orden tiene un único pago
order = Order.query.get(1)
if order.payment:
    print(f"Pago: ${order.payment.amount} via {order.payment.method}")
```

### Order → Shipment (1 a 1)
```python
# Una orden tiene un único envío
order = Order.query.get(1)
if order.shipment:
    print(f"Rastreo: {order.shipment.tracking_number}")
    print(f"Estatus: {order.shipment.status}")
```

---

## Ejemplos de Uso Práctico

### Crear una Orden Completa

```python
from app import app, db
from models.models import User, Product, Order, OrderItem, Address, CartItem

with app.app_context():
    # 1. Obtener usuario
    user = User.query.get(1)
    
    # 2. Obtener carrito
    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    
    # 3. Crear orden
    order = Order(
        user_id=user.id,
        status='pending',
        payment_status='pending'
    )
    order.generate_order_number()
    
    # 4. Agregar items
    for cart_item in cart_items:
        order_item = OrderItem(
            product_id=cart_item.product.id,
            product_name=cart_item.product.name,
            product_sku=cart_item.product.sku,
            price_at_purchase=cart_item.product.price,
            quantity=cart_item.quantity
        )
        order.items.append(order_item)
    
    # 5. Calcular totales
    order.subtotal = sum(item.get_subtotal() for item in order.items)
    order.tax_amount = order.subtotal * 0.16  # 16% IVA México
    order.total_amount = order.subtotal + order.tax_amount
    
    # 6. Guardar
    db.session.add(order)
    db.session.commit()
    
    # 7. Limpiar carrito
    CartItem.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    
    print(f"✓ Orden creada: {order.order_number}")
    print(f"  Total: ${order.total_amount}")
```

### Procesar Pago PayPal

```python
from models.models import Order, Payment

with app.app_context():
    order = Order.query.filter_by(order_number='ORD-20240326120000-1').first()
    
    # Crear registro de pago
    payment = Payment(
        order_id=order.id,
        method='paypal',
        amount=order.total_amount,
        transaction_id='PAYID-XXXXXXXXXXXX',
        payer_email='user@example.com',
        status='completed'
    )
    
    # Actualizar orden
    order.payment_status = 'completed'
    order.status = 'confirmed'
    
    db.session.add(payment)
    db.session.commit()
    
    print(f"✓ Pago procesado: {order.order_number}")
    print(f"  ID Transacción: {payment.transaction_id}")
```

---

¡La base de datos está completamente documentada! 📚

Continúa leyendo otros documentos para más detalles sobre la API, despliegue e integración.

from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'  # <- asegúrate que coincide con el nombre real de tu tabla
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(64), unique=True)
    token_expiry = db.Column(db.DateTime)
    admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.email}>'
    
    @property
    def is_authenticated(self):
        return True  # o lógica que quieras

    @property
    def is_active(self):
        return self.verify == 1

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
    
class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Producto(db.Model):
    __tablename__ = 'productos'  # <- Aquí pon el nombre exacto de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    imagen_url = db.Column(db.String(255))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)  # 👈 Agregado
    # Relaciones (opcional)
    categoria = db.relationship('Categoria', backref='productos')
    
    
class Carrito(db.Model):
    __tablename__ = 'carrito'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    fecha_agregado = db.Column(db.DateTime, default=datetime.utcnow)
    imagen_url = db.Column(db.String(255))  # Nueva columna para URL de imagen

    producto = db.relationship('Producto', backref='carritos')
    usuario = db.relationship('Usuario', backref='carritos')

class DireccionEnvio(db.Model):
    __tablename__ = 'direccion_envio'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    colonia = db.Column(db.String(150), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(10), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    referencias = db.Column(db.Text, nullable=True)  # <-- Nuevo campo agregado

    usuario = db.relationship('Usuario', backref='direccion_envio')
    
class Pedido(db.Model):
    __tablename__ = 'compras'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    direccion_envio_id = db.Column(db.Integer, db.ForeignKey('direccion_envio.id'), nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=False)

    detalles = db.relationship('PedidoDetalle', back_populates='compra', cascade='all, delete-orphan')


class PedidoDetalle(db.Model):
    __tablename__ = 'detalle_compra'

    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)

    compra = db.relationship('Pedido', back_populates='detalles')
    producto = db.relationship('Producto', backref='detalles_pedido')  # ✅ Esto es lo que habilita .producto.nombre
    
class ComprobanteTransferencia(db.Model):
    __tablename__ = 'comprobantes'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('compras.id'), nullable=False)
    archivo = db.Column(db.String(200), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    verificado = db.Column(db.Boolean, default=False)

    pedido = db.relationship('Pedido', backref='comprobante')
    
class Envio(db.Model):
    __tablename__ = 'envios'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('compras.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'procesado', 'aceptado', 'enviado', 'entregado', 'cancelado'), 
                       default='pendiente', nullable=False)
    numero_rastreo = db.Column(db.String(150), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    direccion_envio_id = db.Column(db.Integer, db.ForeignKey('direccion_envio.id'), nullable=False)
    observaciones = db.Column(db.Text)

    pedido = db.relationship('Pedido', backref='envios')
    usuario = db.relationship('Usuario', backref='envios')
    direccion_envio = db.relationship('DireccionEnvio', backref='envios')

    def __repr__(self):
        return f"<Envio id={self.id} pedido_id={self.pedido_id} estado={self.estado}>"


class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)  # si quieres enlazar con usuario
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)  # opcional, IP del usuario
    extra_info = db.Column(db.Text, nullable=True)  # para guardar detalles adicionales si quieres

    user = db.relationship('Usuario', backref='activity_logs')




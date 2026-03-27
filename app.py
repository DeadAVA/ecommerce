from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, abort, make_response, current_app
from config import Config
from models.estados import *
from models import db
from models.models import Usuario, Producto, Carrito, DireccionEnvio, Pedido, PedidoDetalle, ComprobanteTransferencia, Envio, Categoria
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from models.message import enviar_correo_verificacion
from werkzeug.utils import secure_filename
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypal_client import paypal_client
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utils.decorators import admin_required, format_fecha
from utils.auth import JWTAuth, token_required, refresh_token_required
from datetime import datetime
from flask_caching import Cache
from werkzeug.middleware.proxy_fix import ProxyFix
import requests
import uuid
import stripe
import os
import ssl
import logging
import jwt


# ✅ 1. Crear instancia de la app
app = Flask(__name__)
app.config.from_object(Config)

# Stripe config
stripe.api_key = app.config.get('STRIPE_SECRET_KEY')

# Aceptar cabeceras de proxy inverso (Nginx/Traefik)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)



# ✅ 3. Inicializar otras extensiones
db.init_app(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Rate limiting básico
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[app.config.get('RATELIMIT_DEFAULT')],
    storage_uri=app.config.get('RATELIMIT_STORAGE_URI')
)
limiter.init_app(app)

# ✅ 4. Configuración adicional
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), Config.UPLOAD_FOLDER)
app.jinja_env.filters['format_fecha'] = format_fecha

# ✅ Configuración de logging
logging.basicConfig(level=logging.DEBUG if app.debug else logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Configuración HTTPS/SSL

from admin import admin_bp
import admin.routes
from api_zonas.routes import zones_bp

# Registrar Blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(zones_bp)

csp = {
    'default-src': ["'self'"],
    'script-src': ["'self'", "'unsafe-inline'", 'cdn.jsdelivr.net', 'cdnjs.cloudflare.com'],
    'style-src': ["'self'", "'unsafe-inline'", 'cdn.jsdelivr.net', 'cdnjs.cloudflare.com', 'fonts.googleapis.com'],
    'img-src': ["'self'", 'data:', 'https:'],
    'font-src': ["'self'", 'cdnjs.cloudflare.com', 'fonts.gstatic.com'],
    'connect-src': ["'self'", 'cdn.jsdelivr.net']  # 'self' permite /api/zones/
}

Talisman(
    app,
    content_security_policy=csp,
    force_https=app.config.get('FORCE_HTTPS', False),
    session_cookie_secure=app.config.get('SESSION_COOKIE_SECURE', False),
    session_cookie_samesite=app.config['SESSION_COOKIE_SAMESITE'],
    referrer_policy='strict-origin-when-cross-origin'
)

cache = Cache(app, config={'CACHE_TYPE': app.config['CACHE_TYPE'], 'CACHE_REDIS_URL': app.config['CACHE_REDIS_URL']})

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    if app.config.get('FORCE_HTTPS', False):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    else:
        response.headers.pop('Strict-Transport-Security', None)
    response.headers['X-Permitted-Cross-Domain-Policies'] = 'none'
    return response

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            nombre = request.form.get('nombre', '').strip()
            apellido = request.form.get('apellido', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            
            # Validaciones básicas
            if not all([username, nombre, apellido, email, password]):
                flash('Todos los campos son obligatorios.', 'danger')
                return redirect(url_for('register'))
            
            if len(password) < 6:
                flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
                return redirect(url_for('register'))
            
            # Validar existencia usuario/email
            if Usuario.query.filter_by(email=email).first():
                flash('El email ya está registrado.', 'danger')
                return redirect(url_for('register'))
            if Usuario.query.filter_by(username=username).first():
                flash('El username ya está registrado.', 'danger')
                return redirect(url_for('register'))
            
            user = Usuario(username=username, nombre=nombre, apellido=apellido, email=email)
            user.set_password(password)
            user.verify = False
            db.session.add(user)
            db.session.commit()

            # Enviar correo verificación
            enviar_correo_verificacion(user)

            flash('Registro exitoso! Revisa tu correo para confirmar la cuenta.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"Error en registro: {str(e)}")
            db.session.rollback()
            flash('Error al registrar. Por favor intenta de nuevo.', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)  # 1 hora para confirmar
    except SignatureExpired:
        flash('El enlace de confirmación ha expirado.', 'danger')
        return redirect(url_for('login'))
    except BadSignature:
        flash('El enlace de confirmación no es válido.', 'danger')
        return redirect(url_for('login'))
    user = Usuario.query.filter_by(email=email).first_or_404()
    if user.verify:
        flash('Cuenta ya verificada. Por favor ingresa.', 'info')
    else:
        user.verify = True
        db.session.commit()
        flash('Cuenta verificada con éxito!', 'success')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            
            if not email or not password:
                flash('Email y contraseña son requeridos.', 'danger')
                return redirect(url_for('login'))
            
            user = Usuario.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                if not user.verify:
                    flash('Debes verificar tu correo antes de ingresar.', 'warning')
                    return redirect(url_for('login'))
                
                # Crear tokens JWT
                access_token, refresh_token = JWTAuth.create_tokens(user.id, user.email)
                
                # Login con Flask-Login para compatibilidad
                login_user(user)
                
                # Crear respuesta y agregar cookies
                response = make_response(redirect(url_for('index')))
                response = JWTAuth.set_token_cookies(response, access_token, refresh_token)
                
                flash('¡Bienvenido!', 'success')
                logger.info(f"Usuario {user.email} inició sesión")
                
                return response
            else:
                flash('Email o contraseña incorrectos.', 'danger')
                logger.warning(f"Intento de login fallido para: {email}")
        except Exception as e:
            logger.error(f"Error en login: {str(e)}")
            flash('Error al iniciar sesión. Por favor intenta de nuevo.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    response = make_response(redirect(url_for('index')))
    response = JWTAuth.clear_token_cookies(response)
    flash('Has cerrado sesión.', 'info')
    logger.info(f"Usuario {current_user.email} cerró sesión")
    return response

@app.route('/api/refresh-token', methods=['POST'])
@refresh_token_required
def refresh_token():
    """Refresca el access token usando el refresh token"""
    try:
        user = db.session.get(Usuario, request.user_id)
        if not user:
            return jsonify({'message': 'Usuario no encontrado'}), 401
        
        # Crear nuevo access token
        access_token, refresh_token = JWTAuth.create_tokens(user.id, user.email)
        
        response = make_response(jsonify({'message': 'Token refrescado'}))
        response = JWTAuth.set_token_cookies(response, access_token, refresh_token)
        
        return response, 200
    except Exception as e:
        logger.error(f"Error al refrescar token: {str(e)}")
        return jsonify({'message': 'Error al refrescar token'}), 500

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        user = Usuario.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt='password-reset')
            link = url_for('reset_password', token=token, _external=True)
            msg = Message('Restablece tu contraseña', recipients=[email])
            msg.body = f'Hola {user.nombre}, haz clic en el siguiente enlace para restablecer tu contraseña: {link}'
            mail.send(msg)
            flash('Correo de recuperación enviado.', 'info')
        else:
            flash('No existe una cuenta con ese correo.', 'warning')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset', max_age=3600)
    except SignatureExpired:
        flash('El enlace para restablecer contraseña ha expirado.', 'danger')
        return redirect(url_for('reset_password_request'))
    except BadSignature:
        flash('Enlace no válido.', 'danger')
        return redirect(url_for('reset_password_request'))
    user = Usuario.query.filter_by(email=email).first_or_404()
    if request.method == 'POST':
        password = request.form['password']
        user.set_password(password)
        db.session.commit()
        flash('Contraseña actualizada con éxito!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

@app.route('/privacidad')
def privacidad():
    return render_template('privacidad.html')

@app.route('/soporte')
def soporte():
    return render_template('soporte.html')

@app.route('/enviar-contacto-soporte', methods=['POST'])
def enviar_contacto_soporte():
    """Enviar mensaje de contacto desde soporte"""
    nombre = request.form.get('nombre', '').strip()
    email = request.form.get('email', '').strip()
    telefono = request.form.get('telefono', '').strip()
    asunto = request.form.get('asunto', 'Otro').strip()
    mensaje = request.form.get('mensaje', '').strip()
    
    if not nombre or not email or not mensaje:
        flash('Por favor completa los campos obligatorios', 'danger')
        return redirect(url_for('soporte'))
    
    try:
        # Crear mensaje para el equipo de soporte
        msg = Message(
            subject=f'Nuevo mensaje de soporte - {asunto}',
            sender=app.config.get('MAIL_DEFAULT_SENDER'),
            recipients=['soporte@a-space.store']
        )
        
        msg.body = f"""
Nuevo mensaje de contacto desde Centro de Soporte:

DATOS DEL CLIENTE:
- Nombre: {nombre}
- Email: {email}
- Teléfono: {telefono}
- Asunto: {asunto}

MENSAJE:
{mensaje}

---
Resonde a: {email}
Enviado: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        mail.send(msg)
        
        # Enviar confirmación al usuario
        msg_confirm = Message(
            subject='Hemos recibido tu mensaje - A-space Store',
            sender=app.config.get('MAIL_DEFAULT_SENDER'),
            recipients=[email]
        )
        
        msg_confirm.html = f"""
        <h2>Hola {nombre},</h2>
        <p>Gracias por contactar a A-space Store. Hemos recibido tu mensaje y nuestro equipo te responderá en las próximas 24 horas.</p>
        
        <p><strong>Detalles de tu solicitud:</strong></p>
        <ul>
        <li>Asunto: {asunto}</li>
        <li>Número de referencia: {datetime.utcnow().strftime('%Y%m%d%H%M%S')}</li>
        </ul>
        
        <p>Si tienes urgencia, puedes contactarnos por:</p>
        <ul>
        <li>Teléfono: +52 (555) 123-4567</li>
        <li>WhatsApp: +52 (555) 123-4567</li>
        <li>Horario: Lunes a Viernes, 9:00 - 18:00 hrs</li>
        </ul>
        
        <p>Saludos,<br>Equipo de A-space Store</p>
        """
        
        mail.send(msg_confirm)
        
        flash('Mensaje enviado exitosamente. Te responderemos pronto.', 'success')
        return redirect(url_for('soporte'))
        
    except Exception as e:
        logger.error(f'Error al enviar contacto de soporte: {str(e)}')
        flash('Hubo un error al enviar tu mensaje. Intenta más tarde.', 'danger')
        return redirect(url_for('soporte'))

@app.route('/cart')
@login_required
def cart():
    items = Carrito.query.filter_by(usuario_id=current_user.id).all()
    total_cart_price  = sum(item.producto.precio * item.cantidad for item in items)
    return render_template('cart.html', items=items, total_cart_price =total_cart_price )

@app.route('/agregar/<int:producto_id>', methods=['POST'])
@login_required
def add_to_cart(producto_id):
    try:
        producto = Producto.query.get_or_404(producto_id)
        
        if producto.stock <= 0:
            flash('Este producto no está disponible en este momento.', 'warning')
            return redirect(url_for('shop'))
        
        item_existente = Carrito.query.filter_by(producto_id=producto.id, usuario_id=current_user.id).first()
        if item_existente:
            item_existente.cantidad += 1
        else:
            item = Carrito(producto_id=producto.id, usuario_id=current_user.id, cantidad=1, imagen_url=producto.imagen_url)
            db.session.add(item)

        db.session.commit()
        flash({'nombre': producto.nombre, 'imagen_url': producto.imagen_url}, 'success_img')
        return redirect(url_for('shop'))
    except Exception as e:
        logger.error(f"Error al agregar al carrito: {str(e)}")
        flash('Error al agregar el producto al carrito.', 'danger')
        return redirect(url_for('shop'))

@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    # Buscar el item en el carrito del usuario actual
    item = Carrito.query.filter_by(id=item_id, usuario_id=current_user.id).first()

    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Producto eliminado del carrito.', 'success')
    else:
        flash('No se encontró el producto en tu carrito.', 'danger')

    return redirect(url_for('cart'))  # Reemplaza 'car

@app.route('/cart/update_quantity', methods=['POST'])
@login_required
def update_quantity():
    data = request.get_json()
    item_id = data.get('item_id')
    new_quantity = data.get('quantity')

    if not item_id or new_quantity is None:
        return jsonify({'success': False, 'message': 'Faltan datos'}), 400

    try:
        new_quantity = int(new_quantity)
        if new_quantity < 1:
            new_quantity = 1
    except ValueError:
        return jsonify({'success': False, 'message': 'Cantidad inválida'}), 400

    item = Carrito.query.filter_by(id=item_id, usuario_id=current_user.id).first()
    if not item:
        return jsonify({'success': False, 'message': 'Producto no encontrado en el carrito'}), 404

    item.cantidad = new_quantity
    db.session.commit()

    total_item = float(item.producto.precio) * new_quantity

    return jsonify({
        'success': True,
        'new_quantity': new_quantity,
        'total_item': total_item
    })

@app.route('/checkout')
@login_required
def checkout():
    # Obtener los items del carrito
    carrito_items = Carrito.query.filter_by(usuario_id=current_user.id).all()
    if not carrito_items:
        return redirect(url_for('shop'))
    # Calcular el total
    total = sum(item.cantidad * item.producto.precio for item in carrito_items)
    
    # Obtener las direcciones del usuario
    direcciones = DireccionEnvio.query.filter_by(usuario_id=current_user.id).all()
    
    # Determinar la dirección seleccionada
    if direcciones:
        direccion_seleccionada_id = direcciones[0].id
    else:
        direccion_seleccionada_id = None  # O 'nueva' si quieres abrir el formulario para nueva dirección

        
    return render_template(
        'checkout.html',
        carrito=carrito_items,
        total=total,
        direcciones=direcciones,
        direccion_seleccionada_id=direccion_seleccionada_id,
        mostrar_formulario_nueva_direccion=not direcciones,
        estados=ESTADOS_MEXICO
    )

@app.route('/direccion', methods=['POST'])
@login_required
def agregar_direccion():
    data = request.get_json() if request.is_json else request.form

    colonia = data.get('colonia')
    estado = data.get('estado')
    codigo_postal = data.get('codigo_postal')
    direccion_texto = data.get('direccion')
    ciudad = data.get('ciudad')
    telefono = data.get('telefono')
    referencias = data.get('referencias')
    source = data.get('source')  # <-- Saber de dónde vino

    # Validación de campos obligatorios
    if not all([colonia, estado, codigo_postal, direccion_texto, ciudad, telefono]):
        if request.is_json:
            return jsonify({'error': 'Faltan datos obligatorios.'}), 400
        else:
            flash('Faltan datos obligatorios.', 'danger')
            return redirect(url_for(source if source in ['checkout', 'profile'] else 'profile'))

    if not validar_codigo_postal_mexico(codigo_postal, estado, colonia):
        if request.is_json:
            return jsonify({'error': 'Código postal, estado o colonia no coinciden.'}), 400
        else:
            flash('Código postal, estado o colonia no coinciden.', 'danger')
            return redirect(url_for(source if source in ['checkout', 'profile'] else 'profile'))

    direccion = DireccionEnvio(
        usuario_id=current_user.id,
        direccion=direccion_texto,
        colonia=colonia,
        ciudad=ciudad,
        estado=estado,
        codigo_postal=codigo_postal,
        telefono=telefono,
        referencias=referencias
    )
    db.session.add(direccion)
    db.session.commit()

    if request.is_json:
        return jsonify({'mensaje': 'Dirección guardada con éxito.'}), 201
    else:
        flash('Dirección guardada con éxito.', 'success')
        return redirect(url_for(source if source in ['checkout', 'profile'] else 'profile'))

@app.route('/direcciones', methods=['GET'])
@login_required
def obtener_direcciones():
    direcciones = DireccionEnvio.query.filter_by(usuario_id=current_user.id).all()
    resultado = [{
        'id': d.id,
        'direccion': d.direccion,
        'colonia': d.colonia,
        'ciudad': d.ciudad,
        'estado': d.estado,
        'codigo_postal': d.codigo_postal,
        'telefono': d.telefono,
        'referencias': d.referencias
    } for d in direcciones]
    return jsonify(resultado)

@app.route('/direccion/<int:direccion_id>', methods=['DELETE'])
@login_required
def eliminar_direccion(direccion_id):
    direccion = DireccionEnvio.query.filter_by(id=direccion_id, usuario_id=current_user.id).first_or_404()
    db.session.delete(direccion)
    db.session.commit()
    return jsonify({'mensaje': 'Dirección eliminada.'})

@app.route('/procesar_pago', methods=['POST'])
@login_required
def procesar_pago():
    try:
        metodo = request.form.get('metodo_pago', 'tarjeta').strip().lower()
        direccion_id = request.form.get('direccion_envio')
        observaciones = request.form.get('observaciones', '').strip()

        if metodo not in ['tarjeta', 'paypal']:
            flash("Método de pago no válido.", "danger")
            return redirect(url_for('checkout'))

        direccion = DireccionEnvio.query.filter_by(id=direccion_id, usuario_id=current_user.id).first()
        if not direccion:
            flash("Debes seleccionar una dirección de envío válida.", "danger")
            return redirect(url_for('checkout'))

        carrito_items = Carrito.query.filter_by(usuario_id=current_user.id).all()
        if not carrito_items:
            flash("Tu carrito está vacío.", "warning")
            return redirect(url_for('checkout'))

        # Validar stock antes de crear pedido
        for item in carrito_items:
            if item.producto.stock < item.cantidad:
                flash(f"No hay suficiente stock para: {item.producto.nombre}", "danger")
                return redirect(url_for('checkout'))

        total = sum(item.cantidad * item.producto.precio for item in carrito_items)

        nuevo_pedido = Pedido(
            usuario_id=current_user.id,
            direccion_envio_id=direccion_id,
            metodo_pago=metodo,
            fecha=datetime.utcnow(),
            estado='pendiente',
            total=total
        )
        db.session.add(nuevo_pedido)
        db.session.flush()

        envio = Envio(
            pedido_id=nuevo_pedido.id,
            usuario_id=current_user.id,
            direccion_envio_id=direccion_id,
            estado='pendiente',
            numero_rastreo='pendiente',
            observaciones=observaciones
        )
        db.session.add(envio)

        for item in carrito_items:
            detalle = PedidoDetalle(
                compra_id=nuevo_pedido.id,
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio
            )
            db.session.add(detalle)

        db.session.commit()
        logger.info(f"Pedido #{nuevo_pedido.id} creado para usuario {current_user.id}")

        if metodo == 'paypal':
            return redirect(url_for('pagar_paypal', pedido_id=nuevo_pedido.id))

        # Stripe Checkout para tarjeta
        if not stripe.api_key:
            flash("Pago con tarjeta no disponible. Falta configurar Stripe.", "danger")
            return redirect(url_for('checkout'))

        line_items = []
        for item in carrito_items:
            line_items.append({
                'price_data': {
                    'currency': app.config.get('STRIPE_CURRENCY', 'mxn'),
                    'product_data': {'name': item.producto.nombre},
                    'unit_amount': int(round(float(item.producto.precio) * 100)),
                },
                'quantity': item.cantidad,
            })

        session = stripe.checkout.Session.create(
            mode='payment',
            payment_method_types=['card'],
            customer_email=current_user.email,
            line_items=line_items,
            metadata={'pedido_id': nuevo_pedido.id, 'usuario_id': current_user.id},
            success_url=url_for('stripe_success', pedido_id=nuevo_pedido.id, _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('stripe_cancel', pedido_id=nuevo_pedido.id, _external=True)
        )

        return redirect(session.url, code=303)

    except Exception as e:
        logger.error(f"Error en procesar_pago: {str(e)}")
        db.session.rollback()
        flash("Ocurrió un error al procesar tu pedido. Por favor intenta de nuevo.", "danger")
        return redirect(url_for('checkout'))

@app.route('/pagar_paypal/<int:pedido_id>', methods=['GET'])
@login_required
def pagar_paypal(pedido_id):
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        if pedido.usuario_id != current_user.id:
            abort(403)

        logger.info(f"Iniciando pago PayPal para pedido {pedido_id}, total: {pedido.total}")

        request_order = OrdersCreateRequest()
        request_order.prefer("return=representation")
        request_order.request_body({
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "MXN",
                    "value": f"{pedido.total:.2f}"
                },
                "description": f"Pedido #{pedido.id}"
            }],
            "application_context": {
                "return_url": url_for('paypal_success', pedido_id=pedido.id, _external=True),
                "cancel_url": url_for('paypal_cancel', pedido_id=pedido.id, _external=True)
            }
        })

        response = paypal_client.client.execute(request_order)
        logger.info(f"PayPal ORDER STATUS: {response.result.status}, ID: {response.result.id}")
        
        for link in response.result.links:
            if link.rel == "approve":
                return redirect(link.href)
        
        flash("Error al conectar con PayPal: No se encontró enlace de aprobación", "danger")
        return redirect(url_for('checkout'))
        
    except Exception as e:
        logger.error(f"Error PayPal: {str(e)}")
        flash("Error al conectar con PayPal. Por favor intenta de nuevo.", "danger")
        return redirect(url_for('checkout'))

@app.route('/paypal/success/<int:pedido_id>')
@login_required
def paypal_success(pedido_id):
    token = request.args.get('token')  # Token de PayPal
    capture_request = OrdersCaptureRequest(token)
    capture_request.prefer("return=representation")
    capture_response = paypal_client.client.execute(capture_request)

    # Aquí puedes verificar estado y datos del comprador
    status = capture_response.result.status
    if status == "COMPLETED":
        pedido = Pedido.query.get_or_404(pedido_id)
        pedido.estado = 'pagado'
        db.session.commit()
        flash("¡Pago completado con éxito mediante PayPal!", "success")
    else:
        flash("El pago no se completó correctamente.", "warning")

    return redirect(url_for('confirmacion'))


@app.route('/stripe/success/<int:pedido_id>')
@login_required
def stripe_success(pedido_id):
    session_id = request.args.get('session_id')
    if not session_id:
        flash('Pago inválido: falta session_id.', 'danger')
        return redirect(url_for('checkout'))

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            pedido = Pedido.query.get_or_404(pedido_id)
            pedido.estado = 'pagado'

            detalles = PedidoDetalle.query.filter_by(compra_id=pedido.id).all()
            for det in detalles:
                producto = db.session.get(Producto, det.producto_id)
                if producto and producto.stock >= det.cantidad:
                    producto.stock -= det.cantidad

            Carrito.query.filter_by(usuario_id=current_user.id).delete()
            db.session.commit()
            flash('Pago completado con tarjeta.', 'success')
            return redirect(url_for('confirmacion'))

        flash('No se pudo confirmar el pago.', 'warning')
        return redirect(url_for('checkout'))
    except Exception as e:
        logger.error(f"Error en stripe_success: {str(e)}")
        flash('Ocurrió un problema al validar el pago.', 'danger')
        return redirect(url_for('checkout'))


@app.route('/stripe/cancel/<int:pedido_id>')
@login_required
def stripe_cancel(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    pedido.estado = 'cancelado'
    db.session.commit()
    flash('Pago cancelado. Puedes intentar nuevamente.', 'info')
    return redirect(url_for('checkout'))

@app.route('/paypal/cancel/<int:pedido_id>')
@login_required
def paypal_cancel(pedido_id):
    flash("El pago con PayPal fue cancelado.", "warning")
    return redirect(url_for('checkout'))


@app.route('/subir_comprobante/<int:pedido_id>', methods=['GET', 'POST'])
@login_required
def subir_comprobante(pedido_id):
    try:
        pedido = Pedido.query.get_or_404(pedido_id)

        if pedido.usuario_id != current_user.id:
            flash("No tienes permiso para subir comprobantes para este pedido.", "danger")
            return redirect(url_for('orders'))

        if request.method == 'POST':
            archivo = request.files.get('archivo')
            if archivo and allowed_file(archivo.filename):
                nombre_archivo = f"{uuid.uuid4().hex}_{secure_filename(archivo.filename)}"
                ruta = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)

                # Crea la carpeta si no existe
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

                archivo.save(ruta)

                comprobante = ComprobanteTransferencia(
                    pedido_id=pedido.id,
                    archivo=nombre_archivo
                )
                db.session.add(comprobante)

                # Cambiar estado del pedido a "Pagado"
                pedido.estado = "Pagado"

                db.session.commit()
                logger.info(f"Comprobante subido para pedido {pedido_id}")

                flash("Comprobante enviado correctamente.", "success")
                return redirect(url_for('orders'))
            else:
                flash("Archivo inválido. Solo se permiten imágenes y PDF.", "warning")
                return redirect(url_for('subir_comprobante', pedido_id=pedido_id))

        return render_template('subir_comprobante.html', pedido=pedido)
    
    except Exception as e:
        logger.error(f"Error al subir comprobante: {str(e)}")
        flash('Error al procesar el comprobante.', 'danger')
        return redirect(url_for('orders'))


@app.route('/confirmacion')
@login_required
def confirmacion():
    pedido = Pedido.query.filter_by(usuario_id=current_user.id).order_by(Pedido.fecha.desc()).first()
    envio = Envio.query.filter_by(pedido_id=pedido.id).first() if pedido else None
    return render_template('thankyou.html', pedido=pedido, envio=envio)

@app.route('/orders/<int:envio_id>/actualizar_estado', methods=['POST'])
@login_required
@admin_required
def actualizar_estado_envio(envio_id):
    if not current_user.is_admin:
        return "No autorizado", 403

    nuevo_estado = request.form.get('estado')
    envio = Envio.query.get_or_404(envio_id)

    if nuevo_estado not in ['pendiente', 'procesado', 'aceptado', 'enviado', 'entregado', 'cancelado']:
        flash('Estado inválido', 'danger')
        return redirect(url_for('admin_panel'))

    envio.estado = nuevo_estado
    db.session.commit()

    flash(f'Estado de envío actualizado a {nuevo_estado}', 'success')
    return redirect(url_for('admin_panel'))

@app.route("/user/orders")
@login_required
def orders():
    envios = Envio.query.filter_by(usuario_id=current_user.id).all()
    return render_template("user/orders.html", envios=envios)

@app.route('/rastreo')
@login_required
def rastreo():
    envio_id = request.args.get('envio_id')
    envio = db.session.get(Envio, envio_id)
    if not envio:
        flash('Envío no encontrado', 'danger')
        return redirect(url_for('orders'))

    # Aquí podrías pasar también el rastreo de Skydropx
    return render_template('user/rastreo.html', envio=envio)

@app.route("/api/rastreo/<string:tracking_number>")
@login_required
def api_rastreo(tracking_number):
    postal_key = current_app.config.get('POSTAL_NINJA_API_KEY')
    if not postal_key:
        logger.error('POSTAL_NINJA_API_KEY no configurada')
        return jsonify({"status": "error", "message": "Integración de rastreo no configurada"}), 503

    headers = {
        "Authorization": f"Bearer {postal_key}",
        "Content-Type": "application/json"
    }

    url = f"https://api.postal.ninja/v1/trackings/{tracking_number}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return jsonify({"status": "ok", "data": data})
    except requests.RequestException as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "No se pudo rastrear el paquete"}), 500

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/enviar_correo', methods=['POST'])
def enviar_correo():
    try:
        fname = request.form.get('fname', '').strip()
        lname = request.form.get('lname', '').strip()
        email = request.form.get('email', '').strip()
        mensaje = request.form.get('message', '').strip()

        # Validar campos
        if not all([fname, lname, email, mensaje]):
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('contact'))

        # Construir el mensaje
        cuerpo = f"""
        Nombre: {fname} {lname}
        Correo: {email}
        
        Mensaje:
        {mensaje}
        """

        msg = Message(
            subject="Nuevo mensaje desde el formulario de contacto",
            recipients=['ipiproyecto603@gmail.com'],
            body=cuerpo
        )

        mail.send(msg)
        logger.info(f"Correo de contacto enviado por {email}")
        flash("Mensaje enviado con éxito", "success")
    except Exception as e:
        logger.error(f"Error al enviar correo de contacto: {str(e)}")
        flash(f"Error al enviar el mensaje. Por favor intenta de nuevo.", "danger")

    return redirect(url_for('contact'))


@app.route('/shop')
def shop():
    try:
        categoria_id = request.args.get('categoria', type=int)

        if categoria_id:
            productos = Producto.query.filter_by(categoria_id=categoria_id).all()
        else:
            productos = Producto.query.all()

        categorias = Categoria.query.all()

        return render_template('shop.html', productos=productos, categorias=categorias)
    except Exception as e:
        logger.error(f"Error al cargar la tienda: {str(e)}")
        flash('No se pudo cargar la tienda. Verifica la conexión a la base de datos.', 'danger')
        return render_template('shop.html', productos=[], categorias=[])

@app.route("/user/profile")
@login_required
def profile():
    usuario = current_user
    direccion = DireccionEnvio.query.filter_by(usuario_id=usuario.id).first()
    return render_template("user/profile.html", usuario=usuario, direccion=direccion)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():

    current_user.username = request.form['username']
    current_user.nombre = request.form['nombre']
    current_user.apellido = request.form['apellido']
    current_user.email = request.form['email']
    db.session.commit()
    flash('Perfil actualizado correctamente')
    return redirect(url_for('profile'))

@app.route('/update_profile_adress', methods=['POST'])
@login_required
def update_profile_adress():
    
    direccion = DireccionEnvio.query.filter_by(usuario_id=current_user.id).first()
    if not direccion:
        direccion = DireccionEnvio(usuario_id=current_user.id)
        db.session.add(direccion)
        
    direccion.direccion = request.form.get('direccion', direccion.direccion)
    direccion.ciudad = request.form.get('ciudad', direccion.ciudad)
    direccion.pais = request.form.get('pais', direccion.pais)
    direccion.codigo_postal = request.form.get('codigo_postal', direccion.codigo_postal)
    direccion.telefono = request.form.get('telefono', direccion.telefono)
    db.session.commit()
    flash('Perfil actualizado correctamente')
    return redirect(url_for('profile'))


@app.route("/user/purchases")
def purchases():
    pedidos = Pedido.query.options(
        db.joinedload(Pedido.detalles).joinedload(PedidoDetalle.producto)
    ).all()
    return render_template("user/purcharses.html", pedidos=pedidos)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=port)

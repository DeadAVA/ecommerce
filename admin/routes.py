# admin/routes.py
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from utils.decorators import admin_required
from admin import admin_bp  # importar el blueprint# Formulario para agregar/editar categorías
from werkzeug.utils import secure_filename
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from admin.log import log_activity
import os

# 👇 IMPORTA LOS MODELOS
from models.models import db, Usuario, Producto, Pedido, Envio, Categoria, DireccionEnvio, ActivityLog, PedidoDetalle, ComprobanteTransferencia
from models.forms import CategoriaForm, UsuarioForm, DireccionForm  # Formulario para agregar/editar categorías

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    log_activity(user_id=current_user.id, action="Accedió al panel de control")
    # Usuarios registrados
    total_usuarios = Usuario.query.count()

    # Total de ventas (solo pedidos confirmados)
    total_ventas = db.session.query(func.sum(Pedido.total)).filter(Pedido.estado == 'pagado').scalar() or 0

    # Ganancias estimadas (ej. 30%)
    ganancias = total_ventas * 0.30

    # Productos en inventario
    inventario_total = db.session.query(func.sum(Producto.stock)).scalar() or 0
    productos = Producto.query.all()

    # Pedidos por estado
    pedidos_pendientes_comprobar = Pedido.query.filter_by(estado='pendiente').all()
    pedidos_pendientes_enviar = Envio.query.filter_by(estado='pendiente').all()

    # Ventas por mes (últimos 6 meses)
    hoy = datetime.today()
    ventas_por_mes = []
    for i in range(5, -1, -1):  # últimos 6 meses
        inicio = (hoy.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        fin = (inicio + timedelta(days=32)).replace(day=1)
        total_mes = db.session.query(func.sum(Pedido.total)).filter(
            Pedido.estado == 'pagado',
            Pedido.fecha >= inicio,
            Pedido.fecha < fin
        ).scalar() or 0
        ventas_por_mes.append({
            'mes': inicio.strftime('%b %Y'),
            'total': float(total_mes)
        })

    return render_template('admin/dashboard.html',
                       total_usuarios=total_usuarios,
                       total_ventas=total_ventas,
                       ganancias=ganancias,
                       inventario_total=inventario_total,
                       pedidos_pendientes_comprobar=pedidos_pendientes_comprobar,
                       pedidos_pendientes_enviar=pedidos_pendientes_enviar,
                       ventas_por_mes=ventas_por_mes,
                       productos=productos)  # 👈 Agregado


######################################################################################################################
#                                                                                                                    #
#                                                    CATEGORIAS                                                      #
#                                                                                                                    # 
######################################################################################################################
@admin_bp.route('/categorias')
@login_required
@admin_required
def categorias():
    log_activity(user_id=current_user.id, action="Accedió a la sección de categorías")
    page = request.args.get('page', 1, type=int)
    per_page = 5
    categorias_paginated = Categoria.query.order_by(Categoria.id.desc()).paginate(page=page, per_page=per_page)
    form = CategoriaForm()
    return render_template('admin/categorias.html', categorias=categorias_paginated, form=form)

@admin_bp.route('/categorias/nueva', methods=['POST'])
@login_required
@admin_required
def nueva_categoria():
    nombre = request.form.get('nombre')
    if nombre:
        nueva = Categoria(nombre=nombre)
        db.session.add(nueva)
        db.session.commit()
        log_activity(user_id=current_user.id, action=f"Creó categoría '{nombre}' (ID: {nueva.id})")
        flash('Categoría agregada exitosamente', 'success')
    return redirect(url_for('admin.categorias'))

@admin_bp.route('/categorias/editar/<int:id>', methods=['POST'])
@login_required
@admin_required
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    nombre = request.form.get('nombre')
    if nombre:
        categoria.nombre = nombre
        db.session.commit()
        log_activity(user_id=current_user.id, action=f"Editó categoría ID {id} con nuevo nombre '{nombre}'")
        flash('Categoría actualizada correctamente', 'success')
    return redirect(url_for('admin.categorias'))

@admin_bp.route('/categorias/eliminar/<int:id>')
@login_required
@admin_required
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    log_activity(user_id=current_user.id, action=f"Eliminó categoría ID {id}")
    flash('Categoría eliminada', 'info')
    return redirect(url_for('admin.categorias'))

######################################################################################################################
#                                                                                                                    #
#                                                    PRODUCTOS                                                       #
#                                                                                                                    # 
######################################################################################################################

@admin_bp.route('/productos')
@login_required
@admin_required
def productos():
    log_activity(user_id=current_user.id, action="Accedió a la sección de productos")
    page = request.args.get('page', 1, type=int)
    per_page = 5
    productos_paginated = Producto.query.order_by(Producto.id.desc()).paginate(page=page, per_page=per_page)
    categorias = Categoria.query.all()
    return render_template('admin/productos.html', productos=productos_paginated, categorias=categorias)


@admin_bp.route('/productos/nuevo', methods=['POST'])
@login_required
@admin_required
def nuevo_producto():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    categoria_id = request.form.get('categoria_id')

    imagen = request.files.get('imagen')
    imagen_url = None
    if imagen and imagen.filename != '':
        filename = secure_filename(imagen.filename)
        imagen_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        imagen.save(imagen_path)
        imagen_url = f'/static/comprobantes/{filename}'

    producto = Producto(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        categoria_id=categoria_id or None,
        imagen_url=imagen_url
    )
    db.session.add(producto)
    db.session.commit()
    
    log_activity(user_id=current_user.id, action=f"Creó producto {producto.nombre} (ID: {producto.id})")
    flash('Producto agregado exitosamente', 'success')
    return redirect(url_for('admin.productos'))


@admin_bp.route('/productos/editar/<int:id>', methods=['POST'])
@login_required
@admin_required
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    categoria_id = request.form.get('categoria_id')

    imagen = request.files.get('imagen')
    if imagen and imagen.filename != '':
        filename = secure_filename(imagen.filename)
        imagen_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        imagen.save(imagen_path)
        producto.imagen_url = f'/static/comprobantes/{filename}'

    producto.nombre = nombre
    producto.descripcion = descripcion
    producto.precio = precio
    producto.categoria_id = categoria_id or None

    db.session.commit()
    log_activity(user_id=current_user.id, action=f"Editó producto '{producto.nombre}' (ID: {id})")
    flash('Producto actualizado correctamente', 'success')
    return redirect(url_for('admin.productos'))


@admin_bp.route('/productos/eliminar/<int:id>', methods=['POST'])  # 👈 permite POST
@login_required
@admin_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    nombre = producto.nombre
    db.session.delete(producto)
    db.session.commit()
    log_activity(user_id=current_user.id, action=f"Eliminó producto '{nombre}' (ID: {id})")
    flash('Producto eliminado correctamente', 'info')
    return redirect(url_for('admin.productos'))

######################################################################################################################
#                                                                                                                    #
#                                                    COMPRAS_USUARIO                                                 #
#                                                                                                                    # 
######################################################################################################################


@admin_bp.route('/Compras_usuario')
@login_required
@admin_required
def Compras_usuario():

    return

######################################################################################################################
#                                                                                                                    #
#                                                    COMPROBANTES                                                    #
#                                                                                                                    # 
######################################################################################################################

@admin_bp.route('/comprobantes')
@login_required
@admin_required
def comprobantes():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    comprobantes = ComprobanteTransferencia.query.order_by(desc(ComprobanteTransferencia.fecha_subida)).paginate(page=page, per_page=per_page)
    pedidos = {p.id: p for p in Pedido.query.all()}
    return render_template('admin/comprobantes.html', comprobantes=comprobantes, pedidos=pedidos)

@admin_bp.route('/comprobantes/editar/<int:id>', methods=['POST'])
@login_required
@admin_required
def editar_comprobante(id):
    comprobante = ComprobanteTransferencia.query.get_or_404(id)
    verificado = request.form.get('verificado') == 'true'
    comprobante.verificado = verificado
    db.session.commit()
    flash('Comprobante actualizado correctamente.', 'success')
    return redirect(url_for('admin.comprobantes'))

@admin_bp.route('/comprobantes/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_comprobante(id):
    comprobante = ComprobanteTransferencia.query.get_or_404(id)
    db.session.delete(comprobante)
    db.session.commit()
    flash('Comprobante eliminado.', 'success')
    return redirect(url_for('admin.comprobantes'))





@admin_bp.route('/direcciones', methods=['GET', 'POST'])
@login_required
@admin_required
def direcciones():
    form = DireccionForm()
    if form.validate_on_submit():
        if request.form.get('editar_id'):  # Editar
            log_activity(user_id=current_user.id, action=f"Editó dirección ID {request.form.get('editar_id')}")
            direccion = DireccionEnvio.query.get(int(request.form.get('editar_id')))
            if direccion:
                form.populate_obj(direccion)
        else:  # Crear
            log_activity(user_id=current_user.id, action="Creó una nueva dirección")
            direccion = DireccionEnvio()
            form.populate_obj(direccion)
            db.session.add(direccion)
        db.session.commit()
        log_activity(user_id=current_user.id, action="Accedió a la sección de direcciones")
        flash('Dirección guardada correctamente', 'success')
        return redirect(url_for('admin.direcciones'))

    page = request.args.get('page', 1, type=int)
    pagination = DireccionEnvio.query.order_by(DireccionEnvio.id.desc()).paginate(page=page, per_page=10)
    direcciones = pagination.items
    return render_template('admin/direcciones.html', form=form, direcciones=direcciones, pagination=pagination)

@admin_bp.route('/direcciones/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_direccion(id):
    direccion = DireccionEnvio.query.get_or_404(id)
    db.session.delete(direccion)
    db.session.commit()
    log_activity(user_id=current_user.id, action=f"Eliminó dirección ID {id}")
    flash('Dirección eliminada correctamente', 'success')
    return redirect(url_for('admin.direcciones'))



######################################################################################################################
#                                                                                                                    #
#                                                      ENVIOS                                                        #
#                                                                                                                    # 
######################################################################################################################
    
@admin_bp.route('/envios')
@login_required
@admin_required
def listar_envios():
    log_activity(user_id=current_user.id, action="Accedió a la sección de envíos")
    page = request.args.get('page', 1, type=int)
    per_page = 10
    envios = Envio.query.order_by(Envio.fecha_creacion.desc()).paginate(page=page, per_page=per_page)
    direcciones = DireccionEnvio.query.all()  # <-- Asegúrate de tener este modelo
    return render_template('admin/envios.html', envios=envios, direcciones=direcciones)

@admin_bp.route('/envios/editar/<int:id>', methods=['POST'])
@login_required
@admin_required
def editar_envio(id):
    envio = Envio.query.get_or_404(id)
    envio.estado = request.form.get('estado')
    envio.numero_rastreo = request.form.get('numero_rastreo')
    envio.observaciones = request.form.get('observaciones')
    envio.direccion_envio_id = request.form.get('direccion_envio_id')  # <-- Asegúrate de guardarlo
    db.session.commit()
    log_activity(user_id=current_user.id, action=f"Editó envío ID {id}")
    flash('Envío actualizado correctamente', 'success')
    return redirect(url_for('admin.listar_envios'))



@admin_bp.route('/envios/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_envio(id):
    envio = Envio.query.get_or_404(id)
    db.session.delete(envio)
    db.session.commit()
    log_activity(user_id=current_user.id, action=f"Eliminó envío ID {id}")
    flash('Envío eliminado correctamente', 'info')
    return redirect(url_for('admin.listar_envios'))


######################################################################################################################
#                                                                                                                    #
#                                                    LISTA_USUARIOS                                                  #
#                                                                                                                    # 
######################################################################################################################

@admin_bp.route('/usuarios')
@login_required
@admin_required
def usuarios():
    log_activity(user_id=current_user.id, action="Accedió a la sección de usuarios")
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Usuario.query.order_by(Usuario.id.desc()).paginate(page=page, per_page=per_page)
    usuarios = pagination.items
    form = UsuarioForm()  # formulario vacío para el modal
    return render_template('admin/usuarios.html', usuarios=usuarios, pagination=pagination, form=form)



# Crear nuevo usuario
@admin_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def nuevo_usuario():
    form = UsuarioForm()
    if form.validate_on_submit():
        user = Usuario(
            username=form.username.data,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            admin=form.admin.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        log_activity(user_id=current_user.id, action=f"Creó usuario '{user.username}' (ID: {user.id})")
        flash('Usuario creado correctamente', 'success')
        return redirect(url_for('admin.usuarios'))
    return render_template('admin/usuarios/form.html', form=form, titulo='Nuevo Usuario')

@admin_bp.route('/usuarios/editar', methods=['POST'])
@login_required
@admin_required
def editar_usuario():
    form = UsuarioForm()
    if form.validate_on_submit():
        user = Usuario.query.get_or_404(request.form.get('editar_id'))
        user.username = form.username.data
        user.nombre = form.nombre.data
        user.apellido = form.apellido.data
        user.email = form.email.data
        user.admin = form.admin.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        log_activity(user_id=current_user.id, action=f"Editó usuario ID {user.id}")
        flash('Usuario actualizado correctamente', 'success')
    else:
        flash('Error en el formulario', 'danger')
    return redirect(url_for('admin.usuarios'))


# Eliminar usuario
@admin_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_usuario(id):
    user = Usuario.query.get_or_404(id)
    username = user.username
    db.session.delete(user)
    db.session.commit()
    log_activity(user_id=current_user.id, action=f"Eliminó usuario '{username}' (ID: {id})")
    flash('Usuario eliminado correctamente', 'success')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/activity-log')
@login_required
@admin_required
def activity_log():
    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(100).all()
    return render_template('admin/activity_log.html', logs=logs)

@admin_bp.route('/detalles_compra')
@login_required
@admin_required
def detalles_compra():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    detalles = PedidoDetalle.query.paginate(page=page, per_page=per_page)

    compras = Pedido.query.all()
    productos = Producto.query.all()

    edit_id = request.args.get('edit_id', type=int)
    detalle_editar = PedidoDetalle.query.get(edit_id) if edit_id else None

    return render_template(
        'admin/detalles_compra.html',
        detalles=detalles,
        compras=compras,
        productos=productos,
        detalle_editar=detalle_editar
    )


@admin_bp.route('/detalles_compra/crear', methods=['POST'])
@login_required
@admin_required
def crear_detalle_compra():
    detalle = PedidoDetalle(
        compra_id=request.form['compra_id'],
        producto_id=request.form['producto_id'],
        cantidad=int(request.form['cantidad']),
        precio_unitario=float(request.form['precio_unitario'])
    )
    db.session.add(detalle)
    db.session.commit()
    flash('Detalle creado correctamente.')
    return redirect(url_for('admin.detalles_compra'))


@admin_bp.route('/detalles_compra/editar/<int:id>', methods=['POST'])
@login_required
@admin_required
def editar_detalle_compra(id):
    detalle = PedidoDetalle.query.get_or_404(id)
    detalle.compra_id = request.form['compra_id']
    detalle.producto_id = request.form['producto_id']
    detalle.cantidad = int(request.form['cantidad'])
    detalle.precio_unitario = float(request.form['precio_unitario'])
    db.session.commit()
    flash('Detalle editado correctamente.')
    return redirect(url_for('admin.detalles_compra'))


@admin_bp.route('/detalles_compra/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_detalle_compra(id):
    detalle = PedidoDetalle.query.get_or_404(id)
    db.session.delete(detalle)
    db.session.commit()
    flash('Detalle eliminado correctamente.')
    return redirect(url_for('admin.detalles_compra'))

# 🛠️ CAMBIOS A LA BASE DE DATOS

## Cambios Realizados para Producción

### 1. **Mejoras Estructurales**
- ✅ Índices estratégicos en columnas frecuentemente consultadas (email, usuario_id, estado, fecha)
- ✅ Claves foráneas con `ON DELETE CASCADE` para eliminar datos huérfanos automáticamente
- ✅ Charset UTF-8MB4 para soporte completo de emojis y caracteres especiales
- ✅ Timestamps automáticos (created_at, updated_at) en todas las tablas
- ✅ Cambio a INT UNSIGNED para IDs (mejor rendimiento)

### 2. **Nuevas Columnas**
- **compras**: `stripe_session_id`, `paypal_transaction_id`, `notas` para tracking de pagos
- **productos**: `activo` (BOOLEAN) para hacer soft-delete sin perder datos
- **categorias**: `descripcion` para SEO y listados
- **direccion_envio**: `es_principal` para marcar dirección por defecto
- **usuarios**: `created_at`, `updated_at` para auditoría
- **activity_logs**: `extra_info` (JSON) para datos complejos

### 3. **Eliminar Comprobantes**
- Tabla `comprobantes` removida (ya no se necesita con Stripe/PayPal)
- El estado del pedido ahora es: `pendiente` → `pagado` → `procesando` → `enviado` → `entregado`

### 4. **Cambios en Métodos de Pago**
- `metodo_pago` default: `'tarjeta'` (Stripe)
- Se elimina `'transferencia'` como opción
- Se mantiene `'paypal'` como alternativa

---

## Archivo SQL Actualizado

El nuevo archivo **`ecommerce_produccion.sql`** incluye:

✅ Estructura optimizada  
✅ Índices para queries rápidas  
✅ Datos de ejemplo  
✅ Usuario admin predeterminado  

### Para usar en tu VPS:

```bash
# Opción 1: Importar completo
mysql -u root -p < ecommerce_produccion.sql

# Opción 2: Importar a base existente
mysql -u usuario -p ecommerce < ecommerce_produccion.sql

# Opción 3: Via phpmyadmin
# Subir el archivo directamente
```

---

## Modelo Entidad-Relación

```
USUARIOS (id, username, email, ...)
    ├── CARRITO (usuario_id → productos)
    ├── DIRECCION_ENVIO (usuario_id)
    │   └── COMPRAS (direccion_id)
    │       ├── DETALLE_COMPRA (productos)
    │       └── ENVIOS
    └── ACTIVITY_LOGS
```

---

## Migrar Datos Antiguos (Si es necesario)

Si tienes datos en la BD antigua que quieras conservar:

```sql
-- Respaldar datos viejos
CREATE TABLE usuarios_backup AS SELECT * FROM usuarios;
CREATE TABLE productos_backup AS SELECT * FROM productos;

-- Limpiar y migrar
TRUNCATE TABLE usuarios;
INSERT INTO usuarios SELECT * FROM usuarios_backup;
```

---

**La nueva estructura está lista para escala y producción.** ✨

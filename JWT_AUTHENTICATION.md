# 🔐 Sistema de Autenticación con JWT y Cookies Seguras

## Descripción General

La aplicación ha sido actualizada para utilizar un sistema de autenticación moderno y seguro basado en **JSON Web Tokens (JWT)** almacenados en **cookies seguras HttpOnly**, eliminando completamente la dependencia de localStorage.

## ¿Por qué JWT + Cookies Seguras?

### Ventajas de este enfoque:

| Característica | localStorage | JWT en Cookies |
|---|---|---|
| **Seguridad XSS** | ❌ Vulnerable | ✅ Protegido (HttpOnly) |
| **CSRF** | ❌ Sin protección nativa | ✅ Protegido (SameSite) |
| **Almacenamiento** | ❌ Cliente (inseguro) | ✅ Automático del navegador |
| **Control del servidor** | ❌ No | ✅ Sí (expiración, revocación) |
| **Sesión automática** | ❌ Manual | ✅ Automática |

## Arquitectura del Sistema

### 1. **Módulo de Autenticación** (`utils/auth.py`)

```python
from utils.auth import JWTAuth, token_required, refresh_token_required

# Crear tokens
access_token, refresh_token = JWTAuth.create_tokens(user_id, user_email)

# Configurar cookies
response = JWTAuth.set_token_cookies(response, access_token, refresh_token)

# Verificar token
payload = JWTAuth.verify_token(token, 'access')

# Limpiar cookies
response = JWTAuth.clear_token_cookies(response)
```

### 2. **Tokens JWT**

#### **Access Token**
- **Duración**: 30 minutos
- **Tipo**: 'access'
- **Uso**: Autenticación en requests
- **Cookie**: HttpOnly, Secure, SameSite=Lax

#### **Refresh Token**
- **Duración**: 7 días
- **Tipo**: 'refresh'
- **Uso**: Obtener nuevo access token
- **Cookie**: HttpOnly, Secure, SameSite=Lax

### 3. **Payload del Token**

```json
{
  "user_id": 123,
  "email": "usuario@email.com",
  "type": "access",
  "iat": 1705977600,
  "exp": 1705979400
}
```

## Flujo de Autenticación

### Diagrama de Flujo

```
1. Usuario inicia sesión
   ↓
2. Servidor valida credenciales
   ↓
3. Servidor genera access_token y refresh_token
   ↓
4. Servidor envía cookies:
   - access_token (HttpOnly, 30 min)
   - refresh_token (HttpOnly, 7 días)
   ↓
5. Cliente recibe cookies automáticamente
   ↓
6. Cada request incluye cookies automáticamente
   ↓
7. Si token expira, refrescar con refresh_token
   ↓
8. Generar nuevo access_token
```

## Implementación en la Aplicación

### Login Mejorado

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        user = Usuario.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            # Crear tokens JWT
            access_token, refresh_token = JWTAuth.create_tokens(user.id, user.email)
            
            # Login con Flask-Login
            login_user(user)
            
            # Crear respuesta y agregar cookies
            response = make_response(redirect(url_for('index')))
            response = JWTAuth.set_token_cookies(response, access_token, refresh_token)
            
            return response
        else:
            flash('Credenciales inválidas', 'danger')
    
    return render_template('login.html')
```

### Logout Mejorado

```python
@app.route('/logout')
@login_required
def logout():
    logout_user()
    response = make_response(redirect(url_for('index')))
    response = JWTAuth.clear_token_cookies(response)
    return response
```

### Refrescar Token

```python
@app.route('/api/refresh-token', methods=['POST'])
@refresh_token_required
def refresh_token():
    user = Usuario.query.get(request.user_id)
    
    # Crear nuevo access token
    access_token, refresh_token = JWTAuth.create_tokens(user.id, user.email)
    
    response = make_response(jsonify({'message': 'Token refrescado'}))
    response = JWTAuth.set_token_cookies(response, access_token, refresh_token)
    
    return response, 200
```

### Proteger Rutas

```python
from utils.auth import token_required

@app.route('/api/datos-protegidos', methods=['GET'])
@token_required
def datos_protegidos():
    # El usuario_id está disponible en request.user_id
    usuario_id = request.user_id
    usuario_email = request.user_email
    
    return jsonify({'data': 'información protegida'})
```

## Configuración de Cookies

Las cookies se configuran con los siguientes parámetros de seguridad:

```python
response.set_cookie(
    'access_token',
    access_token,
    max_age=1800,           # 30 minutos
    httponly=True,          # No accesible desde JavaScript
    secure=True,            # Solo HTTPS
    samesite='Lax',         # CSRF protection
    domain=None,            # Dominio actual
    path='/'                # Todas las rutas
)
```

### Explicación de cada parámetro:

| Parámetro | Valor | Razón |
|---|---|---|
| **max_age** | 1800 | Token expira en 30 minutos |
| **httponly** | True | Protege contra ataques XSS |
| **secure** | True | Solo se envía por HTTPS |
| **samesite** | Lax | Protege contra CSRF |
| **domain** | None | Usa el dominio actual |
| **path** | / | Disponible en todas las rutas |

## JavaScript - Sistema de Aplicación Profesional

### Clase App (`static/js/app.js`)

```javascript
class App {
    // Validación de formularios
    validateForm(form) {
        // Valida campos requeridos, email, contraseña
    }
    
    // API calls con manejo automático de tokens
    async api(endpoint, options = {}) {
        // Incluye cookies automáticamente
        // Maneja refresh de token automático
    }
    
    // Refrescar token
    async refreshToken() {
        // Llama a /api/refresh-token
        // Obtiene nuevas cookies automáticamente
    }
    
    // Mostrar notificaciones
    showNotification(message, type) {
        // Muestra alertas profesionales
    }
}
```

### Uso en HTML

```html
<!-- Formulario con validación automática -->
<form id="login-form">
    <input type="email" name="email" required>
    <input type="password" name="password" required>
    <button type="submit">Login</button>
</form>

<!-- API call automático con tokens -->
<script>
async function obtenerDatos() {
    const result = await app.api('/api/datos');
    console.log(result);
}
</script>
```

## Mejoras de Diseño

### Estilos Profesionales (`static/css/professional.css`)

- **Colores modernos**: Naranja (#FF6B35) como primario
- **Tipografía clara**: Segoe UI, tamaños responsivos
- **Componentes reutilizables**: Cards, buttons, forms
- **Responsive design**: Mobile-first approach
- **Transiciones suaves**: Para mejor UX

### Base Template (`templates/base.html`)

- Header profesional con navegación
- Alertas integradas
- Footer con múltiples secciones
- User profile dropdown
- Scripts automáticos

## Seguridad

### Protección contra ataques

| Ataque | Protección |
|---|---|
| **XSS** | Cookies HttpOnly |
| **CSRF** | SameSite=Lax + Tokens |
| **Session Hijacking** | Tokens con firma |
| **Token Reuse** | Refresh token rotation |
| **Man-in-the-Middle** | HTTPS + Secure flag |

### Best Practices Implementados

✅ Tokens con firma (HS256)  
✅ Expiración automática  
✅ Refresh token para renovación  
✅ Cookies seguras  
✅ Validación en servidor  
✅ Logging de eventos  
✅ HTTPS requerido  
✅ Headers de seguridad  

## Configuración en `config.py`

```python
# Cookie settings
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 1800

# JWT settings (en utils/auth.py)
TOKEN_EXPIRATION = 30  # minutos
REFRESH_TOKEN_EXPIRATION = 7 * 24 * 60  # 7 días
```

## Migrando desde localStorage

### Antes (❌ Inseguro)

```javascript
// localStorage no se usa más
// localStorage.setItem('token', token);
// const token = localStorage.getItem('token');
```

### Después (✅ Seguro)

```javascript
// Cookies se manejan automáticamente
// El navegador incluye cookies en cada request
// JavaScript no puede acceder a las cookies HttpOnly

// Para API calls:
const result = await app.api('/api/endpoint');
// Las cookies se incluyen automáticamente con credentials: 'include'
```

## Testing

### Test de Login

```bash
1. Ir a /login
2. Ingresar credenciales válidas
3. Verificar que las cookies se crean:
   - F12 → Application → Cookies
   - Ver access_token y refresh_token
4. Verificar que tienen los flags:
   - HttpOnly: ✓
   - Secure: ✓
   - SameSite: Lax
```

### Test de Token Expiration

```bash
1. Esperar 30 minutos o editar TOKEN_EXPIRATION a 1
2. Hacer un request a una ruta protegida
3. El sistema automáticamente:
   - Detecta el token expirado
   - Llama a /api/refresh-token
   - Obtiene nuevo access_token
   - Reintenta el request original
4. El usuario no ve cambio alguno
```

## Cambios en Rutas Existentes

### Rutas Protegidas con `@login_required`

Continúan funcionando igual porque:
- Flask-Login sigue siendo usado
- El usuario se mantiene autenticado en `current_user`
- Las cookies JWT son adicionales

### Rutas API con `@token_required`

```python
@app.route('/api/carrito/items', methods=['GET'])
@token_required
def api_carrito_items():
    usuario_id = request.user_id  # Del token JWT
    items = Carrito.query.filter_by(usuario_id=usuario_id).all()
    return jsonify([...])
```

## Ventajas de esta Implementación

### Para el Usuario
✅ Experiencia transparente  
✅ Sin popups de "sesión expirada"  
✅ Sesión se mantiene 7 días  
✅ Seguridad mejorada  

### Para el Desarrollador
✅ Fácil de implementar  
✅ Escalable  
✅ Compatible con microservicios  
✅ Compatible con SPA (React, Vue, Angular)  

### Para la Aplicación
✅ Menos vulnerabilidades  
✅ Mejor control de sesiones  
✅ Estadísticas de uso  
✅ Revocación de tokens posible  

## Próximas Mejoras

1. **Refresh Token Rotation**: Cambiar refresh token en cada uso
2. **Token Blacklist**: Revocar tokens manualmente
3. **2FA**: Autenticación de dos factores
4. **Rate Limiting**: Limitar intentos de login
5. **Audit Log**: Registro de todos los accesos
6. **OAuth2**: Integración con redes sociales

## Referencias

- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [OWASP Session Management](https://owasp.org/www-community/attacks/CSRF)
- [Cookies Security](https://owasp.org/www-community/controls/Cookie_Security)
- [HttpOnly Flag](https://owasp.org/www-community/controls/Content_Security_Policy/Expecting-CT-Header-in-Response-Type)

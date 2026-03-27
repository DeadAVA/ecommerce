# Guía de Contribución

Este es un repositorio privado. Las contribuciones están limitadas al propietario del proyecto.

## Flujo de Trabajo

### 1. Actualizar desde main

```bash
git pull origin master
```

### 2. Crear rama de feature

```bash
git checkout -b feature/nombre-descriptivo
```

**Ejemplos de ramas:**
- `feature/agregar-paypal` - Nueva característica
- `fix/carrito-error` - Arreglar bug
- `docs/actualizar-readme` - Documentación
- `refactor/simplificar-auth` - Refactoring

### 3. Hacer cambios y commits

```bash
# Staging
git add archivo.py

# Commit con mensaje descriptivo
git commit -m "Descripción clara del cambio"
```

**Guía de mensajes de commit:**
- Usar imperativo: "Agregar", "Arreglar", "Actualizar"
- Describir QUÉ hace el cambio
- Primera línea ≤ 50 caracteres
- Detalles en líneas siguientes si es necesario

**Ejemplos buenos:**
```
Agregar validación de email en registro
Arreglar error de carrito cuando producto no existe  
Actualizar dependencias (requirements.txt)
Refactor función de pago
```

### 4. Push a la rama

```bash
git push -u origin feature/nombre-descriptivo
```

### 5. Mantener actualizado

Si la rama master cambió mientras trabajas:

```bash
git fetch origin
git rebase origin/master

# Si hay conflictos, resolverlos y:
git rebase --continue
```

---

## Estándares de Código

### Python

**Formato y style:**
- Usar PEP 8 (4 espacios de indentación)
- Máximo 79 caracteres por línea (docstrings/comentarios 72)
- Nombres descriptivos en inglés

```python
# ✅ Bueno
def validate_user_email(email):
    """Validate email format."""
    return "@" in email

# ❌ Malo
def validate(e):
    return "@" in e
```

**Documentación:**
- Docstrings en todas las funciones públicas
- Comentarios para lógica compleja
- Type hints recomendados

```python
def get_order_total(order_id: int) -> float:
    """
    Calculate total price for an order.
    
    Args:
        order_id: The order identifier
        
    Returns:
        Total price including tax and shipping
    """
    order = Order.query.get(order_id)
    return order.subtotal + order.tax + order.shipping
```

### HTML/Templates

```html
<!-- Use semantic HTML -->
<section class="products">
    <div class="product-grid">
        <article class="product-card">
            <!-- Proper indentation -->
        </article>
    </div>
</section>
```

### JavaScript

```javascript
// Use const/let, not var
const productList = [];
let currentPage = 1;

// Meaningful names
function calculateCartTotal() {
    // Implementation
}

// Comments for complex logic
// Calculate discount based on quantity tiers
const discount = quantity > 100 ? 0.15 : (quantity > 50 ? 0.10 : 0);
```

### CSS

```css
/* Use meaningful class names */
.product-card {
    /* Properties grouped logically */
    display: flex;
    gap: 1rem;
    padding: 1rem;
    
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
}

/* Use BEM or similar methodology */
.product-card__title { }
.product-card__price { }
```

---

## Testing

### Tests Unitarios

```python
# tests/test_models.py
import pytest
from models.models import User

def test_user_creation():
    user = User(username='test', email='test@example.com')
    assert user.username == 'test'
    assert user.is_admin == False

def test_user_validation():
    user = User(username='', email='invalid')
    assert not user.is_valid()
```

### Ejecutar tests

```bash
# Instalar pytest
pip install pytest

# Ejecutar
pytest

# Con verbose
pytest -v

# Test específico
pytest tests/test_models.py::test_user_creation
```

---

## Checklist Antes de Push

- [ ] Código sigue estándares (PEP 8, etc)
- [ ] Funcionalidad probada localmente
- [ ] No hay archivos innecesarios (.pyc, __pycache__)
- [ ] Variables sensibles no están en el código
- [ ] Documentación/comentarios actualizados
- [ ] Commit message es descriptivo
- [ ] Cambios en requirements.txt si agregó dependencias

---

## Dependencias

Si necesitas agregar una nueva dependencia:

```bash
# Instalar
pip install paquete-nuevo

# Actualizar requirements.txt
pip freeze > requirements.txt

# Comitear cambio
git add requirements.txt
git commit -m "Add paquete-nuevo for [razón]"
```

---

## Bugs Conocidos y TODO

Ver `CAMBIOS_REALIZADOS.md` para:
- Bugs activos
- Features planeadas
- Mejoras pendientes

---

## Preguntas Frecuentes

**¿Cómo recluizar cambios?**
```bash
git reset --hard HEAD~1  # Deshacer último commit
git push --force        # Forzar push (¡cuidado!)
```

**¿Base de datos rota?**
```bash
# Backup y recrear
cp ecommerce.db ecommerce.db.backup
rm ecommerce.db
# Reiniciar app
```

**¿Merge conflict?**
```bash
git status  # Ver conflictos
# Editar archivo y resolver
git add archivo_conflictivo
git commit -m "Resolve merge conflict"
```

---

**Para el propietario:** Por favor revisa los cambios antes de mergesrlos y aprueba la calidad del código.

**Última actualización:** 27 de marzo de 2026

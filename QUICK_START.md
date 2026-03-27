# Setup Rápido - Ecommerce

## Inicio en 5 minutos

### Windows PowerShell

```powershell
# 1. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 2. Instalar dependencias (si es primera vez)
pip install -r requirements.txt

# 3. Configurar variables de entorno
# Crear archivo .env con tus credenciales

# 4. Ejecutar la aplicación
python app.py

# 5. Abrir navegador
Start-Process http://localhost:5000
```

### Linux/Mac

```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar .env
# Editar archivo .env

# 4. Ejecutar
python app.py

# 5. Abrir
open http://localhost:5000
```

## Variables de Entorno (.env)

Las credenciales más críticas:

```
# Seguridad
SECRET_KEY=GeneraUnaSuiteSegura123!
JWT_SECRET_KEY=OtraClaveSegura456!

# PayPal
PAYPAL_CLIENT_ID=tu_client_id_aqui
PAYPAL_SECRET=tu_secret_aqui

# Email (opcional, para reset password)
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=contraseña_app_gmail
```

## Troubleshooting Rápido

### Error: ModuleNotFoundError
```powershell
# Reconectar entorno virtual
.\venv\Scripts\Activate.ps1
pip install --upgrade -r requirements.txt
```

### Error: Port 5000 already in use
```powershell
# Usar otro puerto
python app.py --port 5001
# O en code:
export FLASK_PORT=5001
```

### Base de datos corrupta
```powershell
# Backup y reset
Copy-Item ecommerce.db ecommerce.db.backup
Remove-Item ecommerce.db
python app.py  # Crear DB nueva
```

## URLs Importantes

- **Home**: http://localhost:5000
- **Admin Dashboard**: http://localhost:5000/admin/dashboard
- **Shop**: http://localhost:5000/shop
- **Contacto**: http://localhost:5000/contact

## Credenciales de Ejemplo

Usuario admin debe crearse manualmente o mediante:
```python
# En Python shell
from models.models import User
admin = User(username='admin', email='admin@example.com', is_admin=True)
db.session.add(admin)
db.session.commit()
```

## Próximos Pasos

1. Revisar `config.py` para configuraciones específicas
2. Leer `GUIA_DESPLIEGUE.md` para producción
3. Consultar `IMPLEMENTACION_API_ZONAS.md` si necesitas envíos

---
**¿Problema?** Revisar logs en `debug=True` mode

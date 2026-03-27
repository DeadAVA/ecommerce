# API de Zonas Postales de México

## Descripción

API local para consultar códigos postales, colonias, estados y municipios de México. Utiliza un dataset XML con más de 156,000 registros de información geográfica de México.

## Características

- ✅ Búsqueda rápida de colonias por código postal
- ✅ Validación de códigos postales
- ✅ Búsqueda de ciudades por estado
- ✅ Búsqueda de municipios por estado
- ✅ Búsqueda de texto parcial
- ✅ Cache en cliente para reducir llamadas
- ✅ Índices para búsquedas O(1)

## Instalación

La API está incluida en `api_zonas/` y se registra automáticamente al iniciar la aplicación Flask.

```bash
# Asegúrate de tener el archivo de datos:
api_zonas/data/CPdescarga.xml
```

## Endpoints

### 1. Obtener Información de la API

```
GET /api/zones/info
```

**Respuesta:**
```json
{
  "total_registros": 156940,
  "cargado": true,
  "estados": 32,
  "archivo": "CPdescarga.xml",
  "codigos_postales_unicos": 1203
}
```

### 2. Listar Todos los Estados

```
GET /api/zones/estados
```

**Respuesta:**
```json
{
  "estados": [
    "Aguascalientes",
    "Baja California",
    "Ciudad de México",
    ...
  ]
}
```

### 3. Obtener Colonias por Código Postal

```
GET /api/zones/colonias/{codigo_postal}
```

**Parámetros:**
- `codigo_postal` (string): Código postal de 5 dígitos (ej: 01001)

**Respuesta:**
```json
{
  "codigo_postal": "01001",
  "colonias": [
    {
      "colonia": "San Ángel",
      "tipo": "Colonia",
      "municipio": "Álvaro Obregón",
      "estado": "Ciudad de México",
      "zona": "Urbano"
    },
    ...
  ],
  "total": 63
}
```

### 4. Obtener Ciudades por Estado

```
GET /api/zones/ciudades/{estado}
```

**Parámetros:**
- `estado` (string): Nombre del estado

**Respuesta:**
```json
{
  "estado": "Ciudad de México",
  "ciudades": [
    "Ciudad de México"
  ],
  "total": 1
}
```

### 5. Obtener Municipios por Estado

```
GET /api/zones/municipios/{estado}
```

**Parámetros:**
- `estado` (string): Nombre del estado

**Respuesta:**
```json
{
  "estado": "Ciudad de México",
  "municipios": [
    "Álvaro Obregón",
    "Benito Juárez",
    "Coyoacán",
    ...
  ],
  "total": 16
}
```

### 6. Validar Código Postal

```
POST /api/zones/validar
Content-Type: application/json
```

**Body:**
```json
{
  "codigo_postal": "01001",
  "estado": "Ciudad de México",  // Opcional
  "colonia": "San Ángel"          // Opcional
}
```

**Respuesta (válido):**
```json
{
  "valido": true,
  "info": {
    "valido": true,
    "codigo_postal": "01001",
    "colonias": ["San Ángel", "Los Alpes", ...],
    "estados": ["Ciudad de México"],
    "ciudades": ["Ciudad de México"],
    "municipios": ["Álvaro Obregón"]
  }
}
```

**Respuesta (inválido):**
```json
{
  "valido": false,
  "info": {
    "valido": false,
    "codigo_postal": "01001",
    "error": "Colonia 'Inexistente' no existe para código postal 01001",
    "colonias": [...],
    "estados": [...],
    "ciudades": [...],
    "municipios": [...]
  }
}
```

### 7. Buscar por Texto

```
GET /api/zones/buscar?q={texto}&campo={campo}
```

**Parámetros Query:**
- `q` (string): Texto a buscar (requerido)
- `campo` (string): Campo donde buscar (default: "colonia")
  - Opciones: `colonia`, `estado`, `municipio`, `ciudad`

**Respuesta:**
```json
{
  "busqueda": "san",
  "campo": "colonia",
  "resultados": [
    {
      "codigo_postal": "01001",
      "colonia": "San Ángel",
      "tipo": "Colonia",
      "municipio": "Álvaro Obregón",
      "estado": "Ciudad de México",
      "ciudad": "Ciudad de México"
    },
    ...
  ],
  "total": 50
}
```

## Cliente JavaScript

Se incluye un cliente JavaScript para usar la API desde el navegador.

### Uso Básico

```javascript
// El cliente está disponible globalmente como 'zonesAPI'

// Obtener colonias
const colonias = await zonesAPI.getColonias('01001');
console.log(colonias);

// Validar dirección
const resultado = await zonesAPI.validar('01001', 'Ciudad de México', 'San Ángel');
if (resultado.valido) {
  console.log('Dirección válida');
}

// Buscar
const resultados = await zonesAPI.buscar('san', 'colonia');
console.log(resultados);
```

### Setup Automático en Formularios

Al incluir `zones-api.js` en una página con formularios de dirección, se configura automáticamente:

1. **Carga automática de colonias**: Al ingresar un código postal en `#codigo_postal`, se cargan las colonias en `#colonia`
2. **Validación automática**: Al enviar un formulario de dirección, valida los datos

### Ejemplo de Uso en HTML

```html
<form method="POST" action="/direccion">
  <input type="text" name="codigo_postal" id="codigo_postal" maxlength="5" pattern="\d{5}">
  
  <select name="colonia" id="colonia">
    <option value="">Selecciona una colonia</option>
  </select>
  
  <button type="submit">Guardar Dirección</button>
</form>

<script src="{{ url_for('static', filename='js/zones-api.js') }}"></script>
```

## Métodos de la Clase ZonesAPI en Python

### Importar

```python
from api_zonas import get_zones_api

api = get_zones_api()
```

### get_colonias_por_cp(codigo_postal)

Obtiene colonias para un código postal.

```python
colonias = api.get_colonias_por_cp('01001')
# [
#   {'colonia': 'San Ángel', 'tipo': 'Colonia', 'municipio': '...', ...},
#   ...
# ]
```

### get_estados()

Obtiene lista de todos los estados.

```python
estados = api.get_estados()
# ['Aguascalientes', 'Baja California', ...]
```

### get_ciudades_por_estado(estado)

Obtiene ciudades de un estado.

```python
ciudades = api.get_ciudades_por_estado('Ciudad de México')
```

### get_municipios_por_estado(estado)

Obtiene municipios de un estado.

```python
municipios = api.get_municipios_por_estado('Ciudad de México')
```

### validar_codigo_postal(codigo_postal, estado=None, colonia=None)

Valida un código postal con estado y colonia opcionales.

```python
es_valido, info = api.validar_codigo_postal('01001', 'Ciudad de México', 'San Ángel')
if es_valido:
    print("Dirección válida")
else:
    print(f"Error: {info.get('error')}")
```

### buscar_por_texto(texto, campo='colonia')

Busca texto en el dataset.

```python
resultados = api.buscar_por_texto('san angel', 'colonia')
# Total máximo de resultados: 100
```

### get_info()

Retorna información de la API.

```python
info = api.get_info()
# {
#   'total_registros': 156940,
#   'cargado': True,
#   'estados': 32,
#   'archivo': 'CPdescarga.xml',
#   'codigos_postales_unicos': 1203
# }
```

## Integración en la Aplicación

### Validación de Direcciones

La función `validar_codigo_postal_mexico` en `models/estados.py` ahora usa la API local:

```python
from models.estados import validar_codigo_postal_mexico

es_valido = validar_codigo_postal_mexico('01001', 'Ciudad de México', 'San Ángel')
```

### Ventajas

- Sin dependencias externas (no requiere API de COPOMEX)
- Búsquedas instantáneas (sin latencia de red)
- Completamente offline una vez cargado el dataset
- Cache inteligente en cliente (JavaScript)

## Rendimiento

- **Carga inicial**: ~2-3 segundos (parseo del XML de 66MB)
- **Búsquedas posteriores**: <10ms (índices y caché)
- **Consumo de memoria**: ~150MB (dataset completo en RAM)

## Estructura de Archivos

```
api_zonas/
├── __init__.py           # Punto de entrada
├── zones_api.py          # Lógica principal
├── routes.py             # Endpoints Flask
└── data/
    └── CPdescarga.xml    # Dataset (66 MB)
```

## Rutas API Registradas

Las rutas se registran automáticamente con el prefijo `/api/zones`:

```python
from api_zonas.routes import zones_bp
app.register_blueprint(zones_bp)
```

## Troubleshooting

### Las colonias no cargan

1. Verifica que el archivo `api_zonas/data/CPdescarga.xml` existe
2. Revisa la consola del servidor para mensajes de error
3. Asegúrate de que el JavaScript `zones-api.js` esté cargado

### Código Postal no válido

- El código postal debe tener exactamente 5 dígitos
- Se rellenan con ceros a la izquierda si es necesario (ej: 999 → 00999)

## Fuente de Datos

Los datos provienen del Servicio Postal Mexicano (CorreoNet) y contienen información postal completa y actualizada del país.

---

**Última actualización:** 18 de febrero de 2026

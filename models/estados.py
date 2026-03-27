import os
from api_zonas import get_zones_api

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')


def validar_codigo_postal_mexico(cp, estado, colonia):
    """
    Valida un código postal con estado y colonia usando la base de datos local
    
    Args:
        cp: Código postal
        estado: Estado
        colonia: Colonia
        
    Returns:
        bool: True si los datos son válidos, False en caso contrario
    """
    try:
        api = get_zones_api()
        es_valido, info = api.validar_codigo_postal(cp, estado, colonia)
        return es_valido
    except Exception as e:
        print(f"Error validando código postal: {e}")
        return False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ESTADOS_MEXICO = [
    "Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
    "Chiapas", "Chihuahua", "Ciudad de México", "Coahuila", "Colima",
    "Durango", "Estado de México", "Guanajuato", "Guerrero", "Hidalgo",
    "Jalisco", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca",
    "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa",
    "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
]

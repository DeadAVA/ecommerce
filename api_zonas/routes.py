"""
Rutas de API REST para Zonas Postales
"""

from flask import Blueprint, jsonify, request
from .zones_api import get_zones_api

zones_bp = Blueprint('zones_api', __name__, url_prefix='/api/zones')


@zones_bp.route('/info', methods=['GET'])
def get_info():
    """Información sobre la API de zonas"""
    try:
        api = get_zones_api()
        return jsonify(api.get_info())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@zones_bp.route('/estados', methods=['GET'])
def get_estados():
    """Obtiene lista de todos los estados"""
    try:
        api = get_zones_api()
        estados = api.get_estados()
        return jsonify({'estados': estados})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@zones_bp.route('/ciudades/<estado>', methods=['GET'])
def get_ciudades(estado):
    """Obtiene ciudades para un estado específico"""
    try:
        api = get_zones_api()
        ciudades = api.get_ciudades_por_estado(estado)
        return jsonify({
            'estado': estado,
            'ciudades': ciudades,
            'total': len(ciudades)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@zones_bp.route('/municipios/<estado>', methods=['GET'])
def get_municipios(estado):
    """Obtiene municipios para un estado específico"""
    try:
        api = get_zones_api()
        municipios = api.get_municipios_por_estado(estado)
        return jsonify({
            'estado': estado,
            'municipios': municipios,
            'total': len(municipios)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@zones_bp.route('/colonias/<codigo_postal>', methods=['GET'])
def get_colonias(codigo_postal):
    """
    Obtiene colonias para un código postal específico
    
    Parámetros:
        codigo_postal: Código postal (ej: 01001)
    """
    try:
        api = get_zones_api()
        colonias = api.get_colonias_por_cp(codigo_postal)
        return jsonify({
            'codigo_postal': codigo_postal,
            'colonias': colonias,
            'total': len(colonias)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@zones_bp.route('/validar', methods=['POST'])
def validar():
    """
    Valida un código postal con opcionalmente estado y colonia
    
    Body JSON:
    {
        "codigo_postal": "01001",
        "estado": "Ciudad de México",  (opcional)
        "colonia": "San Ángel"  (opcional)
    }
    """
    try:
        data = request.get_json()
        if not data or 'codigo_postal' not in data:
            return jsonify({'error': 'codigo_postal es requerido'}), 400

        api = get_zones_api()
        codigo_postal = data.get('codigo_postal')
        estado = data.get('estado')
        colonia = data.get('colonia')

        es_valido, info = api.validar_codigo_postal(codigo_postal, estado, colonia)

        return jsonify({
            'valido': es_valido,
            'info': info
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@zones_bp.route('/buscar', methods=['GET'])
def buscar():
    """
    Busca de forma parcial en los datos
    
    Parámetros:
        q: Texto a buscar
        campo: Campo donde buscar (colonia, estado, municipio, ciudad) - default: colonia
    """
    try:
        q = request.args.get('q', '').strip()
        campo = request.args.get('campo', 'colonia')

        if not q:
            return jsonify({'error': 'Se requiere parámetro "q"'}), 400

        api = get_zones_api()
        resultados = api.buscar_por_texto(q, campo)

        return jsonify({
            'busqueda': q,
            'campo': campo,
            'resultados': resultados,
            'total': len(resultados)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

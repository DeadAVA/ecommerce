"""
API de Zonas Postales - Motor de búsqueda de códigos postales y colonias
"""

import re
import os
from typing import List, Dict, Optional, Tuple
import threading

# Sincronización para evitar problemas de concurrencia
_lock = threading.Lock()


class ZonesAPI:
    """
    API para consultar información de códigos postales y colonias de México
    Carga y parsea el archivo XML de forma eficiente
    """

    def __init__(self, xml_path: str):
        """
        Inicializa la API con el archivo XML de códigos postales
        
        Args:
            xml_path: Ruta al archivo XML con los datos de zonas postales
        """
        self.xml_path = xml_path
        self.data = []
        self._loaded = False
        self.index_cp = {}  # Índice para búsqueda rápida por CP
        self.index_codigo = {}  # Índice para búsqueda rápida por ID de colonia (d_codigo)
        self._load_data()

    def _load_data(self) -> None:
        """Carga el archivo XML parseando con expresiones regulares"""
        if self._loaded:
            return

        if not os.path.exists(self.xml_path):
            raise FileNotFoundError(f"Archivo XML no encontrado: {self.xml_path}")

        try:
            with _lock:
                if self._loaded:  # Double-check
                    return

                # Leer el archivo completo
                with open(self.xml_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Patrón para extraer elementos table
                # El XML está estructurado como: <table xmlns="NewDataSet">...</table>
                table_pattern = r'<table[^>]*>(.*?)</table>'
                tables = re.findall(table_pattern, content, re.DOTALL)

                for table_content in tables:
                    record = self._parse_table(table_content)
                    if record and record.get('d_CP'):
                        self.data.append(record)
                        
                        # Indexar por código postal para búsquedas rápidas
                        cp = record['d_CP']
                        if cp not in self.index_cp:
                            self.index_cp[cp] = []
                        self.index_cp[cp].append(record)
                        
                        # Indexar también por d_codigo (ID de colonia) si existe
                        codigo = record.get('d_codigo', '').strip()
                        if codigo:
                            if codigo not in self.index_codigo:
                                self.index_codigo[codigo] = []
                            self.index_codigo[codigo].append(record)

                self._loaded = True
                print(f"[OK] Cargados {len(self.data)} registros de codigos postales desde {os.path.basename(self.xml_path)}")

        except Exception as e:
            raise Exception(f"Error cargando XML: {str(e)}")

    def _parse_table(self, content: str) -> Dict[str, str]:
        """Parsea el contenido de un elemento table"""
        record = {}
        
        # Patrón para extraer elementos XML simples
        # Busca: <tag>contenido</tag>
        element_pattern = r'<([^/>]+)>([^<]*)</\1>'
        
        matches = re.findall(element_pattern, content)
        for tag, value in matches:
            # Limpiar el tag (puede tener atributos)
            tag = tag.split()[0]
            record[tag] = value.strip()
        
        return record

    def get_colonias_por_cp(self, codigo_postal: str) -> List[Dict[str, str]]:
        """
        Obtiene todas las colonias para un código postal o ID de colonia
        
        Args:
            codigo_postal: Código postal a buscar (ej: '01001') 
                         o ID de colonia (d_codigo)
            
        Returns:
            Lista de diccionarios con información de colonias
        """
        codigo_postal = codigo_postal.strip().zfill(5)
        colonias = []
        
        # Primero intentar búsqueda por CP
        records = self.index_cp.get(codigo_postal, [])
        
        # Si no encuentra por CP, intentar por d_codigo (ID de colonia)
        if not records:
            records = self.index_codigo.get(codigo_postal, [])
        
        seen = set()
        for record in records:
            colonia = record.get('d_asenta', '').strip()
            if colonia and colonia not in seen:
                colonias.append({
                    'colonia': colonia,
                    'tipo': record.get('d_tipo_asenta', ''),
                    'municipio': record.get('D_mnpio', ''),
                    'estado': record.get('d_estado', ''),
                    'zona': record.get('d_zona', ''),
                    'codigo_postal': record.get('d_CP', ''),
                })
                seen.add(colonia)

        return sorted(colonias, key=lambda x: x['colonia'])

    def get_estados(self) -> List[str]:
        """Obtiene lista única de estados"""
        estados = set()
        for record in self.data:
            estado = record.get('d_estado', '').strip()
            if estado:
                estados.add(estado)
        return sorted(list(estados))

    def get_ciudades_por_estado(self, estado: str) -> List[str]:
        """
        Obtiene ciudades para un estado específico
        
        Args:
            estado: Nombre del estado
            
        Returns:
            Lista de ciudades únicas
        """
        ciudades = set()
        for record in self.data:
            if record.get('d_estado', '').strip().lower() == estado.lower():
                ciudad = record.get('d_ciudad', '').strip()
                if ciudad:
                    ciudades.add(ciudad)
        return sorted(list(ciudades))

    def get_municipios_por_estado(self, estado: str) -> List[str]:
        """Obtiene municipios para un estado específico"""
        municipios = set()
        for record in self.data:
            if record.get('d_estado', '').strip().lower() == estado.lower():
                municipio = record.get('D_mnpio', '').strip()
                if municipio:
                    municipios.add(municipio)
        return sorted(list(municipios))

    def validar_codigo_postal(self, codigo_postal: str, estado: str = None, 
                            colonia: str = None) -> Tuple[bool, Dict]:
        """
        Valida si un código postal o ID de colonia existe
        
        Args:
            codigo_postal: Código postal a validar o ID de colonia (d_codigo)
            estado: Estado (opcional)
            colonia: Colonia (opcional)
            
        Returns:
            Tupla (es_válido, información_encontrada)
        """
        codigo_postal = codigo_postal.strip().zfill(5)
        info = {
            'valido': False,
            'codigo_postal': codigo_postal,
            'colonias': [],
            'estados': set(),
            'ciudades': set(),
            'municipios': set()
        }

        # Buscar en índice CP
        records = self.index_cp.get(codigo_postal, [])
        
        # Si no encuentra en CP, buscar en índice d_codigo
        if not records:
            records = self.index_codigo.get(codigo_postal, [])
        
        for record in records:
            info['colonias'].append(record.get('d_asenta', '').strip())
            info['estados'].add(record.get('d_estado', '').strip())
            info['ciudades'].add(record.get('d_ciudad', '').strip())
            info['municipios'].add(record.get('D_mnpio', '').strip())
            info['valido'] = True

        # Remover duplicados y convertir a listas
        info['colonias'] = sorted(list(set(info['colonias'])))
        info['estados'] = sorted(list(info['estados']))
        info['ciudades'] = sorted(list(info['ciudades']))
        info['municipios'] = sorted(list(info['municipios']))

        # Validación adicional si se proporcionan estado/colonia
        if info['valido'] and estado:
            if estado not in info['estados']:
                info['valido'] = False
                info['error'] = f"Estado '{estado}' no coincide con código postal {codigo_postal}"

        if info['valido'] and colonia:
            if colonia not in info['colonias']:
                info['valido'] = False
                info['error'] = f"Colonia '{colonia}' no existe para código postal {codigo_postal}"

        return info['valido'], info

    def buscar_por_texto(self, texto: str, campo: str = 'colonia') -> List[Dict]:
        """
        Busca de forma parcial en un campo específico
        
        Args:
            texto: Texto a buscar
            campo: Campo donde buscar ('colonia', 'estado', 'municipio')
            
        Returns:
            Lista de registros coincidentes
        """
        texto = texto.lower().strip()
        resultados = []
        visto = set()

        campo_map = {
            'colonia': 'd_asenta',
            'estado': 'd_estado',
            'municipio': 'D_mnpio',
            'ciudad': 'd_ciudad'
        }

        if campo not in campo_map:
            return []

        campo_real = campo_map[campo]

        for record in self.data:
            valor = record.get(campo_real, '').lower()
            if texto in valor:
                # Crear clave para evitar duplicados
                key = (record.get('d_CP'), record.get('d_asenta'), record.get('d_estado'))
                if key not in visto:
                    resultados.append({
                        'codigo_postal': record.get('d_CP'),
                        'colonia': record.get('d_asenta'),
                        'tipo': record.get('d_tipo_asenta'),
                        'municipio': record.get('D_mnpio'),
                        'estado': record.get('d_estado'),
                        'ciudad': record.get('d_ciudad'),
                    })
                    visto.add(key)

        return resultados[:100]  # Limitar a 100 resultados

    def get_info(self) -> Dict:
        """Retorna información sobre la API"""
        return {
            'total_registros': len(self.data),
            'cargado': self._loaded,
            'estados': len(self.get_estados()),
            'archivo': os.path.basename(self.xml_path),
            'codigos_postales_unicos': len(self.index_cp)
        }


# Instancia global (singleton)
_zones_api_instance = None


def get_zones_api() -> ZonesAPI:
    """
    Obtiene la instancia global de ZonesAPI (lazy loading)
    
    Returns:
        Instancia de ZonesAPI
    """
    global _zones_api_instance

    if _zones_api_instance is None:
        xml_path = os.path.join(
            os.path.dirname(__file__),
            'data',
            'CPdescarga.xml'
        )
        _zones_api_instance = ZonesAPI(xml_path)

    return _zones_api_instance

    def get_colonias_por_cp(self, codigo_postal: str) -> List[Dict[str, str]]:
        """
        Obtiene todas las colonias para un código postal específico
        
        Args:
            codigo_postal: Código postal a buscar (ej: '01001')
            
        Returns:
            Lista de diccionarios con información de colonias
        """
        codigo_postal = codigo_postal.strip().zfill(5)
        colonias = []

        seen = set()  # Para evitar duplicados
        for record in self.data:
            if record.get('d_CP') == codigo_postal:
                colonia = record.get('d_asenta', '').strip()
                if colonia and colonia not in seen:
                    colonias.append({
                        'colonia': colonia,
                        'tipo': record.get('d_tipo_asenta', ''),
                        'municipio': record.get('D_mnpio', ''),
                        'estado': record.get('d_estado', ''),
                        'zona': record.get('d_zona', ''),
                    })
                    seen.add(colonia)

        return sorted(colonias, key=lambda x: x['colonia'])

    def get_estados(self) -> List[str]:
        """Obtiene lista única de estados"""
        estados = set()
        for record in self.data:
            estado = record.get('d_estado', '').strip()
            if estado:
                estados.add(estado)
        return sorted(list(estados))

    def get_ciudades_por_estado(self, estado: str) -> List[str]:
        """
        Obtiene ciudades para un estado específico
        
        Args:
            estado: Nombre del estado
            
        Returns:
            Lista de ciudades únicas
        """
        ciudades = set()
        for record in self.data:
            if record.get('d_estado', '').strip().lower() == estado.lower():
                ciudad = record.get('d_ciudad', '').strip()
                if ciudad:
                    ciudades.add(ciudad)
        return sorted(list(ciudades))

    def get_municipios_por_estado(self, estado: str) -> List[str]:
        """Obtiene municipios para un estado específico"""
        municipios = set()
        for record in self.data:
            if record.get('d_estado', '').strip().lower() == estado.lower():
                municipio = record.get('D_mnpio', '').strip()
                if municipio:
                    municipios.add(municipio)
        return sorted(list(municipios))

    def validar_codigo_postal(self, codigo_postal: str, estado: str = None, 
                            colonia: str = None) -> Tuple[bool, Dict]:
        """
        Valida si un código postal existe y opcionalmente valida estado/colonia
        
        Args:
            codigo_postal: Código postal a validar
            estado: Estado (opcional)
            colonia: Colonia (opcional)
            
        Returns:
            Tupla (es_válido, información_encontrada)
        """
        codigo_postal = codigo_postal.strip().zfill(5)
        info = {
            'valido': False,
            'codigo_postal': codigo_postal,
            'colonias': [],
            'estados': set(),
            'ciudades': set(),
            'municipios': set()
        }

        for record in self.data:
            if record.get('d_CP') == codigo_postal:
                info['colonias'].append(record.get('d_asenta', '').strip())
                info['estados'].add(record.get('d_estado', '').strip())
                info['ciudades'].add(record.get('d_ciudad', '').strip())
                info['municipios'].add(record.get('D_mnpio', '').strip())
                info['valido'] = True

        # Remover duplicados y convertir a listas
        info['colonias'] = sorted(list(set(info['colonias'])))
        info['estados'] = sorted(list(info['estados']))
        info['ciudades'] = sorted(list(info['ciudades']))
        info['municipios'] = sorted(list(info['municipios']))

        # Validación adicional si se proporcionan estado/colonia
        if info['valido'] and estado:
            if estado not in info['estados']:
                info['valido'] = False
                info['error'] = f"Estado '{estado}' no coincide con código postal {codigo_postal}"

        if info['valido'] and colonia:
            if colonia not in info['colonias']:
                info['valido'] = False
                info['error'] = f"Colonia '{colonia}' no existe para código postal {codigo_postal}"

        return info['valido'], info

    def buscar_por_texto(self, texto: str, campo: str = 'colonia') -> List[Dict]:
        """
        Busca de forma parcial en un campo específico
        
        Args:
            texto: Texto a buscar
            campo: Campo donde buscar ('colonia', 'estado', 'municipio')
            
        Returns:
            Lista de registros coincidentes
        """
        texto = texto.lower().strip()
        resultados = []
        visto = set()

        campo_map = {
            'colonia': 'd_asenta',
            'estado': 'd_estado',
            'municipio': 'D_mnpio',
            'ciudad': 'd_ciudad'
        }

        if campo not in campo_map:
            return []

        campo_real = campo_map[campo]

        for record in self.data:
            valor = record.get(campo_real, '').lower()
            if texto in valor:
                # Crear clave para evitar duplicados
                key = (record.get('d_CP'), record.get('d_asenta'), record.get('d_estado'))
                if key not in visto:
                    resultados.append({
                        'codigo_postal': record.get('d_CP'),
                        'colonia': record.get('d_asenta'),
                        'tipo': record.get('d_tipo_asenta'),
                        'municipio': record.get('D_mnpio'),
                        'estado': record.get('d_estado'),
                        'ciudad': record.get('d_ciudad'),
                    })
                    visto.add(key)

        return resultados[:100]  # Limitar a 100 resultados

    def get_info(self) -> Dict:
        """Retorna información sobre la API"""
        return {
            'total_registros': len(self.data),
            'cargado': self._loaded,
            'estados': len(self.get_estados()),
            'archivo': os.path.basename(self.xml_path)
        }


# Instancia global (singleton)
_zones_api_instance = None


def get_zones_api() -> ZonesAPI:
    """
    Obtiene la instancia global de ZonesAPI (lazy loading)
    
    Returns:
        Instancia de ZonesAPI
    """
    global _zones_api_instance

    if _zones_api_instance is None:
        xml_path = os.path.join(
            os.path.dirname(__file__),
            'data',
            'CPdescarga.xml'
        )
        _zones_api_instance = ZonesAPI(xml_path)

    return _zones_api_instance

    def get_colonias_por_cp(self, codigo_postal: str) -> List[Dict[str, str]]:
        """
        Obtiene todas las colonias para un código postal específico
        
        Args:
            codigo_postal: Código postal a buscar (ej: '01001')
            
        Returns:
            Lista de diccionarios con información de colonias
        """
        codigo_postal = codigo_postal.strip().zfill(5)
        colonias = []

        seen = set()  # Para evitar duplicados
        for record in self.data:
            if record.get('d_CP') == codigo_postal:
                colonia = record.get('d_asenta', '').strip()
                if colonia and colonia not in seen:
                    colonias.append({
                        'colonia': colonia,
                        'tipo': record.get('d_tipo_asenta', ''),
                        'municipio': record.get('D_mnpio', ''),
                        'estado': record.get('d_estado', ''),
                        'zona': record.get('d_zona', ''),
                    })
                    seen.add(colonia)

        return sorted(colonias, key=lambda x: x['colonia'])

    def get_estados(self) -> List[str]:
        """Obtiene lista única de estados"""
        estados = set()
        for record in self.data:
            estado = record.get('d_estado', '').strip()
            if estado:
                estados.add(estado)
        return sorted(list(estados))

    def get_ciudades_por_estado(self, estado: str) -> List[str]:
        """
        Obtiene ciudades para un estado específico
        
        Args:
            estado: Nombre del estado
            
        Returns:
            Lista de ciudades únicas
        """
        ciudades = set()
        for record in self.data:
            if record.get('d_estado', '').strip().lower() == estado.lower():
                ciudad = record.get('d_ciudad', '').strip()
                if ciudad:
                    ciudades.add(ciudad)
        return sorted(list(ciudades))

    def get_municipios_por_estado(self, estado: str) -> List[str]:
        """Obtiene municipios para un estado específico"""
        municipios = set()
        for record in self.data:
            if record.get('d_estado', '').strip().lower() == estado.lower():
                municipio = record.get('D_mnpio', '').strip()
                if municipio:
                    municipios.add(municipio)
        return sorted(list(municipios))

    def validar_codigo_postal(self, codigo_postal: str, estado: str = None, 
                            colonia: str = None) -> Tuple[bool, Dict]:
        """
        Valida si un código postal existe y opcionalmente valida estado/colonia
        
        Args:
            codigo_postal: Código postal a validar
            estado: Estado (opcional)
            colonia: Colonia (opcional)
            
        Returns:
            Tupla (es_válido, información_encontrada)
        """
        codigo_postal = codigo_postal.strip().zfill(5)
        info = {
            'valido': False,
            'codigo_postal': codigo_postal,
            'colonias': [],
            'estados': set(),
            'ciudades': set(),
            'municipios': set()
        }

        for record in self.data:
            if record.get('d_CP') == codigo_postal:
                info['colonias'].append(record.get('d_asenta', '').strip())
                info['estados'].add(record.get('d_estado', '').strip())
                info['ciudades'].add(record.get('d_ciudad', '').strip())
                info['municipios'].add(record.get('D_mnpio', '').strip())
                info['valido'] = True

        # Remover duplicados y convertir a listas
        info['colonias'] = sorted(list(set(info['colonias'])))
        info['estados'] = sorted(list(info['estados']))
        info['ciudades'] = sorted(list(info['ciudades']))
        info['municipios'] = sorted(list(info['municipios']))

        # Validación adicional si se proporcionan estado/colonia
        if info['valido'] and estado:
            if estado not in info['estados']:
                info['valido'] = False
                info['error'] = f"Estado '{estado}' no coincide con código postal {codigo_postal}"

        if info['valido'] and colonia:
            if colonia not in info['colonias']:
                info['valido'] = False
                info['error'] = f"Colonia '{colonia}' no existe para código postal {codigo_postal}"

        return info['valido'], info

    def buscar_por_texto(self, texto: str, campo: str = 'colonia') -> List[Dict]:
        """
        Busca de forma parcial en un campo específico
        
        Args:
            texto: Texto a buscar
            campo: Campo donde buscar ('colonia', 'estado', 'municipio')
            
        Returns:
            Lista de registros coincidentes
        """
        texto = texto.lower().strip()
        resultados = []
        visto = set()

        campo_map = {
            'colonia': 'd_asenta',
            'estado': 'd_estado',
            'municipio': 'D_mnpio',
            'ciudad': 'd_ciudad'
        }

        if campo not in campo_map:
            return []

        campo_real = campo_map[campo]

        for record in self.data:
            valor = record.get(campo_real, '').lower()
            if texto in valor:
                # Crear clave para evitar duplicados
                key = (record.get('d_CP'), record.get('d_asenta'), record.get('d_estado'))
                if key not in visto:
                    resultados.append({
                        'codigo_postal': record.get('d_CP'),
                        'colonia': record.get('d_asenta'),
                        'tipo': record.get('d_tipo_asenta'),
                        'municipio': record.get('D_mnpio'),
                        'estado': record.get('d_estado'),
                        'ciudad': record.get('d_ciudad'),
                    })
                    visto.add(key)

        return resultados[:100]  # Limitar a 100 resultados

    def get_info(self) -> Dict:
        """Retorna información sobre la API"""
        return {
            'total_registros': len(self.data),
            'cargado': self._loaded,
            'estados': len(self.get_estados()),
            'archivo': os.path.basename(self.xml_path)
        }


# Instancia global (singleton)
_zones_api_instance = None


def get_zones_api() -> ZonesAPI:
    """
    Obtiene la instancia global de ZonesAPI (lazy loading)
    
    Returns:
        Instancia de ZonesAPI
    """
    global _zones_api_instance

    if _zones_api_instance is None:
        xml_path = os.path.join(
            os.path.dirname(__file__),
            'data',
            'CPdescarga.xml'
        )
        _zones_api_instance = ZonesAPI(xml_path)

    return _zones_api_instance

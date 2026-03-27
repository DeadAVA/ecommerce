/**
 * API de Zonas Postales - JavaScript Client
 * Maneja la carga de colonias basada en código postal
 */

class ZonesAPIClient {
    constructor(baseUrl = '/api/zones') {
        this.baseUrl = baseUrl;
        this.cache = {}; // Cache para reducir llamadas
    }

    /**
     * Obtiene colonias para un código postal específico
     */
    async getColonias(codigoPostal) {
        codigoPostal = codigoPostal.toString().padStart(5, '0');
        
        // Usar cache si disponible
        if (this.cache[codigoPostal]) {
            return this.cache[codigoPostal];
        }

        try {
            const response = await fetch(`${this.baseUrl}/colonias/${codigoPostal}`);
            const data = await response.json();
            
            if (data.colonias) {
                this.cache[codigoPostal] = data.colonias;
                return data.colonias;
            }
            return [];
        } catch (error) {
            console.error('Error fetching colonias:', error);
            return [];
        }
    }

    /**
     * Valida un código postal con estado y colonia opcionalmente
     */
    async validar(codigoPostal, estado = null, colonia = null) {
        const body = {
            codigo_postal: codigoPostal.toString().padStart(5, '0')
        };
        if (estado) body.estado = estado;
        if (colonia) body.colonia = colonia;

        try {
            const response = await fetch(`${this.baseUrl}/validar`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error validating:', error);
            return { valido: false };
        }
    }

    /**
     * Obtiene lista de estados
     */
    async getEstados() {
        if (this.cache['estados']) {
            return this.cache['estados'];
        }

        try {
            const response = await fetch(`${this.baseUrl}/estados`);
            const data = await response.json();
            if (data.estados) {
                this.cache['estados'] = data.estados;
                return data.estados;
            }
            return [];
        } catch (error) {
            console.error('Error fetching estados:', error);
            return [];
        }
    }

    /**
     * Busca en el dataset
     */
    async buscar(texto, campo = 'colonia') {
        try {
            const response = await fetch(`${this.baseUrl}/buscar?q=${encodeURIComponent(texto)}&campo=${campo}`);
            const data = await response.json();
            return data.resultados || [];
        } catch (error) {
            console.error('Error searching:', error);
            return [];
        }
    }
}

// Instancia global
const zonesAPI = new ZonesAPIClient();

/**
 * Setupea los event listeners para cargar colonias
 */
function setupAddressForms() {
    const codigoPostalInput = document.getElementById('codigo_postal');
    const coloniaSelect = document.getElementById('colonia');

    if (!codigoPostalInput) return; // No hay formulario de dirección

    // Cargar colonias cuando se ingresa un código postal
    codigoPostalInput.addEventListener('change', async function() {
        const cp = this.value.trim();
        
        if (!cp || cp.length !== 5) {
            coloniaSelect.innerHTML = '<option value="">Ingresa un código postal válido (5 dígitos)</option>';
            return;
        }

        coloniaSelect.innerHTML = '<option value="">Cargando...</option>';
        coloniaSelect.disabled = true;

        const colonias = await zonesAPI.getColonias(cp);

        if (colonias.length > 0) {
            coloniaSelect.innerHTML = '<option value="">Selecciona una colonia</option>';
            colonias.forEach(col => {
                const option = document.createElement('option');
                option.value = col.colonia;
                option.textContent = `${col.colonia} (${col.municipio})`;
                option.dataset.tipo = col.tipo;
                option.dataset.municipio = col.municipio;
                option.dataset.estado = col.estado;
                coloniaSelect.appendChild(option);
            });
        } else {
            coloniaSelect.innerHTML = '<option value="">No se encontraron colonias para este código postal</option>';
        }

        coloniaSelect.disabled = false;
    });

    // También permitir búsqueda mientras escribe
    if (codigoPostalInput.addEventListener) {
        codigoPostalInput.addEventListener('input', debounce(async function() {
            const cp = this.value.trim();
            if (cp === '' || cp.length < 3) return;

            const resultados = await zonesAPI.buscar(cp, 'ciudad');
            // Aquí podrías mostrar un autocomplete si lo deseas
        }, 500));
    }
}

/**
 * Debounce para evitar múltiples llamadas mientras se escribe
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func.apply(this, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Validar dirección en el servidor antes de enviar
 */
async function validarDireccionAntesDeSend(event) {
    const form = event.target;
    const cp = form.querySelector('[name="codigo_postal"]').value;
    const estado = form.querySelector('[name="estado"]')?.value;
    const colonia = form.querySelector('[name="colonia"]')?.value;

    if (cp && estado && colonia) {
        const resultado = await zonesAPI.validar(cp, estado, colonia);
        if (!resultado.valido) {
            event.preventDefault();
            alert(resultado.info?.error || 'Los datos de la dirección no son válidos');
            return false;
        }
    }
    return true;
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', setupAddressForms);

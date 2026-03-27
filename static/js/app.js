/**
 * Sistema profesional de aplicación web
 * Manejo de API con tokens JWT en cookies
 */

class App {
    constructor() {
        this.apiBase = window.location.origin;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFormValidation();
        this.setupAjaxInterceptor();
    }

    /**
     * Configurar listeners globales
     */
    setupEventListeners() {
        // Cerrar sesión
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-logout]')) {
                e.preventDefault();
                this.logout();
            }
        });

        // Refrescar token
        setInterval(() => this.refreshToken(), 25 * 60 * 1000); // Cada 25 minutos
    }

    /**
     * Validación de formularios
     */
    setupFormValidation() {
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!form.classList.contains('no-validate')) {
                    if (!this.validateForm(form)) {
                        e.preventDefault();
                    }
                }
            });
        });
    }

    /**
     * Validar formulario
     */
    validateForm(form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');

        requiredFields.forEach(field => {
            const value = field.value.trim();
            
            if (!value) {
                this.showFieldError(field, 'Este campo es obligatorio');
                isValid = false;
            } else {
                this.clearFieldError(field);
            }

            // Validación de email
            if (field.type === 'email' && value && !this.isValidEmail(value)) {
                this.showFieldError(field, 'Email inválido');
                isValid = false;
            }

            // Validación de contraseña
            if (field.type === 'password' && value && value.length < 6) {
                this.showFieldError(field, 'Mínimo 6 caracteres');
                isValid = false;
            }
        });

        return isValid;
    }

    /**
     * Mostrar error en campo
     */
    showFieldError(field, message) {
        field.classList.add('is-invalid');
        field.setAttribute('data-error', message);
        
        let errorElement = field.parentElement.querySelector('.form-error');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'form-error';
            field.parentElement.appendChild(errorElement);
        }
        errorElement.textContent = message;
    }

    /**
     * Limpiar error en campo
     */
    clearFieldError(field) {
        field.classList.remove('is-invalid');
        const errorElement = field.parentElement.querySelector('.form-error');
        if (errorElement) {
            errorElement.remove();
        }
    }

    /**
     * Validar email
     */
    isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    /**
     * Configurar interceptor AJAX
     */
    setupAjaxInterceptor() {
        // Interceptar todos los fetch
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            let response = await originalFetch(...args);

            // Si token expirado, refrescar
            if (response.status === 401) {
                await this.refreshToken();
                response = await originalFetch(...args);
            }

            return response;
        };
    }

    /**
     * Realizar petición AJAX
     */
    async api(endpoint, options = {}) {
        const url = `${this.apiBase}${endpoint}`;
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include' // Incluir cookies
        };

        const config = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, config);

            if (!response.ok && response.status !== 401) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            this.showNotification('Error en la solicitud', 'danger');
            return null;
        }
    }

    /**
     * Refrescar token JWT
     */
    async refreshToken() {
        try {
            const response = await this.api('/api/refresh-token', {
                method: 'POST'
            });

            if (response && response.message === 'Token refrescado') {
                console.log('Token refrescado exitosamente');
            }
        } catch (error) {
            console.error('Error refrescando token:', error);
            this.logout();
        }
    }

    /**
     * Cerrar sesión
     */
    logout() {
        window.location.href = '/logout';
    }

    /**
     * Mostrar notificación
     */
    showNotification(message, type = 'info') {
        const alertClass = {
            'success': 'alert-success',
            'danger': 'alert-danger',
            'warning': 'alert-warning',
            'info': 'alert-info'
        }[type] || 'alert-info';

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert ${alertClass}`;
        alertDiv.innerHTML = `
            <span>${message}</span>
            <button type="button" class="btn-close" onclick="this.parentElement.remove()">&times;</button>
        `;

        const container = document.querySelector('[data-alerts]') || document.body;
        container.insertBefore(alertDiv, container.firstChild);

        setTimeout(() => alertDiv.remove(), 5000);
    }

    /**
     * Crear parámetros de formulario
     */
    formToObject(formElement) {
        const formData = new FormData(formElement);
        return Object.fromEntries(formData);
    }

    /**
     * Cargar datos en formulario
     */
    objectToForm(formElement, data) {
        Object.keys(data).forEach(key => {
            const field = formElement.querySelector(`[name="${key}"]`);
            if (field) {
                field.value = data[key];
            }
        });
    }
}

// Inicializar aplicación cuando el DOM está listo
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});

/**
 * Utilidades adicionales
 */

// Formato de moneda
function formatCurrency(value) {
    return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN',
        minimumFractionDigits: 2
    }).format(value);
}

// Formato de fecha
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    return new Intl.DateTimeFormat('es-MX', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

// Spinner/Loading
function showLoading(element) {
    element.classList.add('loading');
    element.disabled = true;
}

function hideLoading(element) {
    element.classList.remove('loading');
    element.disabled = false;
}

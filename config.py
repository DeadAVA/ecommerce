# config.py
import os
import warnings
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
_env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(_env_path, override=True)


def _require_env(name: str, default=None, required: bool = False):
    """Obtiene una variable de entorno y opcionalmente exige que exista."""
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"La variable de entorno {name} es obligatoria en producción")
    if not value and default is not None:
        warnings.warn(
            f"Usando valor por defecto para {name}. Define la variable de entorno en producción.",
            RuntimeWarning
        )
    return value


class Config:
    # Modo de ejecución
    ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
    TESTING = False

    # Seguridad
    SECRET_KEY = _require_env('SECRET_KEY', required=True)

    # ================== BASE DE DATOS ==================
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASS = os.getenv("DB_PASS", "")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "ecommerce")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30,
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "connect_args": {
            "connect_timeout": 5,
            "read_timeout": 30,
            "write_timeout": 30,
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ================== CORREO ==================
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', '1') == '1'
    MAIL_USERNAME = _require_env('MAIL_USERNAME', required=True)
    MAIL_PASSWORD = _require_env('MAIL_PASSWORD', required=True)
    MAIL_DEFAULT_SENDER = (
        os.getenv('MAIL_DEFAULT_NAME', 'A-space Shop'),
        MAIL_USERNAME
    )

    # ================== SEGURIDAD ==================
    FORCE_HTTPS = os.getenv('FORCE_HTTPS', '0') == '1'
    PREFERRED_URL_SCHEME = 'https' if FORCE_HTTPS else 'http'
    SESSION_COOKIE_SECURE = FORCE_HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')
    SESSION_COOKIE_AGE = int(os.getenv('SESSION_COOKIE_AGE', 1800))
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=SESSION_COOKIE_AGE)
    REMEMBER_COOKIE_SECURE = FORCE_HTTPS
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = SESSION_COOKIE_SAMESITE

    # ================== UPLOAD ==================
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/comprobantes')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    # ================== CACHE & RATE LIMIT ==================
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'redis')
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', 'redis://127.0.0.1:6379/0')

    # Si Redis no existe, cae a memoria sin romper la app
    if CACHE_TYPE == 'redis' and not CACHE_REDIS_URL:
        CACHE_TYPE = 'simple'

    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '200/hour')
    RATELIMIT_STORAGE_URI = os.getenv('RATELIMIT_STORAGE_URI', 'memory://')

    # ================== INTEGRACIONES ==================
    POSTAL_NINJA_API_KEY = os.getenv('POSTAL_NINJA_API_KEY')
    COPOMEX_TOKEN = os.getenv('COPOMEX_TOKEN')
    ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',') if h.strip()]

    # ================== STRIPE ==================
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
    STRIPE_CURRENCY = os.getenv('STRIPE_CURRENCY', 'mxn')

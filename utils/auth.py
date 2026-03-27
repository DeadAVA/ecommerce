"""
Sistema de autenticación con JWT y cookies seguras
"""
import jwt
import os
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app, make_response
from config import Config

class JWTAuth:
    """Manejo de tokens JWT"""
    
    # Tiempo de expiración del token (en minutos)
    TOKEN_EXPIRATION = 30
    REFRESH_TOKEN_EXPIRATION = 7 * 24 * 60  # 7 días
    
    @staticmethod
    def _get_jwt_secret_key():
        """Genera una clave segura de 32 bytes para HS256 a partir de SECRET_KEY"""
        secret = current_app.config['SECRET_KEY']
        
        # Si ya tiene 32+ bytes, usarla como está
        if isinstance(secret, bytes) and len(secret) >= 32:
            return secret[:32]
        elif isinstance(secret, str) and len(secret.encode('utf-8')) >= 32:
            return secret.encode('utf-8')[:32]
        
        # Si no, derivar una clave de 32 bytes usando SHA256
        if isinstance(secret, str):
            secret = secret.encode('utf-8')
        return hashlib.sha256(secret).digest()
    
    @staticmethod
    def create_tokens(user_id, user_email):
        """Crea access y refresh tokens"""
        now = datetime.utcnow()
        
        # Access token (corta duración)
        access_payload = {
            'user_id': user_id,
            'email': user_email,
            'type': 'access',
            'iat': now,
            'exp': now + timedelta(minutes=JWTAuth.TOKEN_EXPIRATION)
        }
        
        # Refresh token (larga duración)
        refresh_payload = {
            'user_id': user_id,
            'email': user_email,
            'type': 'refresh',
            'iat': now,
            'exp': now + timedelta(minutes=JWTAuth.REFRESH_TOKEN_EXPIRATION)
        }
        
        access_token = jwt.encode(
            access_payload,
            JWTAuth._get_jwt_secret_key(),
            algorithm='HS256'
        )
        
        refresh_token = jwt.encode(
            refresh_payload,
            JWTAuth._get_jwt_secret_key(),
            algorithm='HS256'
        )
        
        return access_token, refresh_token
    
    @staticmethod
    def verify_token(token, token_type='access'):
        """Verifica y decodifica un token JWT"""
        try:
            payload = jwt.decode(
                token,
                JWTAuth._get_jwt_secret_key(),
                algorithms=['HS256']
            )
            
            # Verificar tipo de token
            if payload.get('type') != token_type:
                return None
            
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def set_token_cookies(response, access_token, refresh_token=None):
        """Configura las cookies con los tokens"""
        secure_flag = current_app.config.get('SESSION_COOKIE_SECURE', False)
        samesite_policy = current_app.config.get('SESSION_COOKIE_SAMESITE', 'Lax')
        # Access token (HttpOnly, Secure, SameSite)
        response.set_cookie(
            'access_token',
            access_token,
            max_age=JWTAuth.TOKEN_EXPIRATION * 60,
            httponly=True,
            secure=secure_flag,
            samesite=samesite_policy,
            domain=None,
            path='/'
        )
        
        # Refresh token (HttpOnly, Secure, SameSite)
        if refresh_token:
            response.set_cookie(
                'refresh_token',
                refresh_token,
                max_age=JWTAuth.REFRESH_TOKEN_EXPIRATION * 60,
                httponly=True,
                secure=secure_flag,
                samesite=samesite_policy,
                domain=None,
                path='/'
            )
        
        return response
    
    @staticmethod
    def clear_token_cookies(response):
        """Elimina las cookies de tokens"""
        response.delete_cookie('access_token', path='/')
        response.delete_cookie('refresh_token', path='/')
        return response


def token_required(f):
    """Decorador para proteger rutas que requieren token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Obtener token de cookie
        token = request.cookies.get('access_token')
        
        if not token:
            return jsonify({'message': 'Token faltante', 'error': 'Unauthorized'}), 401
        
        # Verificar token
        payload = JWTAuth.verify_token(token, 'access')
        
        if not payload:
            return jsonify({'message': 'Token inválido o expirado', 'error': 'Unauthorized'}), 401
        
        # Guardar información del usuario en request context
        request.user_id = payload['user_id']
        request.user_email = payload['email']
        
        return f(*args, **kwargs)
    
    return decorated


def refresh_token_required(f):
    """Decorador para rutas que usan refresh token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Obtener refresh token de cookie
        token = request.cookies.get('refresh_token')
        
        if not token:
            return jsonify({'message': 'Refresh token faltante', 'error': 'Unauthorized'}), 401
        
        # Verificar refresh token
        payload = JWTAuth.verify_token(token, 'refresh')
        
        if not payload:
            return jsonify({'message': 'Refresh token inválido o expirado', 'error': 'Unauthorized'}), 401
        
        # Guardar información del usuario en request context
        request.user_id = payload['user_id']
        request.user_email = payload['email']
        
        return f(*args, **kwargs)
    
    return decorated

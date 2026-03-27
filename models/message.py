from flask import url_for, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
from extensions import mail, db
from models.models import Usuario

def enviar_correo_verificacion(usuario):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(usuario.email, salt='email-confirm')

    usuario.token = token
    usuario.token_expiry = datetime.utcnow() + timedelta(hours=24)
    db.session.commit()

    verification_url = url_for('confirm_email', token=token, _external=True)

    html = f"""
    <html>
    <head>
        <title>Verifica tu cuenta</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; text-align: center; }}
            .button {{
                background-color: #ff6600; color: white; padding: 10px; text-decoration: none; border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <h1>¡Gracias por registrarte!</h1>
        <h2>Por favor verifica tu cuenta</h2>
        <p>Hola <b>{usuario.username}</b>, haz clic en el siguiente enlace para verificar tu cuenta:</p>
        <a href='{verification_url}' class='button'>Verificar cuenta</a>
        <p>Este enlace expirará en 24 horas.</p>
    </body>
    </html>
    """

    msg = Message(subject="Verifica tu cuenta", recipients=[usuario.email])
    msg.body = f"Hola {usuario.username}, visita este enlace para verificar tu cuenta: {verification_url}"
    msg.html = html

    mail.send(msg)
    
    
    
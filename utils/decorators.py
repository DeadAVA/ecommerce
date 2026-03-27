from flask_login import current_user
from functools import wraps
from flask import abort


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, 'admin', False):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def format_fecha(fecha, formato='%d/%m/%Y'):
    if fecha:
        return fecha.strftime(formato)
    return 'Sin fecha'



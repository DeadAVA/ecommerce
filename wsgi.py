import os

# Punto de entrada WSGI para servidores como gunicorn/uwsgi
from app import app

application = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=app.config.get("DEBUG", False))

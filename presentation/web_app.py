import os
from flask import Flask
import queue

# Cola global para SSE
eventos_queue = queue.Queue()
# Estado global para saber la última tarjeta
ultimo_estado = {"uid": "Ninguno", "nombre": "Ninguno", "autorizado": False, "zona": "ESPERA"}

def crear_app():
    # Calculamos las rutas absolutas a templates y static
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Importamos y registramos las rutas
    from presentation.routes import registrar_rutas
    registrar_rutas(app, eventos_queue)

    return app
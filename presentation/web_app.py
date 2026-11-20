import os
from flask import Flask
import queue

# En lugar de una sola cola, tenemos una lista de colas (una por cada cliente/pestaña)
clientes_conectados = []
estado_global = {"ultimo": {"uid": "Ninguno", "nombre": "Ninguno", "autorizado": False, "zona": "ESPERA"}}

def crear_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    from presentation.routes import registrar_rutas
    # Le pasamos la lista de clientes a las rutas
    registrar_rutas(app, clientes_conectados, estado_global)

    return app
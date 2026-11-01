from flask import render_template, Response
import json
import queue
import presentation.web_app as web_app_module

def registrar_rutas(app, eventos_queue):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/stream')
    def stream():
        def event_stream():
            # 1. Enviar el último estado al conectar
            yield f"data: {json.dumps(web_app_module.ultimo_estado)}\n\n"

            while True:
                try:
                    # 2. Esperar nuevos eventos
                    evento = eventos_queue.get(timeout=15)
                    yield f"data: {json.dumps(evento)}\n\n"
                except queue.Empty:
                    yield ": ping\n\n" # Keep-alive

        return Response(event_stream(), mimetype="text/event-stream")
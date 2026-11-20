from flask import render_template, Response
import json
import queue

def registrar_rutas(app, clientes_conectados, estado_global):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/stream')
    def stream():
        def event_stream():
            # 1. Creamos una cola exclusiva para esta pestaña
            mi_cola = queue.Queue()
            clientes_conectados.append(mi_cola)
            print(f"✅ Nueva pestaña conectada. Total activas: {len(clientes_conectados)}")

            try:
                # 2. Enviamos el último estado
                yield f"data: {json.dumps(estado_global['ultimo'])}\n\n"

                while True:
                    try:
                        # 3. Escuchamos SOLO en nuestra cola exclusiva
                        evento = mi_cola.get(timeout=5) # Reducido a 5 seg para detectar desconexiones rápido
                        yield f"data: {json.dumps(evento)}\n\n"
                    except queue.Empty:
                        yield ": ping\n\n"
            finally:
                # 4. Si la pestaña se cierra, liberamos la memoria
                if mi_cola in clientes_conectados:
                    clientes_conectados.remove(mi_cola)
                    print(f"❌ Pestaña desconectada. Total activas: {len(clientes_conectados)}")

        # 5. AÑADIMOS ESTOS HEADERS PARA EVITAR QUE EL NAVEGADOR BLOQUEE EL SSE
        response = Response(event_stream(), mimetype="text/event-stream")
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['X-Accel-Buffering'] = 'no'
        response.headers['Connection'] = 'keep-alive'
        return response
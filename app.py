import os
import threading
import time

from infrastructure.repositories.sqlite_vehiculo_repository import SQLiteVehiculoRepository
from infrastructure.messaging.mqtt_listener import MQTTListener
from application.use_case.procesar_lectura import ProcesarLecturaRFID
import presentation.web_app as web_app

ultimo_uid = ""
ultimo_tiempo = 0

def on_message_mqtt(client, userdata, msg):
    global ultimo_uid, ultimo_tiempo

    uid = msg.payload.decode()
    tiempo_actual = time.time()

    if uid == ultimo_uid and (tiempo_actual - ultimo_tiempo) < 2.0:
        return

    ultimo_uid = uid
    ultimo_tiempo = tiempo_actual

    resultado = caso_uso_procesar.ejecutar(uid)

    print("\n" + "="*40)
    print(f"LECTURA DETECTADA: {resultado['nombre']} -> {resultado['zona']}")
    print("="*40)

    # Guardamos el estado general
    web_app.estado_global["ultimo"] = resultado

    # --- ENVIAMOS A TODAS LAS PESTAÑAS A LA VEZ ---
    print(f"📡 Haciendo Broadcast a {len(web_app.clientes_conectados)} pestañas...")
    for cola_cliente in list(web_app.clientes_conectados):
        cola_cliente.put(resultado)
    print("-" * 40 + "\n")

if __name__ == '__main__':
    print("Iniciando...")
    repositorio = SQLiteVehiculoRepository('rfid.db')
    mqtt_listener = MQTTListener("broker.hivemq.com", "rfid/lecturas_proyecto_igf", on_message_mqtt)
    caso_uso_procesar = ProcesarLecturaRFID(repositorio)

    if not os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        hilo_mqtt = threading.Thread(target=mqtt_listener.iniciar, daemon=True)
        hilo_mqtt.start()

    print("Iniciando servidor Web en http://localhost:5000 ...")
    app = web_app.crear_app()
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
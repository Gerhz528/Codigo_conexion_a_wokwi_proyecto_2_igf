import os
import threading
import time

# Importacion de las capas
from infrastructure.repositories.sqlite_vehiculo_repository import SQLiteVehiculoRepository
from infrastructure.messaging.mqtt_listener import MQTTListener
from application.use_case.procesar_lectura import ProcesarLecturaRFID
import presentation.web_app as web_app

# Variables globales para el Debounce (evitar doble lectura)
ultimo_uid = ""
ultimo_tiempo = 0

def on_message_mqtt(client, userdata, msg):
    global ultimo_uid, ultimo_tiempo

    uid = msg.payload.decode()
    tiempo_actual = time.time()

    # Filtro anti-rebote
    if uid == ultimo_uid and (tiempo_actual - ultimo_tiempo) < 2.0:
        return

    ultimo_uid = uid
    ultimo_tiempo = tiempo_actual

    # EJECUTAMOS EL CASO DE USO
    resultado = caso_uso_procesar.ejecutar(uid)

    # Salida por consola
    print("\n" + "="*40)
    print("LECTURA DE TARJETA RFID DETECTADA")
    print("="*40)
    print(f"UID:        {resultado['uid']}")
    print(f"Nombre:     {resultado['nombre']}")
    print(f"Autorizado: {'SÍ' if resultado['autorizado'] else 'NO'}")
    print(f"Zona:       {resultado['zona']}")
    print("="*40 + "\n")

if __name__ == '__main__':
    print("Iniciando...")
    # --- INYECCIÓN DE DEPENDENCIAS ---

    # 1. Infraestructura
    repositorio = SQLiteVehiculoRepository('rfid.db')
    mqtt_listener = MQTTListener("broker.hivemq.com", "rfid/lecturas_proyecto_igf", on_message_mqtt)

    # 2. Aplicación
    caso_uso_procesar = ProcesarLecturaRFID(repositorio)

    # 3. Arrancar MQTT (evitando duplicados en debug)
    if not os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        hilo_mqtt = threading.Thread(target=mqtt_listener.iniciar, daemon=True)
        hilo_mqtt.start()

    # Como no tenemos Flask ejecutándose, el programa principal se cerraría.
    # Este bucle infinito mantiene la consola viva esperando lecturas.
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCerrando sistema...")
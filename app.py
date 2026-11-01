from flask import Flask
import paho.mqtt.client as mqtt
import json
import threading

app = Flask(__name__)

# --- CONFIGURACIÓN MQTT ---
BROKER = "broker.hivemq.com"
TOPIC_LECTURA = "rfid/lecturas_proyecto_igf"
TOPIC_RESPUESTA = "rfid/respuestas_proyecto_igf"

# --- LÓGICA DEL DOMINIO (SIMULADA POR AHORA) ---
def procesar_uid(uid):
    print(f"UID recibido por MQTT: {uid}")
    # Aquí después irá tu consulta a SQLite
    if uid == "01020304":
        return {"autorizado": True, "zona": "A"}
    else:
        return {"autorizado": False, "zona": None}

# --- EVENTOS MQTT ---
def on_connect(client, userdata, flags, rc):
    print("Conectado al Broker MQTT. Código de resultado:", rc)
    # Nos suscribimos al tema donde Wokwi envía las tarjetas
    client.subscribe(TOPIC_LECTURA)
    print(f"Escuchando en el topic: {TOPIC_LECTURA}")

def on_message(client, userdata, msg):
    # Cuando llega un mensaje de Wokwi
    uid = msg.payload.decode()
    
    # Procesamos el UID
    resultado = procesar_uid(uid)
    
    # Publicamos la respuesta para que Wokwi la lea
    client.publish(TOPIC_RESPUESTA, json.dumps(resultado))
    print(f"Respuesta enviada a {TOPIC_RESPUESTA}: {resultado}")

# --- INICIAR MQTT EN UN HILO APARTE ---
def iniciar_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.loop_forever() # Bucle infinito escuchando mensajes

# --- INICIAR FLASK ---
if __name__ == '__main__':
    # Lanzamos el cliente MQTT en un hilo separado para que no bloquee a Flask
    hilo_mqtt = threading.Thread(target=iniciar_mqtt)
    hilo_mqtt.daemon = True
    hilo_mqtt.start()

    print("Iniciando servidor Flask...")
    app.run(host='0.0.0.0', port=5000)
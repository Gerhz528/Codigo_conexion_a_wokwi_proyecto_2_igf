import paho.mqtt.client as mqtt

class MQTTListener:
    def __init__(self, broker: str, topic: str, on_message_callback):
        self.broker = broker
        self.topic = topic
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = on_message_callback

    def _on_connect(self, client, userdata, flags, rc):
        print(f"📡 MQTT Conectado (código {rc}). Escuchando en {self.topic}")
        client.subscribe(self.topic)

    def iniciar(self):
        self.client.connect(self.broker, 1883, 60)
        self.client.loop_forever()
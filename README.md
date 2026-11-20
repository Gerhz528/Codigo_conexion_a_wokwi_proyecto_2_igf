
```markdown
# Sistema de Control Vehicular RFID Emulado (TrafficFirst)

Sistema de control de acceso que utiliza tecnología RFID para identificar vehículos, determinar su zona de destino mediante reglas de negocio y mostrar la indicación en un semáforo web en tiempo real.

El proyecto implementa un **Hardware Emulado** (Wokwi) comunicándose mediante **MQTT** con un backend en **Python (Flask)** estructurado con **Arquitectura Onion**, y una interfaz web reactiva usando **Server-Sent Events (SSE)**.

##  Arquitectura y Tecnologías

*   **Hardware Emulado:** ESP32 + Lector RC522 en [Wokwi](https://wokwi.com).
*   **Comunicación IoT:** MQTT (Broker público HiveMQ).
*   **Backend:** Python 3.10+, Flask, `paho-mqtt`.
*   **Base de Datos:** SQLite (Consultas SQL nativas sin ORM).
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla) con EventSource (SSE).
*   **Patrón de Diseño:** Arquitectura Onion (Domain-Driven Design).

##  Estructura del Proyecto

```text
├── app.py                        # Punto de entrada (Inyección de Dependencias)
├── init_db.py                    # Script para crear e inicializar la BD SQLite
├── rfid.db                       # Base de datos (se genera automáticamente)
├── requirements.txt              # Dependencias de Python
│
├── domain/                       # Núcleo del negocio (Entidades, Puertos)
├── application/                  # Casos de Uso (Orquestación)
├── infrastructure/               # Adaptadores (SQLite, MQTT)
├── presentation/                 # Flask, Rutas y SSE
├── templates/                    # index.html
└── static/                       # style.css
```

## ️ Requisitos Previos

*   Python 3.10 o superior instalado.
*   Acceso a Internet (para conectarse al broker MQTT y a Wokwi).
*   Navegador web moderno (Chrome, Edge, Firefox).

##  Instalación y Ejecución

Sigue estos pasos para levantar el sistema en tu entorno local:

**1. Clonar el repositorio o descargar los archivos:**
```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

**2. Crear y activar un entorno virtual (venv):**
*   En Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
*   En macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**3. Instalar las dependencias:**
```bash
pip install -r requirements.txt
```
*(Si no tienes el archivo requirements, usa: `pip install flask paho-mqtt`)*

**4. Inicializar la Base de Datos:**
Ejecuta el script para crear las tablas y agregar los vehículos de prueba:
```bash
python init_db.py
```

**5. Ejecutar el servidor backend:**
```bash
python app.py
```
Deberías ver en la consola: `Iniciando servidor Web en http://localhost:5000 ...`

**6. Abrir el Frontend:**
Abre tu navegador web y visita:
 **`http://localhost:5000`**

**7. Simular el Hardware (Wokwi):**
*   Abre el proyecto de Wokwi con el código del ESP32.
*   Dale al botón de "Play" (Iniciar simulación).
*   Espera a que el monitor serie indique "WiFi conectado" y "MQTT conectado".
*   Haz clic en el lector RC522 y selecciona una tarjeta virtual (ej. UID `01020304`).

##  Pruebas Básicas

1.  **Acceso Autorizado:** Pasa la tarjeta `01020304`. El semáforo web debe encender la flecha izquierda (Zona A).
2.  **Acceso Denegado:** Pasa una tarjeta cuyo UID no esté en la base de datos. El semáforo debe encender la luz roja.
3.  **Múltiples Pestañas:** Abre `http://localhost:5000` en dos pestañas distintas. Al pasar una tarjeta, ambas pestañas deben actualizarse al mismo tiempo (Patrón Broadcast).

##  Tópicos MQTT Utilizados

*   **Lectura (Wokwi -> Backend):** `rfid/lecturas_proyecto_igf`
*   **Broker:** `broker.hivemq.com` (Puerto 1883)

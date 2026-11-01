import sqlite3

def crear_base_datos():
    # Conecta (o crea si no existe) el archivo rfid.db
    conn = sqlite3.connect('rfid.db')
    cursor = conn.cursor()

    # Creamos la tabla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehiculos (
            uid TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            zona TEXT NOT NULL,
            autorizado INTEGER NOT NULL
        )
    ''')

    # Limpiamos la tabla por si ejecutas esto varias veces
    cursor.execute('DELETE FROM vehiculos')

    # Insertamos datos de prueba
    # Nota: En Wokwi, los UIDs suelen ser hexadecimales.
    # Usaremos los que tenías de prueba y añadiremos otros.
    vehiculos = [
        ("01020304", "Juan", "A", 1),
        ("55667788", "Toñito", "B", 1),
        ("AABBCCDD", "Roberto", "C", 1),
        ("11223344", "Carlos", "DENEGADO", 0) # Este existe pero está desautorizado
    ]

    cursor.executemany('INSERT INTO vehiculos VALUES (?, ?, ?, ?)', vehiculos)

    conn.commit()
    conn.close()
    print("✅ Base de datos 'rfid.db' creada y poblada con éxito.")

if __name__ == '__main__':
    crear_base_datos()
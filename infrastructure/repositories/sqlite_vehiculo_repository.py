import sqlite3
from domain.ports.i_vehiculo_repository import IVehiculoRepository
from domain.entities.vehiculo import Vehiculo

class SQLiteVehiculoRepository(IVehiculoRepository):
    def __init__(self, db_path: str = 'rfid.db'):
        self.db_path = db_path

    def buscar_por_uid(self, uid: str) -> Vehiculo | None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT nombre, zona, autorizado FROM vehiculos WHERE uid = ?", (uid,))
        fila = cursor.fetchone()
        conn.close()

        if fila:
            return Vehiculo(
                uid=uid,
                nombre=fila[0],
                zona=fila[1],
                autorizado=bool(fila[2])
            )
        return None
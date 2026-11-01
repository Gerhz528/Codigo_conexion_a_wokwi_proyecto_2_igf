from domain.ports.i_vehiculo_repository import IVehiculoRepository

class ProcesarLecturaRFID:
    def __init__(self, repositorio: IVehiculoRepository):
        self.repositorio = repositorio

    def ejecutar(self, uid: str) -> dict:
        vehiculo = self.repositorio.buscar_por_uid(uid)

        if vehiculo and vehiculo.autorizado:
            return {"uid": uid, "nombre": vehiculo.nombre, "autorizado": True, "zona": vehiculo.zona}
        elif vehiculo:
            return {"uid": uid, "nombre": vehiculo.nombre, "autorizado": False, "zona": "DENEGADO"}
        else:
            return {"uid": uid, "nombre": "Desconocido", "autorizado": False, "zona": "DENEGADO"}
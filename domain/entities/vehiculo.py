from dataclasses import dataclass

@dataclass
class Vehiculo:
    uid: str
    nombre: str
    zona: str
    autorizado: bool
from abc import ABC, abstractmethod
from domain.entities.vehiculo import Vehiculo

class IVehiculoRepository(ABC):
    @abstractmethod
    def buscar_por_uid(self, uid: str) -> Vehiculo | None:
        """Busca un vehículo por su UID y lo devuelve, o None si no existe."""
        pass
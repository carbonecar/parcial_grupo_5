"""
Interfaz para el patrón Repository de pagos.
Define el contrato que debe cumplir cualquier implementación de persistencia.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional


class PaymentRepository(ABC):
    """
    Interfaz abstracta para el repositorio de pagos.
    Define las operaciones básicas de persistencia sin especificar cómo se implementan.
    """

    @abstractmethod
    def get_all(self) -> Dict:
        """
        Obtiene todos los pagos.

        Returns:
            Dict: Diccionario con todos los pagos registrados.
        """

    @abstractmethod
    def get_by_id(self, payment_id: str) -> Optional[Dict]:
        """
        Obtiene un pago específico por su ID.

        Args:
            payment_id: ID del pago a obtener.

        Returns:
            Optional[Dict]: Los datos del pago si existe, None si no existe.
        """

    @abstractmethod
    def save(self, payment_id: str, payment_data: Dict) -> None:
        """
        Guarda o actualiza un pago.

        Args:
            payment_id: ID del pago.
            payment_data: Datos del pago a guardar.
        """

    @abstractmethod
    def delete(self, payment_id: str) -> None:
        """
        Elimina un pago.

        Args:
            payment_id: ID del pago a eliminar.
        """

    @abstractmethod
    def exists(self, payment_id: str) -> bool:
        """
        Verifica si un pago existe.

        Args:
            payment_id: ID del pago a verificar.

        Returns:
            bool: True si el pago existe, False en caso contrario.
        """

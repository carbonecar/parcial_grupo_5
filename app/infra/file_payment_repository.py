"""
Implementación del repositorio de pagos usando almacenamiento en archivo JSON.
"""
import json
import os
from typing import Dict, Optional
from app.ports.payment_repository import PaymentRepository


class FilePaymentRepository(PaymentRepository):
    """
    Implementación del repositorio usando archivos JSON para persistencia.
    """
    DATA_PATH = "data.json"

    def __init__(self, data_path: str = DATA_PATH):
        """
        Inicializa el repositorio de archivos.

        Args:
            data_path: Ruta del archivo JSON donde se almacenan los pagos.
        """
        self.data_path = data_path

    def get_all(self) -> Dict:
        """
        Obtiene todos los pagos del archivo JSON.

        Returns:
            Dict: Diccionario vacío si el archivo no existe, los datos si existe.
        """
        if not os.path.isfile(self.data_path):
            return {}

        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def get_by_id(self, payment_id: str) -> Optional[Dict]:
        """
        Obtiene un pago específico por su ID.

        Args:
            payment_id: ID del pago a obtener.

        Returns:
            Optional[Dict]: Los datos del pago si existe, None si no existe.
        """
        all_payments = self.get_all()
        return all_payments.get(payment_id)

    def save(self, payment_id: str, payment_data: Dict) -> None:
        """
        Guarda o actualiza un pago en el archivo JSON.

        Args:
            payment_id: ID del pago.
            payment_data: Datos del pago a guardar.
        """
        all_payments = self.get_all()
        all_payments[str(payment_id)] = payment_data
        self._write_all(all_payments)

    def delete(self, payment_id: str) -> None:
        """
        Elimina un pago del archivo JSON.

        Args:
            payment_id: ID del pago a eliminar.
        """
        all_payments = self.get_all()
        if str(payment_id) in all_payments:
            del all_payments[str(payment_id)]
            self._write_all(all_payments)

    def exists(self, payment_id: str) -> bool:
        """
        Verifica si un pago existe en el archivo JSON.

        Args:
            payment_id: ID del pago a verificar.

        Returns:
            bool: True si el pago existe, False en caso contrario.
        """
        return str(payment_id) in self.get_all()

    def _write_all(self, data: Dict) -> None:
        """
        Escribe todos los pagos en el archivo JSON.

        Args:
            data: Diccionario con todos los pagos.
        """
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

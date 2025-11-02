# pylint: disable=W1514
"""
Módulo para manejar la carga y guardado de pagos en un archivo JSON.
"""
from app.domain.constants import STATUS_PAGADO, STATUS_FALLIDO, STATUS_REGISTRADO, AMOUNT, PAYMENT_METHOD,STATUS
from app.application.strategy_factory import Strategyfactory

# Excepciones de dominio / aplicación
class PaymentAlreadyExistsError(Exception):
    """Excepción lanzada cuando se intenta registrar un pago que ya existe."""

class PaymentNotFoundError(Exception):
    """Excepción lanzada cuando no se encuentra un pago."""

class PaymentValidationError(Exception):
    """Excepción lanzada cuando un pago no cumple con las reglas de validación."""

class PaymentsService:
    """
    Servicio para manejar la lógica de pagos.
    """

    def __init__(self, repository):
        """
        Inicializa el servicio de pagos con un repositorio.

        Args:
            repository: Repositorio para manejar la persistencia de pagos.
        """
        self.repository = repository

    def get_all_payments(self) -> dict:
        """
        Obtiene todos los pagos almacenados.

        Returns:
            dict: Diccionario con todos los pagos.
        """
        return self.repository.get_all()
 
    def register_payment(self, payment_id: str, amount: float, payment_method: str):
        """
        Registra un nuevo pago.
        """
        payments = self.repository.get_all()
        if payment_id in payments:
            raise PaymentAlreadyExistsError(payment_id)

        data = {
            AMOUNT: amount,
            PAYMENT_METHOD: payment_method,
            STATUS: STATUS_REGISTRADO,
        }
        self.repository.save(payment_id, data)

    def update_payment(self, payment_id: str, amount: float, payment_method: str) -> None:
        """
        Actualiza un pago existente. Lanza PaymentNotFoundError si no existe.
        """
        payment = self.repository.get_by_id(payment_id)
        if payment is None:
            raise PaymentNotFoundError(payment_id)

        payment[AMOUNT] = amount
        payment[PAYMENT_METHOD] = payment_method
        self.repository.save(payment_id, payment)

    def pay_payment(self, payment_id: str) -> None:
        """
        Procesa el pago usando el Strategy correspondiente.
        Lanza:
          - PaymentNotFoundError si no existe
          - PaymentValidationError si la regla de negocio falla
        """
        payment = self.repository.get_by_id(payment_id)
        if payment is None:
            raise PaymentNotFoundError(payment_id)

        # obtener strategy (puede lanzar si método no soportado)
        try:
            strategy = Strategyfactory.get_strategy(payment[PAYMENT_METHOD])
        except Exception as e:
            # si Strategyfactory lanza errores inesperados, encapsularlos
            raise PaymentValidationError(f"Error al obtener strategy: {str(e)}")

        # ejecutar la validación/proceso del strategy
        try:
            valid = strategy.process_payment(payment, payment_id)
        except Exception as e:
            # si el strategy falla por alguna razón, encapsulamos como validación
            raise PaymentValidationError(f"Error al procesar pago: {str(e)}")

        if valid:
            payment[STATUS] = STATUS_PAGADO
            self.repository.save(payment_id, payment)
        else:
            payment[STATUS] = STATUS_FALLIDO
            self.repository.save(payment_id, payment)
            raise PaymentValidationError("Monto incorrecto para el metodo de pago seleccionado o existe otro pago registrado por procesar")

    def revert_payment(self, payment_id: str) -> None:
        """
        Cambia de 'FALLIDO' a 'REGISTRADO'.
        Lanza PaymentNotFoundError si el pago no existe.
        """
        payment_data = self.repository.get_by_id(payment_id)
        if payment_data is None:
            raise PaymentNotFoundError(payment_id)
        if payment_data[STATUS] != STATUS_FALLIDO:
            raise PaymentValidationError("Solo se pueden revertir pagos en estado FALLIDO")
        payment_data[STATUS] = STATUS_REGISTRADO
        self.repository.save(payment_id, payment_data)

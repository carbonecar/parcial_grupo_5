"""
factory para obtener la strategy de pago adecuada según el método de pago.
"""
from app.domain.credit_card_payment_strategy import CreditCardPaymentStrategy
from app.domain.paypal_payment_strategy import PayPalPaymentStrategy
from app.infra.file_payment_repository import FilePaymentRepository

class Strategyfactory:
    """
    Factory para obtener la estrategia de pago adecuada.
    """
    _strategies = None

    @staticmethod
    def get_strategy(payment_method):
        """
        Devuelve la estrategia de pago correspondiente al método de pago.
        """

        if Strategyfactory._strategies is None: # lo hacemos lazy para evitar crear el diccionario si no se usa
            Strategyfactory._strategies = {
                    ## No tengo un framework de IOC asi que lo hago en la capa de application
                    "credit_card": CreditCardPaymentStrategy(FilePaymentRepository()),
                    "paypal": PayPalPaymentStrategy(),
            }
        return Strategyfactory._strategies.get(payment_method)
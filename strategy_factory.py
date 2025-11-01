"""
factory para obtener la strategy de pago adecuada según el método de pago.
"""
from credit_card_payment_strategy import CreditCardPaymentStrategy
from paypal_payment_strategy import PayPalPaymentStrategy

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
                    "credit_card": CreditCardPaymentStrategy(),
                    "paypal": PayPalPaymentStrategy(),
            }
        return Strategyfactory._strategies.get(payment_method)
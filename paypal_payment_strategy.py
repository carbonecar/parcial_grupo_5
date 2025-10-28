"""
Estrategia de pago para PayPal.
"""
from payment_strategy import PaymentStrategy

from payments_handler import AMOUNT

class PayPalPaymentStrategy(PaymentStrategy):
    """
    Estrategia de pago para PayPal.
    """
    def process_payment(self, payment_data,payment_id):
        """Procesa el pago con PayPal.
        
        Si el monto es menor a $5000, el pago falla.
        Si el monto es $5000 o más, el pago es exitoso.
        """
        amount=payment_data[AMOUNT]
        if amount < 5000:
            return True
        else:
            return False


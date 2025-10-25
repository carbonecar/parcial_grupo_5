from payment_strategy import PaymentStrategy

class PayPalPaymentStrategy(PaymentStrategy):
    """
    Estrategia de pago para PayPal.
    """
    def process_payment(self, amount: float) -> str:
        """Procesa el pago con PayPal.
        
        Si el monto es menor a $5000, el pago falla.
        Si el monto es $5000 o más, el pago es exitoso.
        """
        if amount < 5000:
            return True
        else:
            return False
        

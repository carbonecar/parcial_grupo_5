# pylint: disable=R0903
"""
    Estrategia de pago con tarjeta de crédito.
"""
from payment_strategy import PaymentStrategy
from payments_handler import STATUS, STATUS_REGISTRADO, STATUS_FALLIDO, save_payment_data, load_all_payments
class CreditCardPaymentStrategy(PaymentStrategy):
    """
        Estrategia de pago con tarjeta de crédito.
    """
    def process_payment(self, payment_data,payment_id):
        """Procesa el pago con tarjeta de crédito.
        
        Si el monto es menor a $10,000, el pago falla.
        Si el monto es $10,000 o más, el pago es exitoso.
        """
        amount=payment_data['amount']
        all_payments=load_all_payments()
        if amount > 10000:
            return False
      
        for pid, pdata in all_payments.items():
            if pid != payment_id and pdata[STATUS] == STATUS_REGISTRADO:
                payment_data[STATUS] = STATUS_FALLIDO
                save_payment_data(payment_id, payment_data)
                return False
        return True

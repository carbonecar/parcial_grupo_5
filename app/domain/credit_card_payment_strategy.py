# pylint: disable=R0903
"""
    Estrategia de pago con tarjeta de crédito.
"""
from app.domain.payment_strategy import PaymentStrategy
from app.ports.payment_repository import PaymentRepository
from app.domain.constants import STATUS_REGISTRADO
class CreditCardPaymentStrategy(PaymentStrategy):

    """
        Estrategia de pago con tarjeta de crédito. 
        Si el monto es menor a $10,000, el pago se aprueba.
        Si el monto es $10,000 o más, el pago se rechaza.
    """

    def __init__(self,repo:PaymentRepository):
        self.repo=repo

    def process_payment(self, payment_data,payment_id):
        """Procesa el pago con tarjeta de crédito.
        
       
        """
        amount=payment_data['amount']
        if amount >= 10000:
            return False

        all_payments=self.repo.get_all()
       # Verifico que no exista otro pago con estado registrado
        for pid, pdata in all_payments.items():
            if pid != payment_id and pdata['status'] == STATUS_REGISTRADO and pdata['payment_method']=='credit_card':
                return False
        return True

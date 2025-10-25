from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    
    @abstractmethod
    def process_payment(self,payment_data,payment_id):
        """Procesa el pago y devuelve el estado del pago."""
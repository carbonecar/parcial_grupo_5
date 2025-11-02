"""
Domain model para el manejo de pagos.
"""

class Pyament:

    def __init__(self, amount: float, payment_method: str, status: str):
        self.amount = amount
        self.payment_method = payment_method
        self.status = status
    
    
from credit_card_payment_strategy import CreditCardPaymentStrategy
from paypal_payment_strategy import PayPalPaymentStrategy

class Strategyfactory:
    @staticmethod
    def get_strategy(payment_method):
        strategies = {
            "credit_card": CreditCardPaymentStrategy(),
            "paypal": PayPalPaymentStrategy(),
        }
        return strategies.get(payment_method)
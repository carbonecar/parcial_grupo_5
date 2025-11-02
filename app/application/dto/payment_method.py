"""
 DTO for payment method enumeration.
 """
from enum import Enum

class PaymentMethod(str, Enum):
    """
    Enumeration of supported payment methods.
    """
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"

"""
 DTO for payment request data.
 """
from pydantic import BaseModel

class PaymentRequest(BaseModel):
    """Data Transfer Object for payment requests."""
    amount: float
    payment_method: str



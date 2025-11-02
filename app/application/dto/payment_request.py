"""
 DTO for payment request data.
 """
from pydantic import BaseModel,Field
from app.application.dto.payment_method import PaymentMethod 
class PaymentRequest(BaseModel):
    """Data Transfer Object for payment requests."""
    amount: float = Field(..., gt=0, description="The amount to be paid.")
    payment_method: PaymentMethod = Field(..., description="The payment method to be used.")

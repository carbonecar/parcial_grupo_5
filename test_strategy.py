
import pytest
from strategy_factory import Strategyfactory
from credit_card_payment_strategy import CreditCardPaymentStrategy
from paypal_payment_strategy import PayPalPaymentStrategy

def test_credit_card_payment_strategy_success():
    """Test para la strategy solamente"""
    strategy = Strategyfactory.get_strategy("credit_card")
    assert isinstance(strategy, CreditCardPaymentStrategy)
    payment_data = { "amount": 5000 }
    payment_id = "test_cc_success"
    result = strategy.process_payment(payment_data, payment_id)
    assert result is True

def test_credit_card_payment_strategy_failure():
    """Prueba para el pago fallido con tarjeta de crédito"""
    strategy = Strategyfactory.get_strategy("credit_card")
    assert isinstance(strategy, CreditCardPaymentStrategy)
    payment_data = { "amount": 15000 }
    payment_id = "test_cc_failure"
    result = strategy.process_payment(payment_data, payment_id)
    assert result is False


def test_paypal_payment_strategy_success():
    """Prueba para el pago exitoso con PayPal"""
    strategy = Strategyfactory.get_strategy("paypal")
    assert isinstance(strategy, PayPalPaymentStrategy)
    payment_data = { "amount": 6000 }
    payment_id = "test_paypal_success"
    result = strategy.process_payment(payment_data, payment_id)
    assert result is False


def test_paypal_payment_strategy_failure():
    """Prueba para el pago fallido con PayPal"""
    strategy = Strategyfactory.get_strategy("paypal")
    assert isinstance(strategy, PayPalPaymentStrategy)
    payment_data = { "amount": 3000 }
    payment_id = "test_paypal_failure"
    result = strategy.process_payment(payment_data, payment_id)
    assert result is True

if __name__ == "__main__":
    pytest.main()
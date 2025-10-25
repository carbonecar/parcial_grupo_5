from payment_strategy import PaymentStrategy

class CreditCardPaymentStrategy(PaymentStrategy):

    def process_payment(self, payment_data,all_payments) -> str:
        """Procesa el pago con tarjeta de crédito.
        
        Si el monto es menor a $10,000, el pago falla.
        Si el monto es $10,000 o más, el pago es exitoso.
        """
        amount=payment_data['amount']
        if amount < 10000:
           return False
        else:
            for pid, pdata in all_payments.items():
                if pid != payment_id and pdata[STATUS] == STATUS_REGISTRADO:
                    payment_data[STATUS] = STATUS_FALLIDO
                    save_payment_data(payment_id, payment_data)
                    return False
            return True
        

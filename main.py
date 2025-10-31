"""
    Servidor de ejemplo para la práctica de FastAPI
"""
from strategy_factory import Strategyfactory
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from config import settings
from credit_card_payment_strategy import CreditCardPaymentStrategy
from paypal_payment_strategy import PayPalPaymentStrategy
from payments_handler import (
    DATA_PATH,
    STATUS,
    AMOUNT,
    PAYMENT_METHOD,
    STATUS_REGISTRADO,
    STATUS_PAGADO,
    STATUS_FALLIDO,
    load_all_payments,
    load_payment,
    save_payment_data,
    save_payment,
)

load_dotenv()

app = FastAPI(
    title=settings.app_name,
    description="Parcial Grupo 5 - Ingeniería de Software",
    version=settings.api_version
)


@app.get("/payments")
async def obtener_pagos():
    """
    Obtiene todos los pagos del sistema.
    """
    if not os.path.isfile(DATA_PATH):
        return {"payments": {}}
    payments = load_all_payments()
    return {"payments": payments}


### POST /payments/{payment_id}
@app.post("/payments/{payment_id}")
async def register_payment(payment_id: str, amount: float, payment_method: str):
    """
    Registra un pago con su información.
    """
    # Verificar si el pago ya existe
    if os.path.isfile(DATA_PATH):
        payments = load_all_payments()
        if payment_id in payments:
            raise HTTPException(status_code=400, detail=f"El pago con ID {payment_id} ya existe.")
    
    save_payment(payment_id, amount, payment_method, STATUS_REGISTRADO)
    return {"message": f"Pago con ID {payment_id} registrado exitosamente."}




@app.post("/payments/{payment_id}/update")
async def update_payment(payment_id: str, amount: float, payment_method: str):
    """
    Actualiza la información de un pago existente.
    """
    payment_data = load_payment(payment_id)
    payment_data[AMOUNT] = amount
    payment_data[PAYMENT_METHOD] = payment_method
    save_payment_data(payment_id, payment_data)
    return {"message": f"Pago con ID {payment_id} actualizado exitosamente."}


@app.post("/payments/{payment_id}/pay")
async def pay_payment(payment_id: str):
    """
    Marca un pago como pagado.
    Para el Método de Pago 2 (PayPal) se verifica que el monto sea menor de $5000.
    Si el pago con PayPal es <5000 se marca como PAGADO.
    Para el método de pago 1 (Tarjeta de Crédito) se verifica que el monto sea menor de $10,000.
    Si el pago con Tarjeta de Crédito es <10,000 se marca como PAGADO
    """

    payment_data = load_payment(payment_id)
    payment_strategy=Strategyfactory.get_strategy(payment_data[PAYMENT_METHOD])

    validacion_monto=payment_strategy.process_payment(payment_data,payment_id)
    ## verifico que si el metodo de pago es tarjeta de credito el monto no sea menor a 10.000 y Validamos que no exista mas de un pago con estado registrado
    if validacion_monto:
        payment_data[STATUS] = STATUS_PAGADO
        save_payment_data(payment_id, payment_data)
        return {"message": f"Pago con ID {payment_id} pagado exitosamente."}
    else:
        payment_data[STATUS] = STATUS_FALLIDO
        save_payment_data(payment_id, payment_data)
        return {"message": f"Pago con ID {payment_id} fallido: monto insuficiente para el metodo de pago seleccionado o existe otro pago registrado por procesar."}


@app.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str):
    """
    Revierte un pago al estado registrado.
    """
    payment_data = load_payment(payment_id)
    payment_data[STATUS] = STATUS_REGISTRADO
    save_payment_data(payment_id, payment_data)
    return {"message": f"Pago con ID {payment_id} revertido al estado registrado."}

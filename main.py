"""
    Servidor de ejemplo para la práctica de FastAPI
"""
import json
import os
from fastapi import FastAPI, HTTPException

STATUS = "status"
AMOUNT = "amount"
PAYMENT_METHOD = "payment_method"

STATUS_REGISTRADO = "REGISTRADO"
STATUS_PAGADO = "PAGADO"
STATUS_FALLIDO = "FALLIDO"

DATA_PATH = "data.json"


app = FastAPI(
    title="Parcial Grupo 5",
    description="Parcial Grupo 5 - Ingeniería de Software",
    version="1.0.0"
)

def load_all_payments():
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data


def save_all_payments(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)


def load_payment(payment_id):
    data = load_all_payments()[payment_id]
    return data


def save_payment_data(payment_id, data):
    all_data = load_all_payments()
    all_data[str(payment_id)] = data
    save_all_payments(all_data)


def save_payment(payment_id, amount, payment_method, status):
    data = {
        AMOUNT: amount,
        PAYMENT_METHOD: payment_method,
        STATUS: status,
    }
    save_payment_data(payment_id, data)
    
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
    Si el pago con PayPal es >= 5000 se marca como PAGADO.
    """
    payment_data = load_payment(payment_id)
    amount = float(payment_data.get(AMOUNT, 0))
    method = str(payment_data.get(PAYMENT_METHOD, "")).strip().lower()

    # Considerar tanto "2" como "paypal" como identificadores del método PayPal
    if method in ("2", "paypal"):
        if amount >= 5000.0:
            pass

@app.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str):
    """
    Revierte un pago al estado registrado.
    """
    payment_data = load_payment(payment_id)
    payment_data[STATUS] = STATUS_REGISTRADO
    save_payment_data(payment_id, payment_data)
    return {"message": f"Pago con ID {payment_id} revertido al estado registrado."}

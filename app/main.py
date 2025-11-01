"""
    Servidor de ejemplo para la práctica de FastAPI
"""
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from app.application.strategy_factory import Strategyfactory
from app.infra.file_payment_repository import FilePaymentRepository

from app.application.payments_handler import (
    STATUS,
    AMOUNT,
    PAYMENT_METHOD,
    STATUS_REGISTRADO,
    STATUS_PAGADO,
    STATUS_FALLIDO,
)
from config import settings

load_dotenv()

# Instancia global del repositorio
repository = FilePaymentRepository()

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
    payments = repository.get_all()
    return {"payments": payments}


@app.post("/payments/{payment_id}")
async def register_payment(payment_id: str, amount: float, payment_method: str):
    """
    Registra un pago con su información.
    """
    # Verificar si el pago ya existe
    payments = repository.get_all()
    if payment_id in payments:
        raise HTTPException(status_code=400, detail=f"El pago con ID {payment_id} ya existe.")
    repository.save(payment_id, {"amount": amount, "payment_method": payment_method, "status": STATUS_REGISTRADO})
    return {"message": f"Pago con ID {payment_id} registrado exitosamente."}


@app.post("/payments/{payment_id}/update")
async def update_payment(payment_id: str, amount: float, payment_method: str):
    """
    Actualiza la información de un pago existente.
    """
    payment_data = repository.get_by_id(payment_id)
    if payment_data is None:
        raise HTTPException(status_code=404, detail=f"Pago con ID {payment_id} no encontrado")

    payment_data[AMOUNT] = amount
    payment_data[PAYMENT_METHOD] = payment_method
    strategy=Strategyfactory.get_strategy(payment_method)
    if strategy is None:
        raise HTTPException(status_code=400, detail=f"Método de pago {payment_method} no soportado.")
    if not strategy.process_payment(payment_data, payment_id):
        raise HTTPException(status_code=400, detail=f"El pago con ID {payment_id} no es válido con el método de pago {payment_method}.")
    repository.save(payment_id, payment_data)
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


    payment_data = repository.get_by_id(payment_id)
    if payment_data is None:
        raise HTTPException(status_code=404, detail=f"Pago con ID {payment_id} no encontrado")

    payment_strategy=Strategyfactory.get_strategy(payment_data[PAYMENT_METHOD])

    validacion_monto = payment_strategy.process_payment(payment_data, payment_id)

    if validacion_monto:
        payment_data[STATUS] = STATUS_PAGADO
        repository.save(payment_id, payment_data)
        return {"message": f"Pago con ID {payment_id} pagado exitosamente."}
    else:
        payment_data[STATUS] = STATUS_FALLIDO
        repository.save(payment_id, payment_data)
        return {"message": f"Pago con ID {payment_id} fallido: monto insuficiente para el metodo de pago seleccionado o existe otro pago registrado por procesar."}


@app.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str):
    """
    Revierte un pago al estado registrado.
    """
    payment_data = repository.get_by_id(payment_id)
    if payment_data is None:
        raise HTTPException(status_code=404, detail=f"Pago con ID {payment_id} no encontrado")

    payment_data[STATUS] = STATUS_REGISTRADO
    repository.save(payment_id, payment_data)
    return {"message": f"Pago con ID {payment_id} revertido al estado registrado."}

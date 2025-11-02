"""
Payment routes for managing payments.
"""
# pylint: disable=raise-missing-from
from fastapi import APIRouter,Depends, HTTPException,status
from app.infra.file_payment_repository import FilePaymentRepository
from app.application.payments_service import PaymentsService, PaymentAlreadyExistsError,PaymentNotFoundError,PaymentValidationError
from app.domain.constants import STATUS_REGISTRADO,STATUS
from app.application.dto.payment_request import PaymentRequest
router = APIRouter(tags=["Payments"])
repository = FilePaymentRepository()

def get_payment_service():
    """
    Proporciona una instancia de PaymentsService con el repositorio de archivos.
    """
    return PaymentsService(FilePaymentRepository())

@router.get("/payments")
async def obtener_pagos(payments_service: PaymentsService = Depends(get_payment_service)):
    """
    Obtiene todos los pagos del sistema.
    """
    payments = payments_service.get_all_payments()
    return {"payments": payments}


@router.post("/payments/{payment_id}",status_code=status.HTTP_201_CREATED)
async def register_payment(payment_id: str,payment:PaymentRequest,payments_service: PaymentsService = Depends(get_payment_service)):
    """
    Registra un pago con su información.
    """
    try:
        payments_service.register_payment(payment_id, payment.amount, payment.payment_method)
        return {"message": f"Pago con ID {payment_id} registrado exitosamente."}
    except PaymentAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El pago con ID {payment_id} ya existe."
        )



@router.post("/payments/{payment_id}/update",status_code=status.HTTP_200_OK)
async def update_payment(payment_id: str, payment: PaymentRequest,payment_service:PaymentsService = Depends(get_payment_service)):
    """
    Actualiza la información de un pago existente.
    """
    try:
        payment_service.update_payment(payment_id, payment.amount, payment.payment_method)
        return {"message": f"Pago con ID {payment_id} actualizado exitosamente."}
    except PaymentNotFoundError:
        raise HTTPException(status_code=404, detail=f"Pago con ID {payment_id} no encontrado")


@router.post("/payments/{payment_id}/pay")
async def pay_payment(payment_id: str,payments_service: PaymentsService = Depends(get_payment_service)):
    """
    Procesa el pago si cummple con las reglas de dominio.
    """


    try:
        payments_service.pay_payment(payment_id)
        return {"message": f"Pago con ID {payment_id} pagado exitosamente."}
    except PaymentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pago con ID {payment_id} no encontrado"
        )
    except PaymentValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

@router.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str, payments_service: PaymentsService = Depends(get_payment_service)):
    """
    Revierte un pago al estado registrado.
    """
    try:
        payments_service.revert_payment(payment_id)
        return {"message": f"Pago con ID {payment_id} revertido al estado registrado."}
    except PaymentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pago con ID {payment_id} no encontrado"
        )

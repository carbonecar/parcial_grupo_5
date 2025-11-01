# pylint: disable=W1514
"""
Módulo para manejar la carga y guardado de pagos en un archivo JSON.
"""
import json

STATUS = "status"
AMOUNT = "amount"
PAYMENT_METHOD = "payment_method"

STATUS_REGISTRADO = "REGISTRADO"
STATUS_PAGADO = "PAGADO"
STATUS_FALLIDO = "FALLIDO"

DATA_PATH = "data.json"



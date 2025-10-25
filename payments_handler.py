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

def load_all_payments():
    """Carga todos los pagos desde el archivo de datos."""
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data


def save_all_payments(data):
    """Guarda todos los pagos en el archivo de datos."""
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)


def load_payment(payment_id):
    """Carga un pago específico por su ID."""
    data = load_all_payments()[payment_id]
    return data


def save_payment_data(payment_id, data):
    """Guarda los datos de un pago específico por su ID."""
    all_data = load_all_payments()
    all_data[str(payment_id)] = data
    save_all_payments(all_data)


def save_payment(payment_id, amount, payment_method, status):
    """Guarda un nuevo pago con su información."""
    data = {
        AMOUNT: amount,
        PAYMENT_METHOD: payment_method,
        STATUS: status,
    }
    save_payment_data(payment_id, data)
"""
    Servidor de ejemplo para la práctica de FastAPI
"""
import json
import os
from pydantic import BaseModel
from fastapi import FastAPI

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

### metdos de prueba
@app.get("/")
async def prueba_root():
    """
    Endpoint de prueba en la raíz
    """
    return {"message": "Accediste al endpoint de prueba"}


@app.get("/files")
async def listar_archivos():
    """
    Develve los archivos del directorio
    """
    archivos = os.listdir("./files")
    return {"archivos": archivos}

@app.get("/files/{nombre_archivo}")
async def leer_archivo(nombre_archivo: str):
    """
    Lee el contenido de un archivo específico
    """
    ruta_archivo = os.path.join("./files", nombre_archivo)

    if not os.path.isfile(ruta_archivo):
        return {"error": "El archivo no existe"}

    with open(ruta_archivo, "r") as archivo:
        contenido = archivo.read()    
    return {"nombre_archivo": nombre_archivo, "contenido": contenido}





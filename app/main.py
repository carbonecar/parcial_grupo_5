"""
    Servidor de ejemplo para la práctica de FastAPI
"""
from dotenv import load_dotenv
from fastapi import FastAPI
from app.infra.file_payment_repository import FilePaymentRepository
from app.api.payment_routes import router as payment_router
from config import settings

load_dotenv()

# Instancia global del repositorio
repository = FilePaymentRepository()

app = FastAPI(
    title=settings.app_name,
    description="Parcial Grupo 5 - Ingeniería de Software",
    version=settings.api_version
)

app.include_router(payment_router)

@app.get("/health")
async def health():
    """Endpoint raíz que devuelve un mensaje de bienvenida."""
    return {"message": "Welcome to the Payments API!"}
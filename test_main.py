# test para main.py
import os
import pytest
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
@pytest.fixture(scope="module", autouse=True)

def setup_and_teardown():
    """Fixture para configurar y limpiar el entorno de pruebas."""
    # Setup: Crear un archivo de datos de prueba antes de las pruebas
    test_data = {
        "1": {
            "amount": 100,
            "payment_method": "credit_card",
            "status": "PAGADO"
        },
        "2": {
            "amount": 50,
            "payment_method": "paypal",
            "status": "FALLIDO"
        }
    }
    with open("data.json", "w") as f:
        import json
        json.dump(test_data, f)
    yield
    # Teardown: Eliminar el archivo de datos de prueba después de las pruebas
    os.remove("data.json")

def test_obtener_pagos():
    """Prueba para el endpoint GET /payments"""
    response = client.get("/payments")
    assert response.status_code == 200
    data = response.json()
    assert "payments" in data
    assert len(data["payments"]) == 2
    assert data["payments"]["1"]["amount"] == 100
    assert data["payments"]["1"]["payment_method"] == "credit_card"
    assert data["payments"]["1"]["status"] == "PAGADO"
    assert data["payments"]["2"]["amount"] == 50
    assert data["payments"]["2"]["payment_method"] == "paypal"
    assert data["payments"]["2"]["status"] == "FALLIDO"




# Nota: Asegurarse de que el directorio ./files exista antes de ejecutar las pruebas
if __name__ == "__main__":
    pytest.main()
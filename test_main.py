# test para main.py
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
    ## generamos un data.json vacio
    with open("data.json", "w") as f:
        json.dump({}, f)

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

def test_register_existing_payment():
    #evita registrar un pago con un ID ya existente
    response = client.post(
        "/payments/1",
        params={"amount": 999, "payment_method": "debit_card"}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"].startswith("El pago con ID") and "ya existe" in data["detail"]
    
def test_register_payment():
    """Prueba para el endpoint POST /payments/{payment_id}"""
    response = client.post("/payments/3", params={"amount": 200, "payment_method": "credit_card"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Pago con ID 3 registrado exitosamente."
    # Verificar que el pago se haya guardado correctamente
    response = client.get("/payments")
    payments = response.json()["payments"]
    assert "3" in payments
    assert payments["3"]["amount"] == 200
    assert payments["3"]["payment_method"] == "credit_card"
    assert payments["3"]["status"] == "REGISTRADO"

def test_update_payment():
    """Prueba para el endpoint POST /payments/{payment_id}/update"""
    response = client.post("/payments/1/update", params={"amount": 150, "payment_method": "paypal"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Pago con ID 1 actualizado exitosamente."
    # Verificar que el pago se haya actualizado correctamente
    response = client.get("/payments")
    payments = response.json()["payments"]
    assert payments["1"]["amount"] == 150
    assert payments["1"]["payment_method"] == "paypal"


# Nota: Asegurarse de que el directorio ./files exista antes de ejecutar las pruebas
if __name__ == "__main__":
    pytest.main()
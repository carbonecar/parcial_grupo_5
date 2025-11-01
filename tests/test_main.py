# test para main.py
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.infra.file_payment_repository import FilePaymentRepository
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
        json.dump(test_data, f)
    yield
    # Teardown: Eliminar el archivo de datos de prueba después de las pruebas
    # generamos un data.json vacio
    with open("data.json", "w") as f:
        json.dump({}, f)


@pytest.fixture
def repository():
    """Fixture para proporcionar una instancia del repositorio con datos limpios."""
    # Reinicializar datos antes de cada test
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
        json.dump(test_data, f)

    repo = FilePaymentRepository("data.json")
    yield repo

    # Limpiar después del test
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


# ============= Tests del Repositorio =============

def test_repository_get_all(repository):
    """Prueba que get_all() retorna todos los pagos."""
    all_payments = repository.get_all()
    assert isinstance(all_payments, dict)
    assert "1" in all_payments
    assert "2" in all_payments
    assert len(all_payments) == 2


def test_repository_get_by_id(repository):
    """Prueba que get_by_id() retorna un pago específico."""
    payment = repository.get_by_id("1")
    assert payment is not None
    assert payment["amount"] == 100
    assert payment["payment_method"] == "credit_card"
    assert payment["status"] == "PAGADO"


def test_repository_get_by_id_nonexistent(repository):
    """Prueba que get_by_id() retorna None si no existe el pago."""
    payment = repository.get_by_id("999")
    assert payment is None


def test_repository_save_new(repository):
    """Prueba que save() guarda un nuevo pago."""
    new_payment = {
        "amount": 250,
        "payment_method": "credit_card",
        "status": "REGISTRADO"
    }
    repository.save("10", new_payment)

    # Verificar que se guardó correctamente
    saved_payment = repository.get_by_id("10")
    assert saved_payment is not None
    assert saved_payment["amount"] == 250
    assert saved_payment["payment_method"] == "credit_card"


def test_repository_save_update(repository):
    """Prueba que save() actualiza un pago existente."""
    updated_payment = {
        "amount": 200,
        "payment_method": "paypal",
        "status": "PAGADO"
    }
    repository.save("1", updated_payment)

    # Verificar que se actualizó correctamente
    saved_payment = repository.get_by_id("1")
    assert saved_payment["amount"] == 200
    assert saved_payment["payment_method"] == "paypal"


def test_repository_exists(repository):
    """Prueba que exists() verifica si un pago existe."""
    assert repository.exists("1") is True
    assert repository.exists("2") is True
    assert repository.exists("999") is False


def test_repository_delete(repository):
    """Prueba que delete() elimina un pago."""
    # Verificar que existe
    assert repository.exists("1") is True

    # Eliminar
    repository.delete("1")

    # Verificar que ya no existe
    assert repository.exists("1") is False
    assert repository.get_by_id("1") is None


def test_repository_delete_nonexistent(repository):
    """Prueba que delete() no falla al eliminar un pago inexistente."""
    # No debe lanzar excepción
    repository.delete("999")
    assert repository.exists("999") is False


# Nota: Asegurarse de que el directorio ./files exista antes de ejecutar las pruebas
if __name__ == "__main__":
    pytest.main()
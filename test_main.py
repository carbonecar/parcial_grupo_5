# test para main.py
from fastapi.testclient import TestClient
from main import app
import os
import pytest
client = TestClient(app)
@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup: Crear el directorio ./files si no existe
    if not os.path.exists("./files"):
        os.makedirs("./files")
    yield
    # Teardown: Eliminar todos los archivos creados durante las pruebas
    for filename in os.listdir("./files"):
        file_path = os.path.join("./files", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
def test_prueba_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Accediste al endpoint de prueba"}
def test_listar_archivos_empty():
    response = client.get("/files")
    assert response.status_code == 200
    assert response.json() == {"archivos": []}

def test_leer_archivo_no_existe():
    response = client.get("/files/no_existe.txt")
    assert response.status_code == 200
    assert response.json() == {"error": "El archivo no existe"}

# Nota: Asegurarse de que el directorio ./files exista antes de ejecutar las pruebas
if __name__ == "__main__":
    pytest.main()
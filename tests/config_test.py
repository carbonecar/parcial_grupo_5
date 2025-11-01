# tests/conftest.py
import sys
from pathlib import Path

# agregar la raíz del proyecto al sys.path
ROOT = Path(__file__).resolve().parents[1]  # carpeta que contiene app/
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

"""
Configuración centralizada de la aplicación
"""
import os
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"

# Asegurar que existe data/
DATA_DIR.mkdir(exist_ok=True)

# Versión de la aplicación
APP_VERSION = "2.0.0"
APP_NAME = "Smart Reports - Instituto Hutchison Ports"

# Configuración de la UI
UI_CONFIG = {
    "appearance_mode": "dark",  # "dark" o "light"
    "default_color_theme": "blue",
    "window_size": "1400x900",
}

# Usuarios por defecto (desarrollo)
DEFAULT_USERS = {
    'admin': {'password': '1234', 'role': 'Administrador'},
    'usuario': {'password': 'pass', 'role': 'Operador'},
    'demo': {'password': 'demo', 'role': 'Usuario Demo'}
}

# Configuración de importación Excel
EXCEL_CONFIG = {
    "max_rows": 10000,
    "chunk_size": 500,
    "encoding": "utf-8"
}

# Configuración de reportes PDF
PDF_CONFIG = {
    "page_size": "letter",
    "margins": {"top": 0.5, "bottom": 0.5, "left": 0.5, "right": 0.5},
    "font_family": "Helvetica"
}

# Configuración de gráficos D3.js
D3_CONFIG = {
    "http_server_port": 8050,
    "cache_enabled": True,
    "temp_dir": "smartreports_d3_charts"
}

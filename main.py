"""
SMART REPORTS - INSTITUTO HUTCHISON PORTS
MainActivity - Punto de entrada (Android Studio style)
Versión 2.1 - Android Studio Architecture
"""
import sys
import os
from pathlib import Path

# Configurar paths
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import customtkinter as ctk

# Android Studio structure imports - Importaciones corregidas
from src.main.res.config.settings import UI_CONFIG, APP_NAME
from src.main.python.ui.activities.ventana_login import LoginWindow
from src.main.python.ui.activities.ventana_principal_view import VentanaPrincipalView as MainWindow


def main():
    """Función principal de la aplicación"""
    # Configurar CustomTkinter
    ctk.set_appearance_mode(UI_CONFIG["appearance_mode"])
    ctk.set_default_color_theme(UI_CONFIG["default_color_theme"])

    # Crear ventana raíz
    root = ctk.CTk()

    # Variable para almacenar usuario autenticado
    authenticated_user = {'username': None, 'role': None}

    def on_login_success(username, role):
        """Callback ejecutado cuando el login es exitoso"""
        authenticated_user['username'] = username
        authenticated_user['role'] = role

        # Crear ventana principal
        app = MainWindow(root, username=username, user_role=role)
        print(f"✓ Usuario autenticado: {username} - Rol: {role}")

    # Mostrar login
    login_window = LoginWindow(root, on_login_success)

    # Iniciar loop principal
    root.mainloop()


if __name__ == "__main__":
    print(f"🚀 Iniciando {APP_NAME}")
    main()

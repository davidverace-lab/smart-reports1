"""
SMART REPORTS - INSTITUTO HUTCHISON PORTS
Punto de entrada principal - VERSIÓN MODERNA
Versión 2.0
"""

import sys
import os

# Agregar el directorio padre al path para imports absolutos
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from smart_reports.ui.login_window import LoginWindow
from smart_reports.ui.main_window_modern import MainWindow


def main():
    """Función principal de la aplicación - Versión Moderna"""
    # Configurar CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # Crear ventana raíz
    root = ctk.CTk()

    # Variable para almacenar usuario autenticado
    authenticated_user = {'username': None}

    def on_login_success(username):
        """Callback ejecutado cuando el login es exitoso"""
        authenticated_user['username'] = username

        # Determinar rol según usuario (puedes expandir esto con BD)
        user_roles = {
            'admin': 'Administrador',
            'usuario': 'Operador',
            'demo': 'Usuario Demo'
        }
        user_role = user_roles.get(username.lower(), 'Usuario')

        # Crear ventana principal después del login exitoso
        app = MainWindow(root, username=username.title(), user_role=user_role)
        # Opcional: Mostrar mensaje de bienvenida
        print(f"Usuario autenticado: {username} - Rol: {user_role}")

    # Mostrar primero la pantalla de login
    login_window = LoginWindow(root, on_login_success)

    # Iniciar loop principal
    root.mainloop()


if __name__ == "__main__":
    main()

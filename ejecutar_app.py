"""
Script mejorado para ejecutar Smart Reports
Maneja diferentes estructuras de directorio
"""
import sys
import os

# Detectar la estructura del directorio y ajustar el path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Si estamos en un subdirectorio duplicado, subir un nivel
if os.path.basename(current_dir) == 'smart-reports1-main':
    parent = os.path.dirname(current_dir)
    if os.path.basename(parent) == 'smart-reports1-main':
        print(f"⚠️  Detectado directorio duplicado: {current_dir}")
        print(f"   Usando directorio padre: {parent}")
        current_dir = parent

# Agregar al path
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print(f"✓ Directorio de trabajo: {current_dir}")
print(f"✓ Python path configurado correctamente")
print("")

# Ahora importar y ejecutar la aplicación
import customtkinter as ctk
from interfaz.ventanas.ventana_login import LoginWindow
from interfaz.ventanas.ventana_principal import MainWindow


def main():
    """Función principal de la aplicación"""
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

        # Determinar rol según usuario
        user_roles = {
            'admin': 'Administrador',
            'usuario': 'Operador',
            'demo': 'Usuario Demo'
        }
        user_role = user_roles.get(username.lower(), 'Usuario')

        # Crear ventana principal
        app = MainWindow(root, username=username.title(), user_role=user_role)
        print(f"✓ Usuario autenticado: {username} - Rol: {user_role}")

    # Mostrar login
    login_window = LoginWindow(root, on_login_success)

    # Iniciar loop
    root.mainloop()


if __name__ == "__main__":
    main()

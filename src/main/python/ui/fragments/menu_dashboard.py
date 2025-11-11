"""
MenuDashboard - Módulo de interfaz para Dashboard
Separado de ventana principal para mejor organización
"""
import customtkinter as ctk
from src.main.python.ui.fragments.dashboard.panel_dashboards_gerenciales import DashboardsGerencialesPanel


def show_dashboard_menu(parent, db_connection, username, user_role):
    """
    Mostrar menú de Dashboard

    Args:
        parent: Widget padre donde se mostrará el panel
        db_connection: Conexión a base de datos
        username: Nombre del usuario
        user_role: Rol del usuario

    Returns:
        Panel de dashboard creado
    """
    if not db_connection:
        return _show_error(parent, "No hay conexión a la base de datos")

    # Información del usuario
    usuario_info = {
        "nombre": username,
        "rol": user_role
    }

    # Crear panel de dashboards gerenciales
    panel = DashboardsGerencialesPanel(
        parent,
        db_connection=db_connection,
        usuario_actual=usuario_info
    )

    return panel


def _show_error(parent, message):
    """Mostrar mensaje de error"""
    error_frame = ctk.CTkFrame(parent, fg_color='transparent')

    error_label = ctk.CTkLabel(
        error_frame,
        text=f'⚠️ {message}\n\nPor favor verifica la configuración.',
        font=('Montserrat', 18),
        text_color='#ff6b6b'
    )
    error_label.pack(expand=True)

    return error_frame

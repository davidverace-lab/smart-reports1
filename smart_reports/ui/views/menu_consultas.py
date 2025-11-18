"""
MenuConsultas - Módulo de interfaz para Consultas
Separado de ventana principal para mejor organización
"""
from smart_reports.ui.views.panel_consultas import PanelConsultas


def show_consultas_menu(parent, db_connection):
    """
    Mostrar menú de consultas

    Args:
        parent: Widget padre donde se mostrará el panel
        db_connection: Conexión a base de datos

    Returns:
        Panel de consultas completo con todas las funcionalidades
    """
    if not db_connection:
        from .menu_dashboard import _show_error
        return _show_error(parent, "No hay conexión a la base de datos")

    # Crear cursor si no existe
    cursor = db_connection.cursor() if db_connection else None

    # Crear panel de consultas completo
    panel = PanelConsultas(
        parent,
        db_connection=db_connection,
        cursor=cursor
    )

    return panel

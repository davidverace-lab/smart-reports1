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
    # Crear cursor si existe conexión
    cursor = db_connection.cursor() if db_connection else None

    # Crear panel de consultas completo (funciona con o sin BD)
    panel = PanelConsultas(
        parent,
        db_connection=db_connection,
        cursor=cursor
    )

    return panel

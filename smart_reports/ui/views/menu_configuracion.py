"""
MenuConfiguracion - Módulo de interfaz para Configuración
Separado de ventana principal para mejor organización
"""
from src.main.python.ui.fragments.configuracion.panel_configuracion import ConfiguracionPanel


def show_configuracion_menu(parent, db_connection, cursor, db_instance):
    """
    Mostrar menú de configuración

    Args:
        parent: Widget padre donde se mostrará el panel
        db_connection: Conexión a base de datos
        cursor: Cursor de base de datos
        db_instance: Instancia de DatabaseConnection

    Returns:
        Panel de configuración creado
    """
    if not db_connection:
        from .menu_dashboard import _show_error
        return _show_error(parent, "No hay conexión a la base de datos")

    # Crear panel de configuración (solo necesita db_connection)
    panel = ConfiguracionPanel(
        parent,
        db_connection=db_connection
    )

    return panel

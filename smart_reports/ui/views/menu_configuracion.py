"""
MenuConfiguracion - Módulo de interfaz para Configuración
Separado de ventana principal para mejor organización
"""
from smart_reports.ui.views.configuracion.panel_configuracion import ConfiguracionPanel


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
    # Crear panel de configuración (funciona con o sin BD)
    panel = ConfiguracionPanel(
        parent,
        db_connection=db_connection
    )

    return panel

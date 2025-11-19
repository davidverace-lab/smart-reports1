"""
MenuActualizar - Módulo de interfaz para Actualización/Importación
Separado de ventana principal para mejor organización
"""
from smart_reports.ui.views.configuracion.panel_importacion_datos import PanelImportacionDatos


def show_actualizar_menu(parent, db_connection, file_controller):
    """
    Mostrar menú de actualización/importación de datos

    Args:
        parent: Widget padre donde se mostrará el panel
        db_connection: Conexión a base de datos
        file_controller: Controller para manejar archivos

    Returns:
        Panel de importación creado
    """
    # Crear panel de importación (funciona con o sin BD)
    panel = PanelImportacionDatos(
        parent,
        db_connection=db_connection
    )

    return panel

"""
MenuConsultas - Módulo de interfaz para Consultas
Separado de ventana principal para mejor organización
"""
import customtkinter as ctk
from src.main.res.config.themes import HUTCHISON_COLORS
from src.main.res.config.gestor_temas import get_theme_manager


def show_consultas_menu(parent, db_connection):
    """
    Mostrar menú de consultas

    Args:
        parent: Widget padre donde se mostrará el panel
        db_connection: Conexión a base de datos

    Returns:
        Panel de consultas (placeholder por ahora)
    """
    if not db_connection:
        from .menu_dashboard import _show_error
        return _show_error(parent, "No hay conexión a la base de datos")

    # TODO: Crear panel de consultas dedicado
    # Por ahora mostrar placeholder
    return _show_placeholder(
        parent,
        "Panel de Consultas",
        "Panel en desarrollo - Próximamente disponible"
    )


def _show_placeholder(parent, title, message):
    """Mostrar placeholder para paneles en desarrollo"""
    theme_manager = get_theme_manager()
    theme = theme_manager.get_current_theme()

    placeholder_frame = ctk.CTkFrame(parent, fg_color='transparent')

    title_label = ctk.CTkLabel(
        placeholder_frame,
        text=f'🚧 {title}',
        font=('Montserrat', 28, 'bold'),
        text_color=HUTCHISON_COLORS['aqua_green']
    )
    title_label.pack(expand=True, pady=(0, 10))

    message_label = ctk.CTkLabel(
        placeholder_frame,
        text=message,
        font=('Montserrat', 16),
        text_color=theme['text_secondary']
    )
    message_label.pack(expand=True)

    return placeholder_frame

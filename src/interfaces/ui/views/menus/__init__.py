"""
Módulos de menú - Organización modular de la interfaz
Cada menú en su propio archivo para mejor mantenibilidad
"""
from .menu_dashboard import show_dashboard_menu
from .menu_reportes import show_reportes_menu
from .menu_actualizar import show_actualizar_menu
from .menu_configuracion import show_configuracion_menu
from .menu_consultas import show_consultas_menu

__all__ = [
    'show_dashboard_menu',
    'show_reportes_menu',
    'show_actualizar_menu',
    'show_configuracion_menu',
    'show_consultas_menu'
]

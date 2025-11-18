"""
Gestor de Temas - Administra el cambio entre tema claro y oscuro
================================================================
"""
from smart_reports.config.themes import DARK_THEME, LIGHT_THEME, get_theme


class ThemeManager:
    """Singleton para gestionar el tema de la aplicación"""

    _instance = None
    _current_theme = 'dark'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa el gestor de temas"""
        if not hasattr(self, '_initialized'):
            self._current_theme = 'dark'
            self._callbacks = []
            self._initialized = True

    def get_current_theme(self):
        """Retorna el tema actual"""
        return get_theme(self._current_theme)

    def get_theme_mode(self):
        """Retorna el modo actual ('dark' o 'light')"""
        return self._current_theme

    def set_theme(self, mode):
        """
        Establece el tema de la aplicación

        Args:
            mode (str): 'dark' o 'light'
        """
        if mode in ['dark', 'light']:
            self._current_theme = mode
            self._notify_callbacks()
        else:
            raise ValueError(f"Tema inválido: {mode}. Use 'dark' o 'light'")

    def toggle_theme(self):
        """Alterna entre tema claro y oscuro"""
        new_theme = 'light' if self._current_theme == 'dark' else 'dark'
        self.set_theme(new_theme)
        return new_theme

    def register_callback(self, callback):
        """
        Registra una función callback que se ejecutará cuando cambie el tema

        Args:
            callback (callable): Función a ejecutar
        """
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def unregister_callback(self, callback):
        """
        Elimina un callback registrado

        Args:
            callback (callable): Función a eliminar
        """
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def _notify_callbacks(self):
        """Notifica a todos los callbacks registrados sobre el cambio de tema"""
        for callback in self._callbacks:
            try:
                callback(self._current_theme)
            except Exception as e:
                print(f"Error en callback de tema: {e}")

    def get_color(self, color_name):
        """
        Obtiene un color del tema actual

        Args:
            color_name (str): Nombre del color

        Returns:
            str: Código hexadecimal del color
        """
        theme = self.get_current_theme()
        return theme['colors'].get(color_name, '#000000')


# Singleton global
_theme_manager_instance = None


def get_theme_manager():
    """
    Obtiene la instancia única del gestor de temas

    Returns:
        ThemeManager: Instancia del gestor
    """
    global _theme_manager_instance
    if _theme_manager_instance is None:
        _theme_manager_instance = ThemeManager()
    return _theme_manager_instance

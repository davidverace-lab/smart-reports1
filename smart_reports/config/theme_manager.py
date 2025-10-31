"""
Gestor de Temas - Modo Claro/Oscuro
Smart Reports v2.0
"""
import json
import os
from typing import Dict, Callable
from smart_reports.config.settings import DARK_THEME, LIGHT_THEME


class ThemeManager:
    """Gestiona el tema de la aplicación (claro/oscuro)"""

    def __init__(self, config_path: str = None):
        """
        Inicializa el gestor de temas

        Args:
            config_path: Ruta al archivo de configuración JSON
        """
        if config_path is None:
            # Ubicar config.json en la carpeta raíz del proyecto
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            config_path = os.path.join(base_dir, 'config.json')

        self.config_path = config_path
        self.current_theme = 'dark'  # Tema por defecto
        self.theme_callbacks = []  # Callbacks para notificar cambios de tema

        # Cargar tema guardado
        self.load_theme_preference()

    def load_theme_preference(self) -> None:
        """Carga la preferencia de tema desde config.json"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_theme = config.get('theme', 'dark')
            else:
                # Crear archivo de configuración con valores por defecto
                self.save_theme_preference()
        except Exception as e:
            print(f"Error cargando preferencias de tema: {e}")
            self.current_theme = 'dark'

    def save_theme_preference(self) -> None:
        """Guarda la preferencia de tema en config.json"""
        try:
            # Cargar configuración existente o crear nueva
            config = {}
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

            # Actualizar tema
            config['theme'] = self.current_theme

            # Guardar
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando preferencias de tema: {e}")

    def get_current_theme(self) -> Dict[str, str]:
        """Retorna el diccionario de colores del tema actual"""
        return DARK_THEME if self.current_theme == 'dark' else LIGHT_THEME

    def is_dark_mode(self) -> bool:
        """Verifica si el modo oscuro está activo"""
        return self.current_theme == 'dark'

    def toggle_theme(self) -> None:
        """Cambia entre modo claro y oscuro"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.save_theme_preference()
        self._notify_theme_change()

    def set_theme(self, theme: str) -> None:
        """
        Establece el tema específico

        Args:
            theme: 'dark' o 'light'
        """
        if theme in ['dark', 'light']:
            self.current_theme = theme
            self.save_theme_preference()
            self._notify_theme_change()

    def register_callback(self, callback: Callable) -> None:
        """
        Registra un callback para ser notificado cuando cambie el tema

        Args:
            callback: Función a llamar cuando cambie el tema
        """
        if callback not in self.theme_callbacks:
            self.theme_callbacks.append(callback)

    def unregister_callback(self, callback: Callable) -> None:
        """
        Desregistra un callback

        Args:
            callback: Función a desregistrar
        """
        if callback in self.theme_callbacks:
            self.theme_callbacks.remove(callback)

    def _notify_theme_change(self) -> None:
        """Notifica a todos los callbacks registrados del cambio de tema"""
        theme_colors = self.get_current_theme()
        for callback in self.theme_callbacks:
            try:
                callback(theme_colors)
            except Exception as e:
                print(f"Error en callback de tema: {e}")

    def get_color(self, color_key: str) -> str:
        """
        Obtiene un color específico del tema actual

        Args:
            color_key: Clave del color (ej: 'background', 'surface', 'primary')

        Returns:
            Código hexadecimal del color
        """
        theme = self.get_current_theme()
        return theme.get(color_key, '#ffffff')


# Singleton global para el gestor de temas
_theme_manager_instance = None


def get_theme_manager() -> ThemeManager:
    """Obtiene la instancia singleton del ThemeManager"""
    global _theme_manager_instance
    if _theme_manager_instance is None:
        _theme_manager_instance = ThemeManager()
    return _theme_manager_instance

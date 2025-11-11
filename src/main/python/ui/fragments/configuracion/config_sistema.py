"""
Configuración - Ajustes del Sistema
Configuración general de la aplicación
"""
import customtkinter as ctk
from config.gestor_temas import get_theme_manager


class ConfigSistemaPanel(ctk.CTkFrame):
    """Panel de configuración del sistema"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.theme_manager = get_theme_manager()

        self._create_ui()

    def _create_ui(self):
        """Crear interfaz de configuración del sistema"""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = ctk.CTkLabel(
            self,
            text="⚙️ Configuración del Sistema",
            font=('Montserrat', 22, 'bold'),
            text_color=theme['text']
        )
        header.pack(pady=(10, 20), padx=20, anchor='w')

        # TODO: Agregar opciones de configuración
        # TODO: Agregar toggle de tema claro/oscuro
        # TODO: Agregar configuración de reportes

        placeholder = ctk.CTkLabel(
            self,
            text="Configuración del sistema\n(En desarrollo)",
            font=('Montserrat', 14),
            text_color=theme['text_secondary']
        )
        placeholder.pack(expand=True)

"""
Panel de Configuración - Versión Modular Simplificada
Agrupa configuración de sistema y usuarios
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.navigation.boton_pestana import CustomTabView
from config.gestor_temas import get_theme_manager

# Importar módulos de configuración
from .config_sistema import ConfigSistemaPanel
from .config_usuario import ConfigUsuariosPanel


class ConfiguracionPanel(ctk.CTkFrame):
    """Panel de configuración con tabs para sistema y usuarios"""

    def __init__(self, parent, db_connection=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.db_connection = db_connection
        self.theme_manager = get_theme_manager()

        # Header principal
        self._create_header()

        # Tabs de configuración
        self.tab_view = CustomTabView(self)
        self.tab_view.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Crear pestañas
        self.tab_sistema = self.tab_view.add("⚙️ Sistema", "⚙️")
        self.tab_usuarios = self.tab_view.add("👥 Usuarios", "👥")

        # Llenar pestañas
        self._create_config_panels()

    def _create_header(self):
        """Crear header del panel"""
        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent', height=80)
        header.pack(fill='x', padx=20, pady=(20, 15))
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="⚙️ Configuración del Sistema",
            font=('Montserrat', 24, 'bold'),
            text_color=theme['text']
        )
        title.pack(side='left', anchor='w')

    def _create_config_panels(self):
        """Crear paneles de configuración"""

        # Panel de configuración del sistema
        self.panel_sistema = ConfigSistemaPanel(self.tab_sistema)
        self.panel_sistema.pack(fill='both', expand=True)

        # Panel de gestión de usuarios
        self.panel_usuarios = ConfigUsuariosPanel(self.tab_usuarios, self.db_connection)
        self.panel_usuarios.pack(fill='both', expand=True)

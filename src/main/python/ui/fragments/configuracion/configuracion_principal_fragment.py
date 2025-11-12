"""
ConfiguracionPrincipalFragment - Fragment del menú principal de configuración
Separado según arquitectura Android Studio
"""
import customtkinter as ctk
from tkinter import messagebox
from src.main.res.config.gestor_temas import get_theme_manager
from src.main.python.ui.widgets.charts.tarjeta_configuracion import ConfigCard


class ConfiguracionPrincipalFragment(ctk.CTkFrame):
    """Fragment Principal de Configuración con Grid de Tarjetas 2x2"""

    def __init__(self, parent,
                 on_gestionar_empleados=None,
                 on_registro_soporte=None,
                 on_historial_reportes=None,
                 **kwargs):
        """
        Args:
            parent: Widget padre
            on_gestionar_empleados: Callback para navegar a gestión de empleados
            on_registro_soporte: Callback para navegar a registro de soporte
            on_historial_reportes: Callback para navegar a historial de reportes
        """
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.on_gestionar_empleados = on_gestionar_empleados
        self.on_registro_soporte = on_registro_soporte
        self.on_historial_reportes = on_historial_reportes
        self.theme_manager = get_theme_manager()

        # Crear interfaz
        self._create_interface()

        # Registrar callback para cambios de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    def _create_interface(self):
        """Crear interfaz completa del fragment"""
        theme = self.theme_manager.get_current_theme()

        # Frame principal con scroll
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header con título
        self._create_header(scroll_frame, theme)

        # Grid de tarjetas 2x2
        self._create_cards_grid(scroll_frame, theme)

    def _create_header(self, parent, theme):
        """Crear header con título"""
        header = ctk.CTkFrame(parent, fg_color='transparent', height=80)
        header.pack(fill='x', pady=(20, 30))
        header.pack_propagate(False)

        # Color del título: blanco en modo oscuro, azul marino en modo claro
        is_dark = self.theme_manager.is_dark_mode()
        title_color = '#FFFFFF' if is_dark else '#002E6D'

        title = ctk.CTkLabel(
            header,
            text='Configuración',
            font=('Montserrat', 36, 'bold'),
            text_color=title_color
        )
        title.pack(side='left', padx=20, pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text='Gestiona las opciones del sistema',
            font=('Montserrat', 14),
            text_color=theme['text_secondary']
        )
        subtitle.pack(side='left', padx=(20, 0), pady=20)

    def _create_cards_grid(self, parent, theme):
        """Crear grid 2x2 de tarjetas de configuración"""
        # Contenedor principal con grid 2x2
        grid_container = ctk.CTkFrame(parent, fg_color='transparent')
        grid_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Configurar grid
        grid_container.grid_columnconfigure((0, 1), weight=1)
        grid_container.grid_rowconfigure((0, 1), weight=1)

        # Card 1: Gestionar Empleados
        card1 = ConfigCard(
            grid_container,
            icon='👥',
            title='Gestionar Empleados',
            description='Agregar, editar o consultar empleados del sistema',
            button_text='Gestionar',
            command=self.on_gestionar_empleados if self.on_gestionar_empleados else None
        )
        card1.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')

        # Card 2: Registro de Soporte
        card2 = ConfigCard(
            grid_container,
            icon='📝',
            title='Registro de Soporte',
            description='Registrar soporte brindado a usuarios por correo electrónico',
            button_text='Registrar',
            command=self.on_registro_soporte if self.on_registro_soporte else None
        )
        card2.grid(row=0, column=1, padx=15, pady=15, sticky='nsew')

        # Card 3: Historial de Reportes
        card3 = ConfigCard(
            grid_container,
            icon='📋',
            title='Historial de Reportes',
            description='Ver y descargar reportes PDF generados anteriormente',
            button_text='Ver Historial',
            command=self.on_historial_reportes if self.on_historial_reportes else None
        )
        card3.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')

        # Card 4: Acerca de
        card4 = ConfigCard(
            grid_container,
            icon='ℹ️',
            title='Acerca de',
            description='Información de la versión y del desarrollador',
            button_text='Ver Info',
            command=self._show_about
        )
        card4.grid(row=1, column=1, padx=15, pady=15, sticky='nsew')

    # ==================== LÓGICA DE NEGOCIO ====================

    def _show_about(self):
        """Mostrar información sobre la aplicación"""
        messagebox.showinfo(
            "Acerca de",
            "SMART REPORTS V2.0\n\n"
            "SISTEMA DE GESTIÓN DE CAPACITACIONES\n"
            "INSTITUTO HUTCHISON PORTS\n\n"
            "Desarrollado por: David Vera\n"
            "© 2025 - TODOS LOS DERECHOS RESERVADOS"
        )

    # ==================== UTILIDADES ====================

    def _on_theme_changed(self, theme_colors):
        """Callback para cambios de tema"""
        pass

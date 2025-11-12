"""
Panel de Configuración - Coordinador de Fragments
Modularizado según arquitectura Android Studio
"""
import customtkinter as ctk
from src.main.res.config.gestor_temas import get_theme_manager
from src.main.python.ui.fragments.configuracion.configuracion_principal_fragment import ConfiguracionPrincipalFragment
from src.main.python.ui.fragments.configuracion.gestion_usuarios_fragment import GestionUsuariosFragment
from src.main.python.ui.fragments.configuracion.soporte_tickets_fragment import SoporteTicketsFragment
from src.main.python.ui.fragments.configuracion.historial_reportes_fragment import HistorialReportesFragment
from src.main.python.ui.fragments.configuracion.panel_importacion_datos import PanelImportacionDatos


class ConfiguracionPanel(ctk.CTkFrame):
    """
    Panel de Configuración - Coordinador de Fragments

    Gestiona la navegación entre diferentes fragments de configuración:
    - ConfiguracionPrincipalFragment: Menú principal con tarjetas
    - GestionUsuariosFragment: CRUD de usuarios
    - SoporteTicketsFragment: Registro de soporte
    - HistorialReportesFragment: Historial de reportes
    """

    def __init__(self, parent, db_connection=None, **kwargs):
        """
        Args:
            parent: Widget padre
            db_connection: Conexión a la base de datos (opcional)
        """
        # Obtener tema actual
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        # Configurar fondo explícitamente
        super().__init__(parent, fg_color=theme['background'], **kwargs)

        self.db = db_connection
        self.cursor = db_connection.cursor() if db_connection else None

        # Fragments (lazy loading)
        self.main_fragment = None
        self.users_fragment = None
        self.tickets_fragment = None
        self.history_fragment = None
        self.import_fragment = None

        # Mostrar fragment principal al inicio
        self.show_main_config_frame()

        # Registrar callback para cambios de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    # ==================== NAVEGACIÓN ENTRE FRAGMENTS ====================

    def show_main_config_frame(self):
        """Mostrar fragment principal (menú con tarjetas)"""
        # Ocultar todos los fragments
        self._hide_all_fragments()

        # Crear o mostrar fragment principal
        if not self.main_fragment:
            self.main_fragment = ConfiguracionPrincipalFragment(
                self,
                on_gestionar_empleados=self.show_user_manager_frame,
                on_registro_soporte=self.show_support_ticket_frame,
                on_historial_reportes=self.show_report_history_frame,
                on_importacion_datos=self.show_import_data_frame
            )

        self.main_fragment.pack(fill='both', expand=True)

    def show_user_manager_frame(self):
        """Mostrar fragment de gestión de usuarios"""
        # Ocultar todos los fragments
        self._hide_all_fragments()

        # Crear o mostrar fragment de usuarios
        if not self.users_fragment:
            self.users_fragment = GestionUsuariosFragment(
                self,
                db_connection=self.db,
                on_back=self.show_main_config_frame
            )

        self.users_fragment.pack(fill='both', expand=True)

        # Cargar todos los usuarios al entrar
        if hasattr(self.users_fragment, '_load_all_users'):
            self.users_fragment._load_all_users()

    def show_support_ticket_frame(self):
        """Mostrar fragment de registro de soporte"""
        # Ocultar todos los fragments
        self._hide_all_fragments()

        # Crear o mostrar fragment de tickets
        if not self.tickets_fragment:
            self.tickets_fragment = SoporteTicketsFragment(
                self,
                db_connection=self.db,
                on_back=self.show_main_config_frame
            )

        self.tickets_fragment.pack(fill='both', expand=True)

    def show_report_history_frame(self):
        """Mostrar fragment de historial de reportes"""
        # Ocultar todos los fragments
        self._hide_all_fragments()

        # Crear o mostrar fragment de historial
        if not self.history_fragment:
            self.history_fragment = HistorialReportesFragment(
                self,
                db_connection=self.db,
                on_back=self.show_main_config_frame
            )

        self.history_fragment.pack(fill='both', expand=True)

    def show_import_data_frame(self):
        """Mostrar fragment de importación de datos"""
        # Ocultar todos los fragments
        self._hide_all_fragments()

        # Crear o mostrar fragment de importación
        if not self.import_fragment:
            # PanelImportacionDatos ya tiene botón de volver integrado
            # Lo envolvemos en un wrapper para agregar botón de volver consistente
            wrapper = ctk.CTkFrame(self, fg_color='transparent')

            # Botón volver
            theme = self.theme_manager.get_current_theme()
            back_btn = ctk.CTkButton(
                wrapper,
                text="← Volver",
                command=self.show_main_config_frame,
                fg_color=theme['surface'],
                hover_color=theme['hover'],
                text_color=theme['text'],
                font=('Segoe UI', 13, 'bold'),
                height=40,
                width=120
            )
            back_btn.pack(anchor='nw', padx=20, pady=10)

            # Panel de importación
            import_panel = PanelImportacionDatos(wrapper, db_connection=self.db)
            import_panel.pack(fill='both', expand=True)

            self.import_fragment = wrapper

        self.import_fragment.pack(fill='both', expand=True)

    def _hide_all_fragments(self):
        """Ocultar todos los fragments"""
        if self.main_fragment:
            self.main_fragment.pack_forget()
        if self.users_fragment:
            self.users_fragment.pack_forget()
        if self.tickets_fragment:
            self.tickets_fragment.pack_forget()
        if self.history_fragment:
            self.history_fragment.pack_forget()
        if self.import_fragment:
            self.import_fragment.pack_forget()

    # ==================== CALLBACKS ====================

    def _on_theme_changed(self, theme_colors):
        """Callback para cambios de tema"""
        # Actualizar fondo del panel
        self.configure(fg_color=theme_colors['background'])

        # Los fragments individuales manejan sus propios cambios de tema
        # mediante sus propios callbacks registrados

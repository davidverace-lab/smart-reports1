"""
VentanaPrincipalView - SOLO INTERFAZ VISUAL (UI)
Patrón Android Studio: Esta clase es como el XML (solo vista)
La lógica está en los Controllers (como Java en Android)

ARQUITECTURA LIMPIA:
- View (este archivo): Solo widgets y layout
- Controllers: Toda la lógica de negocio
"""
import customtkinter as ctk
from tkinter import messagebox

# Android Studio structure imports
from src.main.res.config.themes import APP_CONFIG, HUTCHISON_COLORS
from src.main.res.config.gestor_temas import get_theme_manager
from src.main.python.data.repositories.persistence.mysql.connection import DatabaseConnection

# Controllers (LÓGICA separada - ViewModels en Android)
from src.main.python.viewmodels.database_query_controller import DatabaseQueryController
from src.main.python.viewmodels.file_import_controller import FileImportController
from src.main.python.viewmodels.reports_controller import ReportsController
from src.main.python.viewmodels.navigation_controller import NavigationController

# Components (UI - Widgets/Custom Views en Android)
from src.main.python.ui.widgets.navigation.barra_lateral import ModernSidebar
from src.main.python.ui.widgets.navigation.barra_superior import TopBar

# Menus (UI modular - Fragments en Android)
from src.main.python.ui.fragments import (
    show_dashboard_menu,
    show_reportes_menu,
    show_actualizar_menu,
    show_configuracion_menu,
    show_consultas_menu
)


class VentanaPrincipalView:
    """
    Vista principal - SOLO INTERFAZ (patrón Android)

    Esta clase SOLO maneja:
    - Creación de widgets
    - Layout y posicionamiento
    - Navegación entre paneles

    La LÓGICA está en los Controllers
    """

    def __init__(self, root, username="Admin", user_role="Administrador"):
        """
        Inicializar vista principal

        Args:
            root: Ventana raíz de Tkinter
            username: Nombre del usuario
            user_role: Rol del usuario
        """
        self.root = root
        self.root.title("SMART REPORTS - INSTITUTO HUTCHISON PORTS")
        self.root.geometry("1400x900")

        # Información del usuario
        self.username = username
        self.user_role = user_role

        # Theme Manager
        self.theme_manager = get_theme_manager()

        # Track current view for theme refresh
        self.current_view = None

        # Configurar appearance de customtkinter
        appearance = "dark" if self.theme_manager.is_dark_mode() else "light"
        ctk.set_appearance_mode(appearance)
        ctk.set_default_color_theme("dark-blue")

        # === CONTROLLERS (LÓGICA SEPARADA) ===
        self._initialize_controllers()

        # === UI COMPONENTS ===
        self._create_interface()

        # Registrar callback para cambios de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    def _initialize_controllers(self):
        """Inicializar todos los controllers (lógica separada)"""

        # Base de datos
        self.db = DatabaseConnection()
        self.conn = None
        self.cursor = None

        try:
            self.conn = self.db.connect()
            self.cursor = self.db.get_cursor()
        except Exception as e:
            messagebox.showerror(
                "Error de Conexión",
                f"No se pudo conectar a la base de datos:\n{str(e)}\n\n"
                "La aplicación continuará pero algunas funciones no estarán disponibles."
            )

        # Controllers (lógica separada de la UI)
        self.db_controller = DatabaseQueryController(self.conn, self.cursor) if self.conn else None
        self.file_controller = FileImportController(self.db)
        self.reports_controller = ReportsController(self.conn, self.cursor) if self.conn else None
        self.nav_controller = NavigationController()

        # Verificar base de datos
        if self.db_controller:
            success, message = self.db_controller.verify_database_tables()
            if not success:
                messagebox.showwarning("Advertencia de BD", message)

    def _create_interface(self):
        """Crear interfaz de usuario (SOLO UI)"""
        theme = self.theme_manager.get_current_theme()

        # Container principal
        self.main_container = ctk.CTkFrame(
            self.root,
            fg_color=theme['background'],
            corner_radius=0
        )
        self.main_container.pack(fill='both', expand=True)

        # === SIDEBAR (Navegación lateral) ===
        navigation_callbacks = {
            'dashboard': self.show_dashboard,
            'consultas': self.show_consultas,
            'actualizar': self.show_actualizar,
            'importacion': self.show_importacion,
            'reportes': self.show_reportes,
            'configuracion': self.show_configuracion,
        }

        self.sidebar = ModernSidebar(
            self.main_container,
            navigation_callbacks,
            theme_change_callback=self._handle_theme_change
        )
        self.sidebar.pack(side='left', fill='y')

        # === RIGHT FRAME (TopBar + Content) ===
        right_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=theme['background'],
            corner_radius=0
        )
        right_frame.pack(side='left', fill='both', expand=True)

        # TopBar (Barra superior)
        self.top_bar = TopBar(
            right_frame,
            username=self.username,
            user_role=self.user_role
        )
        self.top_bar.pack(side='top', fill='x')

        # Content Area (Área de contenido principal)
        self.content_area = ctk.CTkFrame(
            right_frame,
            fg_color=theme['background'],
            corner_radius=0
        )
        self.content_area.pack(side='top', fill='both', expand=True)

        # Mostrar dashboard por defecto
        self.show_dashboard()
        self.sidebar.set_active('dashboard')

    # ==================== NAVEGACIÓN ENTRE PANELES ====================

    def _clear_content(self):
        """Limpiar área de contenido"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        """Mostrar panel de Dashboards Gerenciales"""
        self._clear_content()
        self.current_view = 'dashboard'
        self.nav_controller.navigate_to('dashboard', None)

        # Usar módulo de menú (lógica separada)
        panel = show_dashboard_menu(
            self.content_area,
            self.conn,
            self.username,
            self.user_role
        )
        panel.pack(fill='both', expand=True)

    def show_actualizar(self):
        """Mostrar panel de Actualización/Cruce de Datos"""
        self._clear_content()
        self.current_view = 'actualizar'
        self.nav_controller.navigate_to('actualizar', None)

        # Usar módulo de menú (lógica separada)
        panel = show_actualizar_menu(
            self.content_area,
            self.conn,
            self.file_controller
        )
        panel.pack(fill='both', expand=True, padx=20, pady=20)

    def show_importacion(self):
        """Mostrar panel de Importación de Datos"""
        self._clear_content()
        self.current_view = 'importacion'
        self.nav_controller.navigate_to('importacion', None)

        # Importar PanelImportacionDatos
        from src.main.python.ui.fragments.configuracion.panel_importacion_datos import PanelImportacionDatos

        # Crear panel de importación
        panel = PanelImportacionDatos(
            self.content_area,
            db_connection=self.conn
        )
        panel.pack(fill='both', expand=True)

    def show_consultas(self):
        """Mostrar panel de Consultas"""
        self._clear_content()
        self.current_view = 'consultas'
        self.nav_controller.navigate_to('consultas', None)

        # Usar módulo de menú (lógica separada)
        panel = show_consultas_menu(
            self.content_area,
            self.conn
        )
        panel.pack(fill='both', expand=True)

    def show_reportes(self):
        """Mostrar panel de Reportes"""
        self._clear_content()
        self.current_view = 'reportes'
        self.nav_controller.navigate_to('reportes', None)

        # Usar módulo de menú (lógica separada)
        show_reportes_menu(
            self.content_area,
            self.conn,
            self.cursor
        )

    def show_configuracion(self):
        """Mostrar panel de Configuración"""
        self._clear_content()
        self.current_view = 'configuracion'
        self.nav_controller.navigate_to('configuracion', None)

        # Usar módulo de menú (lógica separada)
        panel = show_configuracion_menu(
            self.content_area,
            self.conn,
            self.cursor,
            self.db
        )
        panel.pack(fill='both', expand=True)

    # ==================== HELPERS ====================
    # (Código de reportes movido a src/interfaces/ui/views/menus/menu_reportes.py)


    # ==================== HELPERS ====================

    def _show_error_message(self, message):
        """Mostrar mensaje de error en el content area"""
        theme = self.theme_manager.get_current_theme()

        error_frame = ctk.CTkFrame(self.content_area, fg_color='transparent')
        error_frame.pack(fill='both', expand=True)

        error_label = ctk.CTkLabel(
            error_frame,
            text=f'⚠️ {message}\n\nPor favor verifica la configuración.',
            font=('Montserrat', 18),
            text_color='#ff6b6b'
        )
        error_label.pack(expand=True)

    def _show_placeholder(self, title, message):
        """Mostrar placeholder para paneles en desarrollo"""
        theme = self.theme_manager.get_current_theme()

        placeholder_frame = ctk.CTkFrame(self.content_area, fg_color='transparent')
        placeholder_frame.pack(fill='both', expand=True)

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

    def _handle_theme_change(self):
        """Manejar cambio de tema"""
        # El theme manager ya maneja la propagación
        # Solo necesitamos refrescar la interfaz
        pass

    def _on_theme_changed(self, theme_colors):
        """Callback cuando cambia el tema"""
        # Actualizar appearance mode de customtkinter
        appearance = "dark" if self.theme_manager.is_dark_mode() else "light"
        ctk.set_appearance_mode(appearance)

        # Refrescar colores del main container
        self.main_container.configure(fg_color=theme_colors['background'])
        self.content_area.configure(fg_color=theme_colors['background'])

        # Refrescar el panel actual para aplicar cambios de tema inmediatamente
        if self.current_view == 'dashboard':
            self.show_dashboard()
        elif self.current_view == 'consultas':
            self.show_consultas()
        elif self.current_view == 'actualizar':
            self.show_actualizar()
        elif self.current_view == 'importacion':
            self.show_importacion()
        elif self.current_view == 'reportes':
            self.show_reportes()
        elif self.current_view == 'configuracion':
            self.show_configuracion()


# Alias para mantener compatibilidad con código existente
MainWindow = VentanaPrincipalView

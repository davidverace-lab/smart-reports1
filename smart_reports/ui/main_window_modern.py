"""
Ventana principal de Smart Reports - VERSIÓN MODERNA con CustomTkinter
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from datetime import datetime
import os

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DRAG_DROP_AVAILABLE = True
except ImportError:
    DRAG_DROP_AVAILABLE = False
    print("Warning: tkinterdnd2 no disponible. Drag & drop deshabilitado.")

from smart_reports.config.settings import APP_CONFIG, HUTCHISON_COLORS
from smart_reports.config.theme_manager import get_theme_manager
from smart_reports.database.connection import DatabaseConnection
from smart_reports.services.data_processor import TranscriptProcessor
from smart_reports.ui.components.modern_sidebar import ModernSidebar
from smart_reports.ui.components.top_bar import TopBar
from smart_reports.ui.components.config_card import ConfigCard
from smart_reports.ui.panels.modern_dashboard import ModernDashboard
from smart_reports.ui.dialogs.user_management_dialog import UserManagementDialog


class MainWindow:
    """Ventana principal moderna de la aplicación"""

    def __init__(self, root, username="Admin", user_role="Administrador"):
        self.root = root
        self.root.title("SMART REPORTS - INSTITUTO HUTCHISON PORTS")
        self.root.geometry("1400x900")

        # Información del usuario
        self.username = username
        self.user_role = user_role

        # Gestor de temas
        self.theme_manager = get_theme_manager()

        # Configurar appearance de customtkinter según tema guardado
        appearance = "dark" if self.theme_manager.is_dark_mode() else "light"
        ctk.set_appearance_mode(appearance)
        ctk.set_default_color_theme("dark-blue")

        # Base de datos
        self.db = DatabaseConnection()
        self.conn = None
        self.cursor = None

        try:
            self.conn = self.db.connect()
            self.cursor = self.db.get_cursor()
            self.verify_database_tables()
        except Exception as e:
            messagebox.showerror("Error de Conexión",
                f"No se pudo conectar a la base de datos:\n{str(e)}\n\n"
                "La aplicación continuará pero algunas funciones no estarán disponibles.")

        # Variables de tracking
        self.current_file = None
        self.changes_log = []
        self.current_panel = None  # Guardar referencia al panel actual

        # Crear interfaz moderna
        self.create_modern_interface()

        # Registrar callback para cambios de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    def verify_database_tables(self):
        """Verificar que las tablas necesarias existan"""
        tables_needed = ['Instituto_UnidadDeNegocio', 'Instituto_Usuario',
                        'Instituto_Modulo', 'Instituto_ProgresoModulo']
        placeholders = ','.join(['?' for _ in tables_needed])

        try:
            self.cursor.execute(f"""
                SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
                AND TABLE_NAME IN ({placeholders})
            """, tables_needed)

            existing_tables = [t[0] for t in self.cursor.fetchall()]

            if len(existing_tables) < len(tables_needed):
                missing = set(tables_needed) - set(existing_tables)
                messagebox.showwarning("Advertencia",
                    f"Faltan tablas en la BD: {', '.join(missing)}\n" +
                    "Verifique que las tablas existan en la base de datos.")
        except Exception as e:
            print(f"Error verificando tablas: {e}")

    def create_modern_interface(self):
        """Crear interfaz moderna con customtkinter"""
        theme = self.theme_manager.get_current_theme()

        # Container principal
        self.main_container = ctk.CTkFrame(self.root, fg_color=theme['background'], corner_radius=0)
        self.main_container.pack(fill='both', expand=True)

        # Sidebar moderna
        navigation_callbacks = {
            'dashboard': self.show_dashboard_panel,
            'consultas': self.show_consultas_panel,
            'actualizar': self.show_actualizar_panel,
            'configuracion': self.show_configuracion_panel,
        }

        self.sidebar = ModernSidebar(
            self.main_container,
            navigation_callbacks,
            theme_change_callback=self._handle_theme_change
        )
        self.sidebar.pack(side='left', fill='y')

        # Frame derecho (top bar + contenido)
        right_frame = ctk.CTkFrame(self.main_container, fg_color=theme['background'], corner_radius=0)
        right_frame.pack(side='left', fill='both', expand=True)

        # Top Bar (barra superior)
        self.top_bar = TopBar(
            right_frame,
            username=self.username,
            user_role=self.user_role
        )
        self.top_bar.pack(side='top', fill='x')

        # Área de contenido principal
        self.content_area = ctk.CTkFrame(right_frame, fg_color=theme['background'], corner_radius=0)
        self.content_area.pack(side='top', fill='both', expand=True)

        # Mostrar dashboard por defecto
        self.show_dashboard_panel()
        self.sidebar.set_active('dashboard')

    def clear_content_area(self):
        """Limpiar área de contenido"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # ==================== SECCIONES PRINCIPALES ====================

    def show_dashboard_panel(self):
        """Mostrar panel de dashboard moderno"""
        self.clear_content_area()
        self.current_panel = 'dashboard'

        if self.conn is None:
            # Mostrar mensaje de error si no hay conexión
            error_frame = ctk.CTkFrame(self.content_area, fg_color='transparent')
            error_frame.pack(fill='both', expand=True)

            error_label = ctk.CTkLabel(
                error_frame,
                text='⚠️ No hay conexión a la base de datos\n\nPor favor verifica la configuración de conexión.',
                font=('Segoe UI', 18),
                text_color='#ff6b6b'
            )
            error_label.pack(expand=True)
            return

        # Crear Modern Dashboard
        dashboard = ModernDashboard(self.content_area, self.conn)
        dashboard.pack(fill='both', expand=True)

    def show_actualizar_panel(self):
        """Panel de actualización de datos - MODERNIZADO"""
        self.clear_content_area()
        self.current_panel = 'actualizar'

        # Scroll frame para contenido
        scroll_frame = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color='transparent',
            scrollbar_button_color='#3a3d5c'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header
        header = ctk.CTkFrame(scroll_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 30))

        theme = self.theme_manager.get_current_theme()

        title = ctk.CTkLabel(
            header,
            text='Actualizar Datos',
            font=('Montserrat', 32, 'bold'),
            text_color=theme['text']
        )
        title.pack(side='left')

        # Card 1: Seleccionar archivo
        card1 = ctk.CTkFrame(scroll_frame, fg_color=theme['surface'], corner_radius=20, border_width=1, border_color=theme['border'])
        card1.pack(fill='x', pady=10)

        # Card header
        card1_header = ctk.CTkLabel(
            card1,
            text='1. Seleccionar Archivo',
            font=('Montserrat', 20, 'bold'),
            text_color=theme['text']
        )
        card1_header.pack(padx=30, pady=(20, 10), anchor='w')

        # Drop Zone
        drop_zone_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f0f2f5'
        drop_zone = ctk.CTkFrame(
            card1,
            fg_color=drop_zone_bg,
            corner_radius=15,
            border_width=2,
            border_color='#6c63ff',
            height=150
        )
        drop_zone.pack(fill='x', padx=30, pady=10)
        drop_zone.pack_propagate(False)

        # Icono y texto de drop zone
        drop_icon = ctk.CTkLabel(
            drop_zone,
            text='📁',
            font=('Segoe UI', 48)
        )
        drop_icon.pack(pady=(20, 5))

        drop_text1 = ctk.CTkLabel(
            drop_zone,
            text='Arrastra archivo Excel aquí',
            font=('Segoe UI', 16, 'bold'),
            text_color='#6c63ff'
        )
        drop_text1.pack()

        drop_text2 = ctk.CTkLabel(
            drop_zone,
            text='o haz clic en el botón de abajo',
            font=('Segoe UI', 12),
            text_color='#a0a0b0'
        )
        drop_text2.pack(pady=(5, 10))

        # Configurar drag & drop si está disponible
        if DRAG_DROP_AVAILABLE:
            try:
                # Intentar configurar drop en el frame
                # Esto puede fallar si el root no es TkinterDnD.Tk
                drop_zone.drop_target_register(DND_FILES)
                drop_zone.dnd_bind('<<Drop>>', self._on_file_drop)
                drop_zone.dnd_bind('<<DragEnter>>', lambda e: drop_zone.configure(border_color='#51cf66'))
                drop_zone.dnd_bind('<<DragLeave>>', lambda e: drop_zone.configure(border_color='#6c63ff'))
            except (AttributeError, Exception) as e:
                # Silenciar el error y deshabilitar drag & drop
                # Esto ocurre cuando CTk no tiene soporte para TkinterDnD
                # Actualizar texto de drop zone
                drop_text1.configure(text='Usa el botón de abajo para seleccionar archivo')
                drop_text2.configure(text='(Drag & drop no disponible con CustomTkinter)')

        # File info frame
        file_frame_bg = theme['surface_light'] if self.theme_manager.is_dark_mode() else '#e8e8e8'
        file_frame = ctk.CTkFrame(card1, fg_color=file_frame_bg, corner_radius=10)
        file_frame.pack(fill='x', padx=30, pady=10)

        file_label_title = ctk.CTkLabel(
            file_frame,
            text='Archivo:',
            font=('Segoe UI', 14),
            text_color=theme['text_secondary']
        )
        file_label_title.pack(side='left', padx=15, pady=15)

        self.file_label = ctk.CTkLabel(
            file_frame,
            text='Ningún archivo seleccionado',
            font=('Segoe UI', 14),
            text_color=theme['text_light']
        )
        self.file_label.pack(side='left', padx=5, pady=15)

        # Botón seleccionar
        select_btn = ctk.CTkButton(
            card1,
            text='📁  Seleccionar Archivo Transcript Status',
            font=('Arial', 16, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            corner_radius=10,
            height=50,
            command=self.select_transcript_file
        )
        select_btn.pack(padx=30, pady=(10, 20))

        # Card 2: Actualizar base de datos
        card2 = ctk.CTkFrame(scroll_frame, fg_color=theme['surface'], corner_radius=20, border_width=1, border_color=theme['border'])
        card2.pack(fill='x', pady=10)

        card2_header = ctk.CTkLabel(
            card2,
            text='2. Actualizar Base de Datos',
            font=('Montserrat', 20, 'bold'),
            text_color=theme['text']
        )
        card2_header.pack(padx=30, pady=(20, 10), anchor='w')

        card2_desc = ctk.CTkLabel(
            card2,
            text='Este proceso actualizará usuarios, módulos y progreso en la BD',
            font=('Arial', 12),
            text_color=theme['text_secondary']
        )
        card2_desc.pack(padx=30, pady=(0, 15), anchor='w')

        update_btn = ctk.CTkButton(
            card2,
            text='🔄  Actualizar Base de Datos (Cruce de Datos)',
            font=('Arial', 16, 'bold'),
            fg_color=HUTCHISON_COLORS['success'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            corner_radius=10,
            height=50,
            command=self.update_database_from_file
        )
        update_btn.pack(padx=30, pady=(0, 20))

        # Card 3: Panel de movimientos
        card3 = ctk.CTkFrame(scroll_frame, fg_color=theme['surface'], corner_radius=20, border_width=1, border_color=theme['border'])
        card3.pack(fill='both', expand=True, pady=10)

        card3_header = ctk.CTkLabel(
            card3,
            text='📋  Panel de Movimientos',
            font=('Montserrat', 20, 'bold'),
            text_color=theme['text']
        )
        card3_header.pack(padx=30, pady=(20, 10), anchor='w')

        # Text area para movimientos
        textbox_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        self.movements_text = ctk.CTkTextbox(
            card3,
            fg_color=textbox_bg,
            border_color=theme['border'],
            border_width=1,
            corner_radius=10,
            font=('Consolas', 11),
            text_color=theme['text'],
            height=300
        )
        self.movements_text.pack(fill='both', expand=True, padx=30, pady=(10, 20))

        # Botón de estadísticas
        stats_btn = ctk.CTkButton(
            card3,
            text='📊  Ver Estadísticas Actuales',
            font=('Arial', 14),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            corner_radius=10,
            height=40,
            command=self.show_progress_stats
        )
        stats_btn.pack(padx=30, pady=(0, 20))

    def show_consultas_panel(self):
        """Panel de consultas - MODERNIZADO"""
        self.clear_content_area()
        self.current_panel = 'consultas'

        if self.conn is None:
            # Mostrar mensaje de error si no hay conexión
            error_frame = ctk.CTkFrame(self.content_area, fg_color='transparent')
            error_frame.pack(fill='both', expand=True)

            error_label = ctk.CTkLabel(
                error_frame,
                text='⚠️ No hay conexión a la base de datos\n\nPor favor verifica la configuración de conexión.',
                font=('Segoe UI', 18),
                text_color='#ff6b6b'
            )
            error_label.pack(expand=True)
            return

        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color='transparent',
            scrollbar_button_color='#3a3d5c'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header
        header = ctk.CTkFrame(scroll_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 30))

        theme = self.theme_manager.get_current_theme()

        title = ctk.CTkLabel(
            header,
            text='Consultas de Usuarios',
            font=('Montserrat', 32, 'bold'),
            text_color=theme['text']
        )
        title.pack(side='left')

        # Card: Búsquedas
        search_card = ctk.CTkFrame(scroll_frame, fg_color=theme['surface'], corner_radius=20, border_width=1, border_color=theme['border'])
        search_card.pack(fill='x', pady=10)

        # Búsqueda por ID
        search_id_frame = ctk.CTkFrame(search_card, fg_color='transparent')
        search_id_frame.pack(fill='x', padx=30, pady=20)

        ctk.CTkLabel(
            search_id_frame,
            text='🔍  Buscar Usuario por ID:',
            font=('Arial', 16),
            text_color=theme['text']
        ).pack(side='left', padx=(0, 15))

        self.search_entry = ctk.CTkEntry(
            search_id_frame,
            placeholder_text='Ingrese ID de usuario...',
            font=('Arial', 14),
            width=300,
            height=40,
            corner_radius=10
        )
        self.search_entry.pack(side='left', padx=5)

        search_btn = ctk.CTkButton(
            search_id_frame,
            text='Buscar',
            font=('Arial', 14),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            corner_radius=10,
            height=40,
            width=120,
            command=self.search_user_by_id
        )
        search_btn.pack(side='left', padx=10)

        # Separador
        sep = ctk.CTkFrame(search_card, height=1, fg_color=theme['border'])
        sep.pack(fill='x', padx=30, pady=10)

        # Búsqueda por Unidad de Negocio
        search_unit_frame = ctk.CTkFrame(search_card, fg_color='transparent')
        search_unit_frame.pack(fill='x', padx=30, pady=20)

        ctk.CTkLabel(
            search_unit_frame,
            text='🏢  Consultar por Unidad de Negocio:',
            font=('Arial', 16),
            text_color=theme['text']
        ).pack(side='left', padx=(0, 15))

        self.business_unit_var = tk.StringVar()
        self.business_unit_combo = ctk.CTkComboBox(
            search_unit_frame,
            variable=self.business_unit_var,
            font=('Arial', 14),
            width=350,
            height=40,
            corner_radius=10,
            values=['Cargando...']
        )
        self.business_unit_combo.pack(side='left', padx=5)

        # Cargar unidades
        self.load_business_units()

        search_unit_btn = ctk.CTkButton(
            search_unit_frame,
            text='Consultar',
            font=('Arial', 14),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            corner_radius=10,
            height=40,
            width=120,
            command=self.query_business_unit_from_combo
        )
        search_unit_btn.pack(side='left', padx=10)

        # Separador
        sep2 = ctk.CTkFrame(search_card, height=1, fg_color=theme['border'])
        sep2.pack(fill='x', padx=30, pady=10)

        # PANEL DE FILTROS AVANZADOS (Colapsable)
        filters_header_frame = ctk.CTkFrame(search_card, fg_color='transparent')
        filters_header_frame.pack(fill='x', padx=30, pady=(20, 10))

        self.filters_expanded = tk.BooleanVar(value=False)

        filters_btn_bg = theme['surface_light'] if self.theme_manager.is_dark_mode() else '#e8e8e8'
        self.toggle_filters_btn = ctk.CTkButton(
            filters_header_frame,
            text='🔽  Mostrar Filtros Avanzados',
            font=('Arial', 14, 'bold'),
            fg_color=filters_btn_bg,
            text_color=theme['text'],
            hover_color=HUTCHISON_COLORS['ports_sky_blue'],
            corner_radius=10,
            height=40,
            anchor='w',
            command=self.toggle_advanced_filters
        )
        self.toggle_filters_btn.pack(fill='x')

        # Frame para filtros (inicialmente oculto)
        filters_frame_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        self.advanced_filters_frame = ctk.CTkFrame(search_card, fg_color=filters_frame_bg, corner_radius=10)

        # Fila 1: Estado y Módulo
        filters_row1 = ctk.CTkFrame(self.advanced_filters_frame, fg_color='transparent')
        filters_row1.pack(fill='x', padx=20, pady=(20, 10))

        # Filtro por Estado
        ctk.CTkLabel(
            filters_row1,
            text='📊 Estado:',
            font=('Segoe UI', 13),
            text_color=theme['text']
        ).pack(side='left', padx=(0, 10))

        self.filter_estado_var = tk.StringVar(value='Todos')
        self.filter_estado_menu = ctk.CTkOptionMenu(
            filters_row1,
            variable=self.filter_estado_var,
            values=['Todos', 'Completado', 'En Proceso', 'Sin Iniciar'],
            font=('Arial', 12),
            width=180,
            height=35,
            corner_radius=8,
            fg_color='#2b2d42',
            button_color=HUTCHISON_COLORS['ports_sky_blue'],
            button_hover_color=HUTCHISON_COLORS['ports_sea_blue']
        )
        self.filter_estado_menu.pack(side='left', padx=5)

        # Spacer
        ctk.CTkFrame(filters_row1, fg_color='transparent', width=30).pack(side='left')

        # Filtro por Módulo
        ctk.CTkLabel(
            filters_row1,
            text='📚 Módulo:',
            font=('Segoe UI', 13),
            text_color=theme['text']
        ).pack(side='left', padx=(0, 10))

        self.filter_modulo_var = tk.StringVar(value='Todos')
        self.filter_modulo_menu = ctk.CTkOptionMenu(
            filters_row1,
            variable=self.filter_modulo_var,
            values=['Todos', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'],
            font=('Arial', 12),
            width=180,
            height=35,
            corner_radius=8,
            fg_color='#2b2d42',
            button_color=HUTCHISON_COLORS['ports_sky_blue'],
            button_hover_color=HUTCHISON_COLORS['ports_sea_blue']
        )
        self.filter_modulo_menu.pack(side='left', padx=5)

        # Cargar módulos desde BD
        self.load_modules_for_filter()

        # Fila 2: Rango de Fechas
        filters_row2 = ctk.CTkFrame(self.advanced_filters_frame, fg_color='transparent')
        filters_row2.pack(fill='x', padx=20, pady=10)

        ctk.CTkLabel(
            filters_row2,
            text='📅 Rango de Fechas:',
            font=('Segoe UI', 13),
            text_color=theme['text']
        ).pack(side='left', padx=(0, 10))

        ctk.CTkLabel(
            filters_row2,
            text='Desde:',
            font=('Segoe UI', 11),
            text_color=theme['text_secondary']
        ).pack(side='left', padx=(0, 5))

        self.filter_fecha_desde = ctk.CTkEntry(
            filters_row2,
            placeholder_text='YYYY-MM-DD',
            font=('Segoe UI', 12),
            width=140,
            height=35,
            corner_radius=8
        )
        self.filter_fecha_desde.pack(side='left', padx=5)

        ctk.CTkLabel(
            filters_row2,
            text='Hasta:',
            font=('Segoe UI', 11),
            text_color=theme['text_secondary']
        ).pack(side='left', padx=(15, 5))

        self.filter_fecha_hasta = ctk.CTkEntry(
            filters_row2,
            placeholder_text='YYYY-MM-DD',
            font=('Segoe UI', 12),
            width=140,
            height=35,
            corner_radius=8
        )
        self.filter_fecha_hasta.pack(side='left', padx=5)

        # Fila 3: Botones de acción
        filters_row3 = ctk.CTkFrame(self.advanced_filters_frame, fg_color='transparent')
        filters_row3.pack(fill='x', padx=20, pady=(10, 20))

        ctk.CTkButton(
            filters_row3,
            text='✅ Aplicar Filtros',
            font=('Arial', 13, 'bold'),
            fg_color=HUTCHISON_COLORS['success'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            corner_radius=10,
            height=40,
            width=180,
            command=self.apply_advanced_filters
        ).pack(side='left', padx=5)

        ctk.CTkButton(
            filters_row3,
            text='🔄 Limpiar Filtros',
            font=('Arial', 13, 'bold'),
            fg_color=HUTCHISON_COLORS['warning'],
            hover_color=HUTCHISON_COLORS['danger'],
            corner_radius=10,
            height=40,
            width=180,
            command=self.clear_advanced_filters
        ).pack(side='left', padx=5)

        # Contador de resultados
        self.results_counter_label = ctk.CTkLabel(
            filters_row3,
            text='Mostrando 0 resultados',
            font=('Segoe UI', 12),
            text_color=theme['text_secondary']
        )
        self.results_counter_label.pack(side='right', padx=20)

        # Separador
        sep3 = ctk.CTkFrame(search_card, height=1, fg_color=theme['border'])
        sep3.pack(fill='x', padx=30, pady=10)

        # Botones rápidos
        quick_frame = ctk.CTkFrame(search_card, fg_color='transparent')
        quick_frame.pack(fill='x', padx=30, pady=20)

        ctk.CTkLabel(
            quick_frame,
            text='⚡  Consultas Rápidas:',
            font=('Arial', 16),
            text_color=theme['text']
        ).pack(side='left', padx=(0, 15))

        quick_btn1 = ctk.CTkButton(
            quick_frame,
            text='📋  Todos los Usuarios',
            font=('Arial', 14),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            corner_radius=10,
            height=40,
            command=self.query_new_users
        )
        quick_btn1.pack(side='left', padx=5)

        # Botón de datos de ejemplo
        example_btn = ctk.CTkButton(
            quick_frame,
            text='👁️  Ver Datos de Ejemplo',
            font=('Arial', 14),
            fg_color=HUTCHISON_COLORS['success'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            corner_radius=10,
            height=40,
            command=self.show_example_data
        )
        example_btn.pack(side='left', padx=5)

        # Card: Resultados
        results_card = ctk.CTkFrame(scroll_frame, fg_color=theme['surface'], corner_radius=20, border_width=1, border_color=theme['border'])
        results_card.pack(fill='both', expand=True, pady=10)

        results_header = ctk.CTkLabel(
            results_card,
            text='📊  Resultados',
            font=('Montserrat', 20, 'bold'),
            text_color=theme['text']
        )
        results_header.pack(padx=30, pady=(20, 10), anchor='w')

        # Container para resultados (usaremos tkinter Treeview aquí por compatibilidad)
        results_container_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        results_container = ctk.CTkFrame(results_card, fg_color=results_container_bg, corner_radius=10)
        results_container.pack(fill='both', expand=True, padx=30, pady=(10, 20))

        # Crear Treeview con estilo según tema
        import tkinter.ttk as ttk
        style = ttk.Style()
        style.theme_use('clam')

        if self.theme_manager.is_dark_mode():
            # Estilo oscuro
            style.configure('Themed.Treeview',
                background=theme['background'],
                foreground=theme['text'],
                fieldbackground=theme['background'],
                borderwidth=0,
                font=('Segoe UI', 10)
            )
            style.configure('Themed.Treeview.Heading',
                background=theme['surface'],
                foreground=theme['text'],
                borderwidth=1,
                font=('Segoe UI', 11, 'bold')
            )
            style.map('Themed.Treeview',
                background=[('selected', '#6c63ff')],
                foreground=[('selected', '#ffffff')]
            )
        else:
            # Estilo claro
            style.configure('Themed.Treeview',
                background='#ffffff',
                foreground=theme['text'],
                fieldbackground='#ffffff',
                borderwidth=0,
                font=('Segoe UI', 10)
            )
            style.configure('Themed.Treeview.Heading',
                background='#e8e8e8',
                foreground=theme['text'],
                borderwidth=1,
                font=('Segoe UI', 11, 'bold')
            )
            style.map('Themed.Treeview',
                background=[('selected', HUTCHISON_COLORS['ports_sky_blue'])],
                foreground=[('selected', '#ffffff')]
            )

        # Scrollbars
        vsb = ttk.Scrollbar(results_container, orient="vertical")
        hsb = ttk.Scrollbar(results_container, orient="horizontal")

        self.results_tree = ttk.Treeview(
            results_container,
            columns=(),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            style='Themed.Treeview'
        )

        vsb.config(command=self.results_tree.yview)
        hsb.config(command=self.results_tree.xview)

        self.results_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        results_container.grid_rowconfigure(0, weight=1)
        results_container.grid_columnconfigure(0, weight=1)

        # Configurar tags para filas alternadas según tema
        if self.theme_manager.is_dark_mode():
            self.results_tree.tag_configure('oddrow', background=theme['surface'])
            self.results_tree.tag_configure('evenrow', background=theme['background'])
        else:
            self.results_tree.tag_configure('oddrow', background='#f5f5f5')
            self.results_tree.tag_configure('evenrow', background='#ffffff')

    def show_configuracion_panel(self):
        """Panel de configuración con diseño 2x2"""
        self.clear_content_area()
        self.current_panel = 'configuracion'

        # Frame principal
        main_frame = ctk.CTkFrame(self.content_area, fg_color='transparent')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header
        header = ctk.CTkFrame(main_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 30))

        theme = self.theme_manager.get_current_theme()

        title = ctk.CTkLabel(
            header,
            text='Configuración',
            font=('Montserrat', 32, 'bold'),
            text_color=theme['text']
        )
        title.pack(side='left')

        # Grid frame para layout 2x2
        grid_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        grid_frame.pack(fill='both', expand=True)

        # Configurar grid 2x2
        grid_frame.grid_columnconfigure((0, 1), weight=1)
        grid_frame.grid_rowconfigure((0, 1), weight=1)

        # Definir PRIMARY_COLORS con colores Hutchison Ports
        PRIMARY_COLORS = {
            'accent_blue': HUTCHISON_COLORS['ports_sky_blue'],
            'accent_green': HUTCHISON_COLORS['success'],
            'accent_orange': HUTCHISON_COLORS['warning'],
            'accent_cyan': HUTCHISON_COLORS['ports_horizon_blue']
        }

        # Card 1: Gestión de Usuarios
        card1 = ConfigCard(
            grid_frame,
            icon='👥',
            title='Gestión de Usuarios',
            description='Agregar, editar o consultar usuarios del sistema.',
            button_text='Gestionar',
            button_color=PRIMARY_COLORS['accent_blue'],
            command=self.show_user_management
        )
        card1.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')

        # Card 2: Ticket de Soporte
        card2 = ConfigCard(
            grid_frame,
            icon='🎫',
            title='Ticket de Soporte',
            description='Crear un nuevo ticket de soporte para asistencia técnica.',
            button_text='Crear Ticket',
            button_color=PRIMARY_COLORS['accent_green'],
            command=self.open_support_ticket
        )
        card2.grid(row=0, column=1, padx=15, pady=15, sticky='nsew')

        # Card 3: Historial de Reportes
        card3 = ConfigCard(
            grid_frame,
            icon='📋',
            title='Historial de Reportes',
            description='Ver y descargar reportes PDF generados anteriormente.',
            button_text='Ver Historial',
            button_color=PRIMARY_COLORS['accent_orange'],
            command=self.open_report_history
        )
        card3.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')

        # Card 4: Acerca de
        card4 = ConfigCard(
            grid_frame,
            icon='ℹ️',
            title='Acerca de',
            description='Información de la versión y del desarrollador.',
            button_text='Ver Info',
            button_color=PRIMARY_COLORS['accent_cyan'],
            command=self.show_about
        )
        card4.grid(row=1, column=1, padx=15, pady=15, sticky='nsew')

    def _create_config_card(self, parent, icon, title, description, color, command):
        """Crear card de configuración"""
        card = ctk.CTkFrame(
            parent,
            fg_color='#2b2d42',
            corner_radius=20,
            border_width=1,
            border_color='#3a3d5c'
        )

        # Icono
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=('Segoe UI', 48),
            text_color=color
        )
        icon_label.pack(pady=(30, 10))

        # Título
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=('Montserrat', 20, 'bold'),
            text_color='#ffffff'
        )
        title_label.pack(pady=(0, 10))

        # Descripción
        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=('Arial', 12),
            text_color='#a0a0b0',
            wraplength=250
        )
        desc_label.pack(pady=(0, 20), padx=20)

        # Botón
        action_btn = ctk.CTkButton(
            card,
            text='Ejecutar',
            font=('Arial', 14, 'bold'),
            fg_color=color,
            hover_color=self._darken_color(color),
            corner_radius=10,
            height=40,
            width=150,
            command=command
        )
        action_btn.pack(pady=(0, 30))

        # Hover effect
        card.bind('<Enter>', lambda e: card.configure(border_color=color))
        card.bind('<Leave>', lambda e: card.configure(border_color='#3a3d5c'))

        return card

    def _darken_color(self, hex_color):
        """Oscurecer un color hex - Actualizado con colores Hutchison Ports"""
        # Map de colores Hutchison Ports a sus versiones hover
        color_map = {
            HUTCHISON_COLORS['ports_sky_blue']: HUTCHISON_COLORS['ports_sea_blue'],
            HUTCHISON_COLORS['success']: HUTCHISON_COLORS['ports_sea_blue'],
            HUTCHISON_COLORS['warning']: HUTCHISON_COLORS['danger'],
            HUTCHISON_COLORS['ports_horizon_blue']: HUTCHISON_COLORS['ports_sky_blue']
        }
        return color_map.get(hex_color, HUTCHISON_COLORS['ports_sea_blue'])

    # ==================== FUNCIONES DE DATOS (MANTENER LÓGICA ORIGINAL) ====================

    def _on_file_drop(self, event):
        """Manejar evento de drag & drop de archivos"""
        # Obtener ruta del archivo soltado
        file_path = event.data.strip('{}')

        # Validar extensión
        valid_extensions = ('.xlsx', '.xls', '.csv')
        if not file_path.lower().endswith(valid_extensions):
            messagebox.showerror(
                "Archivo Inválido",
                f"Por favor selecciona un archivo Excel o CSV.\n\n" +
                f"Extensiones válidas: {', '.join(valid_extensions)}\n" +
                f"Archivo recibido: {os.path.basename(file_path)}"
            )
            return

        # Validar que el archivo exista
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"El archivo no existe:\n{file_path}")
            return

        # Procesar archivo
        self._load_file(file_path)

    def select_transcript_file(self):
        """Seleccionar archivo Transcript Status"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Transcript Status",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")]
        )

        if file_path:
            self._load_file(file_path)

    def _load_file(self, file_path: str):
        """
        Carga un archivo y actualiza la UI

        Args:
            file_path: Ruta del archivo a cargar
        """
        self.current_file = file_path
        filename = os.path.basename(file_path)
        self.file_label.configure(text=filename, text_color='#51cf66')
        self.log_movement(f"Archivo seleccionado: {filename}")
        messagebox.showinfo("Archivo Seleccionado",
            f"Archivo cargado: {filename}\n\nAhora haz clic en 'Actualizar Base de Datos'")

    def update_database_from_file(self):
        """Actualizar base de datos desde archivo cargado"""
        if self.conn is None:
            messagebox.showerror("Error de Conexión",
                "No hay conexión a la base de datos.\nNo se puede actualizar.")
            return

        if not self.current_file:
            messagebox.showwarning("Sin Archivo",
                "Primero debes seleccionar un archivo Transcript Status")
            return

        try:
            self.log_movement("="*50)
            self.log_movement("🔄 INICIANDO ACTUALIZACIÓN DE BASE DE DATOS")
            self.log_movement("="*50)

            # Crear procesador
            processor = TranscriptProcessor(self.conn)

            # Procesar archivo
            stats = processor.process_file(self.current_file)

            # Mostrar estadísticas detalladas
            self.show_processing_stats(stats)

            # Mensaje de éxito
            messagebox.showinfo("Actualización Exitosa",
                f"✓ Base de datos actualizada correctamente\n\n" +
                f"Registros procesados: {stats['total_registros']:,}\n" +
                f"Usuarios nuevos: {stats['usuarios_nuevos']}\n" +
                f"Módulos nuevos: {stats['modulos_nuevos']}\n" +
                f"Inscripciones actualizadas: {stats['inscripciones_actualizadas']}")

            self.log_movement("✓ Actualización completada exitosamente")
            self.log_movement("="*50 + "\n")

        except Exception as e:
            error_msg = f"Error al actualizar base de datos: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.log_movement(f"✗ ERROR: {str(e)}")
            import traceback
            self.log_movement(traceback.format_exc())

    def log_movement(self, message):
        """Registrar movimiento en el panel"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        if hasattr(self, 'movements_text'):
            self.movements_text.insert('end', log_entry)
            self.movements_text.see('end')

    def show_processing_stats(self, stats):
        """Mostrar estadísticas de procesamiento"""
        self.log_movement("\n📊 ESTADÍSTICAS DE PROCESAMIENTO:")
        self.log_movement(f"  • Archivo: {stats['archivo']}")
        self.log_movement(f"  • Fecha: {stats['fecha_procesamiento']}")
        self.log_movement(f"  • Total registros: {stats['total_registros']:,}")
        self.log_movement(f"  • Usuarios únicos: {stats['usuarios_unicos']}")
        self.log_movement(f"  • Usuarios nuevos: {stats['usuarios_nuevos']}")
        self.log_movement(f"  • Módulos únicos: {stats['modulos_unicos']}")
        self.log_movement(f"  • Módulos nuevos: {stats['modulos_nuevos']}")
        self.log_movement(f"  • Inscripciones actualizadas: {stats['inscripciones_actualizadas']}")

        if stats['errores']:
            self.log_movement(f"\n⚠️  ERRORES ({len(stats['errores'])}):")
            for error in stats['errores'][:10]:  # Mostrar primeros 10
                self.log_movement(f"  • {error}")

    def search_user_by_id(self):
        """Buscar usuario por ID"""
        if self.cursor is None:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        user_id = self.search_entry.get().strip()
        if not user_id:
            messagebox.showwarning("Advertencia", "Ingrese un ID de usuario")
            return

        try:
            self.cursor.execute("""
                SELECT
                    u.UserId,
                    u.Nombre,
                    u.Email,
                    un.NombreUnidad,
                    u.Nivel,
                    u.Division,
                    m.NombreModulo,
                    pm.EstatusModuloUsuario,
                    CONVERT(VARCHAR(10), pm.FechaInicio, 103) as FechaAsignacion,
                    CONVERT(VARCHAR(10), pm.FechaFinalizacion, 103) as FechaFinalizacion
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                LEFT JOIN Instituto_ProgresoModulo pm ON u.UserId = pm.UserId
                LEFT JOIN Instituto_Modulo m ON pm.IdModulo = m.IdModulo
                WHERE u.UserId = ?
                ORDER BY m.NombreModulo
            """, (user_id,))

            results = self.cursor.fetchall()
            if results:
                self.display_search_results(results,
                    ['User ID', 'Nombre', 'Email', 'Unidad', 'Nivel', 'División',
                     'Módulo', 'Estatus Módulo', 'Fecha Inicio', 'Fecha Fin'])
            else:
                messagebox.showinfo("Sin resultados", "Usuario no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda: {str(e)}")

    def load_business_units(self):
        """Cargar unidades de negocio en combobox"""
        if self.cursor is None:
            return

        try:
            self.cursor.execute("SELECT DISTINCT NombreUnidad FROM Instituto_UnidadDeNegocio ORDER BY NombreUnidad")
            units = self.cursor.fetchall()
            unit_names = [unit[0] for unit in units]

            if hasattr(self, 'business_unit_combo'):
                self.business_unit_combo.configure(values=unit_names)
                if unit_names:
                    self.business_unit_combo.set(unit_names[0])
        except Exception as e:
            print(f"Error cargando unidades: {e}")

    def query_business_unit_from_combo(self):
        """Consultar por unidad de negocio seleccionada"""
        unit_name = self.business_unit_var.get()
        if not unit_name:
            messagebox.showwarning("Advertencia", "Seleccione una unidad de negocio")
            return

        try:
            self.cursor.execute("""
                SELECT
                    u.UserId,
                    u.Nombre,
                    u.Email,
                    un.NombreUnidad,
                    COUNT(DISTINCT pm.IdModulo) as TotalModulos,
                    SUM(CASE WHEN pm.EstatusModuloUsuario = 'Terminado' THEN 1 ELSE 0 END) as Completados
                FROM Instituto_Usuario u
                JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                LEFT JOIN Instituto_ProgresoModulo pm ON u.UserId = pm.UserId
                WHERE un.NombreUnidad = ?
                GROUP BY u.UserId, u.Nombre, u.Email, un.NombreUnidad
                ORDER BY u.Nombre
            """, (unit_name,))

            results = self.cursor.fetchall()
            if results:
                self.display_search_results(results,
                    ['User ID', 'Nombre', 'Email', 'Unidad', 'Total Módulos', 'Completados'])
            else:
                messagebox.showinfo("Sin resultados", f"No hay usuarios en {unit_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta: {str(e)}")

    def query_new_users(self):
        """Consultar todos los usuarios"""
        try:
            self.cursor.execute("""
                SELECT
                    u.UserId,
                    u.Nombre,
                    u.Email,
                    un.NombreUnidad,
                    COUNT(DISTINCT pm.IdModulo) as TotalModulos,
                    SUM(CASE WHEN pm.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as Completados
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                LEFT JOIN Instituto_ProgresoModulo pm ON u.UserId = pm.UserId
                GROUP BY u.UserId, u.Nombre, u.Email, un.NombreUnidad
                ORDER BY u.UserId
            """)

            results = self.cursor.fetchall()
            if results:
                self.display_search_results(results,
                    ['User ID', 'Nombre', 'Email', 'Unidad', 'Total Módulos', 'Completados'])
            else:
                messagebox.showinfo("Sin resultados", "No hay usuarios en el sistema")
        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta: {str(e)}")

    def display_search_results(self, results, columns):
        """Mostrar resultados en treeview"""
        # Limpiar treeview
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Configurar columnas
        self.results_tree['columns'] = columns
        self.results_tree['show'] = 'headings'

        # Diccionario de anchos fijos
        column_widths = {
            'User ID': 100,
            'Nombre': 200,
            'Email': 220,
            'Unidad': 150,
            'Nivel': 100,
            'División': 120,
            'Módulo': 250,
            'Estatus Módulo': 130,
            'Fecha Inicio': 100,
            'Fecha Fin': 100,
            'Total Módulos': 120,
            'Completados': 120
        }

        for col in columns:
            width = column_widths.get(col, 120)
            self.results_tree.heading(col, text=col, anchor='center')
            self.results_tree.column(col, width=width, minwidth=width, anchor='w')

        # Insertar datos con filas alternadas
        for idx, row in enumerate(results):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            values = [str(v) if v is not None else '' for v in row]
            self.results_tree.insert('', 'end', values=values, tags=(tag,))

    def update_emails(self):
        """Actualizar correos"""
        messagebox.showinfo("En Desarrollo", "Funcionalidad de actualizar correos")

    def update_users(self):
        """Actualizar usuarios"""
        messagebox.showinfo("En Desarrollo", "Funcionalidad de actualizar usuarios")

    def show_progress_stats(self):
        """Mostrar estadísticas de progreso"""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Instituto_Usuario")
            total_users = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT COUNT(*) FROM Instituto_Modulo")
            total_modules = self.cursor.fetchone()[0]

            self.cursor.execute("""
                SELECT
                    SUM(CASE WHEN EstatusModuloUsuario = 'Terminado' THEN 1 ELSE 0 END) as Completados,
                    SUM(CASE WHEN EstatusModuloUsuario = 'En Progreso' THEN 1 ELSE 0 END) as EnProgreso,
                    COUNT(*) as Total
                FROM Instituto_ProgresoModulo
            """)
            result = self.cursor.fetchone()

            msg = f"""
📊 ESTADÍSTICAS GENERALES

Usuarios: {total_users}
Módulos: {total_modules}

Inscripciones Completadas: {result[0]}
En Progreso: {result[1]}
Total Inscripciones: {result[2]}

Porcentaje Completado: {(result[0]/result[2]*100):.1f}%
"""
            messagebox.showinfo("Estadísticas", msg)
        except Exception as e:
            messagebox.showerror("Error", f"Error obteniendo estadísticas: {str(e)}")

    def show_about(self):
        """Mostrar información sobre la aplicación"""
        messagebox.showinfo("Acerca de",
            "SMART REPORTS V2.0\n\n" +
            "SISTEMA DE GESTIÓN DE CAPACITACIONES\n" +
            "INSTITUTO HUTCHISON PORTS\n\n" +
            "Desarrollado por: David Vera\n" +
            "© 2025 - TODOS LOS DERECHOS RESERVADOS")

    def open_support_ticket(self):
        """Abrir diálogo para crear ticket de soporte"""
        messagebox.showinfo(
            "Ticket de Soporte",
            "Función 'Ticket de Soporte' no implementada.\n\n" +
            "Esta funcionalidad permitirá crear tickets de soporte\n" +
            "para asistencia técnica del sistema."
        )

    def open_report_history(self):
        """Abrir historial de reportes generados"""
        messagebox.showinfo(
            "Historial de Reportes",
            "Función 'Historial de Reportes' no implementada.\n\n" +
            "Esta funcionalidad permitirá ver y descargar\n" +
            "reportes PDF generados anteriormente."
        )

    def show_user_management(self):
        """Mostrar ventana de gestión de usuarios"""
        if self.conn is None:
            messagebox.showerror("Error de Conexión",
                "No hay conexión a la base de datos.\n" +
                "No se puede gestionar usuarios sin conexión.")
            return

        # Abrir diálogo de gestión de usuarios
        dialog = UserManagementDialog(self.root, self.conn)
        self.root.wait_window(dialog)

        # Si se creó o actualizó un usuario, refrescar dashboard si está visible
        if dialog.result in ['created', 'updated'] and self.current_panel == 'dashboard':
            self.show_dashboard_panel()

    def backup_database(self):
        """Crear respaldo de la base de datos"""
        from smart_reports.config.settings import DB_TYPE

        try:
            if DB_TYPE == 'sqlserver':
                messagebox.showinfo("Respaldo SQL Server",
                    "Para respaldar SQL Server:\n\n" +
                    "1. Usa SQL Server Management Studio\n" +
                    "2. Click derecho en la base de datos\n" +
                    "3. Tasks → Back Up...\n\n" +
                    "O ejecuta:\n" +
                    "BACKUP DATABASE TNGCORE TO DISK = 'C:\\Backups\\TNGCORE.bak'")
            else:  # MySQL
                messagebox.showinfo("Respaldo MySQL",
                    "Para respaldar MySQL:\n\n" +
                    "Ejecuta en terminal:\n" +
                    "mysqldump -u root -p tngcore > backup.sql\n\n" +
                    "O usa MySQL Workbench:\n" +
                    "Server → Data Export")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear respaldo:\n{str(e)}")

    def show_database_config(self):
        """Mostrar configuración de base de datos"""
        from smart_reports.config.settings import DB_TYPE, SQLSERVER_CONFIG, MYSQL_CONFIG

        current = "SQL Server (Trabajo)" if DB_TYPE == 'sqlserver' else "MySQL (Casa)"

        messagebox.showinfo("Configuración de Base de Datos",
            f"Base de datos actual: {current}\n\n" +
            f"Para cambiar:\n" +
            f"1. Edita: smart_reports/config/settings.py\n" +
            f"2. Cambia DB_TYPE a 'sqlserver' o 'mysql'\n" +
            f"3. Reinicia la aplicación\n\n" +
            f"SQL Server: {SQLSERVER_CONFIG['server']}\n" +
            f"MySQL: {MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}")

    def show_example_data(self):
        """Mostrar datos de ejemplo en la tabla de resultados"""
        # Datos de ejemplo
        example_data = [
            ('U001', 'Juan Pérez López', 'juan.perez@hp.com', 'Operaciones Portuarias', 'Supervisor', 'Operaciones',
             'Seguridad Industrial', 'Terminado', '15/01/2024', '20/02/2024'),
            ('U002', 'María González', 'maria.gonzalez@hp.com', 'Logística y Almacenamiento', 'Jefe de Turno', 'Logística',
             'Operación de Grúas', 'En Progreso', '01/02/2024', ''),
            ('U003', 'Carlos Ramírez', 'carlos.ramirez@hp.com', 'Mantenimiento', 'Técnico', 'Mantenimiento',
             'Primeros Auxilios', 'Terminado', '10/01/2024', '15/02/2024'),
            ('U004', 'Ana Martínez', 'ana.martinez@hp.com', 'Administración', 'Analista', 'Admin',
             'Comunicación Efectiva', 'En Progreso', '05/02/2024', ''),
            ('U005', 'Roberto Silva', 'roberto.silva@hp.com', 'Seguridad', 'Guardia', 'Seguridad',
             'Prevención de Riesgos', 'Registrado', '12/02/2024', ''),
            ('U006', 'Laura Fernández', 'laura.fernandez@hp.com', 'Operaciones Portuarias', 'Operador', 'Operaciones',
             'Manejo de Cargas', 'Terminado', '08/01/2024', '25/01/2024'),
            ('U007', 'Diego Torres', 'diego.torres@hp.com', 'Logística y Almacenamiento', 'Coordinador', 'Logística',
             'Normativa Portuaria', 'En Progreso', '20/01/2024', ''),
            ('U008', 'Patricia Morales', 'patricia.morales@hp.com', 'Mantenimiento', 'Supervisor', 'Mantenimiento',
             'Seguridad Industrial', 'Terminado', '03/01/2024', '10/02/2024'),
        ]

        columns = ['User ID', 'Nombre', 'Email', 'Unidad', 'Nivel', 'División',
                   'Módulo', 'Estatus Módulo', 'Fecha Inicio', 'Fecha Fin']

        self.display_search_results(example_data, columns)

    # ==================== FILTROS AVANZADOS ====================

    def toggle_advanced_filters(self):
        """Mostrar/ocultar panel de filtros avanzados"""
        if self.filters_expanded.get():
            # Ocultar filtros
            self.advanced_filters_frame.pack_forget()
            self.toggle_filters_btn.configure(text='🔽  Mostrar Filtros Avanzados')
            self.filters_expanded.set(False)
        else:
            # Mostrar filtros
            self.advanced_filters_frame.pack(fill='x', padx=30, pady=(10, 0))
            self.toggle_filters_btn.configure(text='🔼  Ocultar Filtros Avanzados')
            self.filters_expanded.set(True)

    def load_modules_for_filter(self):
        """Cargar módulos desde la BD para el filtro"""
        if not self.cursor:
            return

        try:
            self.cursor.execute("""
                SELECT DISTINCT IdModulo, NombreModulo
                FROM Instituto_Modulo
                ORDER BY IdModulo
            """)
            modules = [row[1] for row in self.cursor.fetchall()]  # row[1] es NombreModulo
            if modules:
                self.filter_modulo_menu.configure(values=['Todos'] + modules)
        except Exception as e:
            print(f"Error cargando módulos: {e}")

    def apply_advanced_filters(self):
        """Aplicar filtros avanzados y ejecutar búsqueda"""
        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        # Obtener valores de filtros
        estado = self.filter_estado_var.get()
        modulo = self.filter_modulo_var.get()
        fecha_desde = self.filter_fecha_desde.get().strip()
        fecha_hasta = self.filter_fecha_hasta.get().strip()

        # Construir query dinámica
        base_query = """
            SELECT DISTINCT
                u.UserId,
                u.Nombre,
                u.Email,
                un.NombreUnidad,
                m.NombreModulo,
                pm.EstatusModuloUsuario,
                pm.FechaInicio,
                pm.FechaFin
            FROM Instituto_Usuario u
            LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
            LEFT JOIN Instituto_ProgresoModulo pm ON u.UserId = pm.UserId
            LEFT JOIN Instituto_Modulo m ON pm.IdModulo = m.IdModulo
            WHERE 1=1
        """

        params = []

        # Filtro por Estado
        if estado != 'Todos':
            if estado == 'Completado':
                base_query += " AND pm.EstatusModuloUsuario = 'Terminado'"
            elif estado == 'En Proceso':
                base_query += " AND pm.EstatusModuloUsuario = 'En Proceso'"
            elif estado == 'Sin Iniciar':
                base_query += " AND (pm.EstatusModuloUsuario IS NULL OR pm.EstatusModuloUsuario = 'Sin Iniciar')"

        # Filtro por Módulo
        if modulo != 'Todos':
            base_query += " AND m.NombreModulo = ?"
            params.append(modulo)

        # Filtro por Rango de Fechas
        if fecha_desde:
            base_query += " AND pm.FechaInicio >= ?"
            params.append(fecha_desde)

        if fecha_hasta:
            base_query += " AND pm.FechaFin <= ?"
            params.append(fecha_hasta)

        base_query += " ORDER BY u.Nombre"

        try:
            self.cursor.execute(base_query, params)
            results = self.cursor.fetchall()

            columns = ['UserId', 'Nombre', 'Email', 'Unidad de Negocio',
                      'Módulo', 'Estatus', 'Fecha Inicio', 'Fecha Fin']

            self.display_search_results(results, columns)

            # Actualizar contador
            count = len(results)
            self.results_counter_label.configure(text=f'Mostrando {count} resultado{"s" if count != 1 else ""}')

        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar filtros:\n{str(e)}")
            print(f"Error detallado: {e}")

    def clear_advanced_filters(self):
        """Limpiar todos los filtros avanzados"""
        self.filter_estado_var.set('Todos')
        self.filter_modulo_var.set('Todos')
        self.filter_fecha_desde.delete(0, 'end')
        self.filter_fecha_hasta.delete(0, 'end')
        self.results_counter_label.configure(text='Mostrando 0 resultados')

        # Limpiar resultados
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        messagebox.showinfo("Filtros Limpiados", "Los filtros han sido restaurados a sus valores por defecto")

    # ==================== GESTIÓN DE TEMAS ====================

    def _handle_theme_change(self, theme_colors: dict):
        """
        Callback llamado cuando el usuario cambia el tema desde el sidebar

        Args:
            theme_colors: Diccionario con los colores del nuevo tema
        """
        # Actualizar CustomTkinter appearance mode
        appearance = "dark" if self.theme_manager.is_dark_mode() else "light"
        ctk.set_appearance_mode(appearance)

        # Actualizar colores del contenedor principal y área de contenido
        self.main_container.configure(fg_color=theme_colors['background'])
        self.content_area.configure(fg_color=theme_colors['background'])

        # Recargar panel actual para aplicar nuevos colores
        if self.current_panel == 'dashboard':
            self.show_dashboard_panel()
        elif self.current_panel == 'consultas':
            self.show_consultas_panel()
        elif self.current_panel == 'actualizar':
            self.show_actualizar_panel()
        elif self.current_panel == 'configuracion':
            self.show_configuracion_panel()

    def _on_theme_changed(self, theme_colors: dict):
        """
        Callback llamado por el ThemeManager cuando cambia el tema

        Args:
            theme_colors: Diccionario con los colores del nuevo tema
        """
        # Este método permite que otros componentes también actualicen sus colores
        pass


def main():
    """Función principal"""
    root = ctk.CTk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()

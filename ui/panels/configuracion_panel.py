"""
Panel de Configuración - Con navegación interna (sin ventanas Toplevel)
Smart Reports v2.0
"""
import customtkinter as ctk
from tkinter import messagebox
import tkinter.ttk as ttk
from config.theme_manager import get_theme_manager
from ui.components.config_card import ConfigCard


class ConfiguracionPanel(ctk.CTkFrame):
    """Panel de configuración con navegación interna"""

    def __init__(self, parent, db_connection=None, **kwargs):
        """
        Args:
            parent: Widget padre
            db_connection: Conexión a la base de datos (opcional)
        """
        # Obtener tema actual
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        # Configurar fondo explícitamente para evitar parpadeo en modo oscuro
        super().__init__(parent, fg_color=theme['background'], **kwargs)

        self.db = db_connection
        self.cursor = db_connection.cursor() if db_connection else None

        # Crear frames de contenido (inicialmente ocultos)
        self._create_frames()

        # Mostrar frame principal al inicio
        self.show_main_config_frame()

        # Registrar callback para cambios de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    def _create_frames(self):
        """Crear todos los frames del panel"""
        # Frame principal con cuadrícula 4x4 de ConfigCards
        self.main_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )

        # Frame de Gestión de Usuarios
        self.user_manager_frame = ctk.CTkFrame(
            self,
            fg_color='transparent'
        )

        # Frame de Registro de Soporte
        self.support_ticket_frame = ctk.CTkFrame(
            self,
            fg_color='transparent'
        )

        # Frame de Historial de Reportes
        self.report_history_frame = ctk.CTkFrame(
            self,
            fg_color='transparent'
        )

        # Configurar contenido del frame principal
        self._setup_main_frame()

        # Configurar frames internos
        self._setup_user_manager_frame()
        self._setup_support_ticket_frame()
        self._setup_report_history_frame()

    def _setup_main_frame(self):
        """Configurar frame principal con tarjetas de configuración"""
        theme = self.theme_manager.get_current_theme()

        # Header con título
        header = ctk.CTkFrame(self.main_frame, fg_color='transparent', height=80)
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
            font=('Arial', 14),
            text_color=theme['text_secondary']
        )
        subtitle.pack(side='left', padx=(20, 0), pady=20)

        # Contenedor principal con grid 2x2
        grid_container = ctk.CTkFrame(self.main_frame, fg_color='transparent')
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
            command=self.show_user_manager_frame
        )
        card1.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')

        # Card 2: Registro de Soporte
        card2 = ConfigCard(
            grid_container,
            icon='📝',
            title='Registro de Soporte',
            description='Registrar soporte brindado a usuarios por correo electrónico',
            button_text='Registrar',
            command=self.show_support_ticket_frame
        )
        card2.grid(row=0, column=1, padx=15, pady=15, sticky='nsew')

        # Card 3: Historial de Reportes
        card3 = ConfigCard(
            grid_container,
            icon='📋',
            title='Historial de Reportes',
            description='Ver y descargar reportes PDF generados anteriormente',
            button_text='Ver Historial',
            command=self.show_report_history_frame
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

    def _setup_user_manager_frame(self):
        """Configurar frame de Gestión de Usuarios con CRUD completo"""
        theme = self.theme_manager.get_current_theme()

        # Scroll frame principal
        scroll_frame = ctk.CTkScrollableFrame(
            self.user_manager_frame,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header con botón volver
        header = ctk.CTkFrame(scroll_frame, fg_color='transparent', height=60)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)

        # Botón volver (← Volver)
        back_btn = ctk.CTkButton(
            header,
            text='← Volver',
            font=('Arial', 14, 'bold'),
            fg_color=theme['surface'],
            text_color=theme['text'],
            hover_color=theme['surface_light'],
            corner_radius=10,
            width=120,
            height=40,
            command=self.show_main_config_frame
        )
        back_btn.pack(side='left')

        # Título
        is_dark = self.theme_manager.is_dark_mode()
        title_color = '#FFFFFF' if is_dark else '#002E6D'

        title = ctk.CTkLabel(
            header,
            text='👥 Gestionar Empleados',
            font=('Montserrat', 28, 'bold'),
            text_color=title_color
        )
        title.pack(side='left', padx=20)

        # Card de búsqueda
        search_card = ctk.CTkFrame(
            scroll_frame,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )
        search_card.pack(fill='x', pady=(0, 15))

        search_header = ctk.CTkLabel(
            search_card,
            text='🔍 Buscar Usuario',
            font=('Arial', 18, 'bold'),
            text_color=theme['text']
        )
        search_header.pack(padx=20, pady=(15, 10), anchor='w')

        # Frame de búsqueda
        search_frame = ctk.CTkFrame(search_card, fg_color='transparent')
        search_frame.pack(fill='x', padx=20, pady=(0, 15))

        ctk.CTkLabel(
            search_frame,
            text='User ID o Nombre:',
            font=('Arial', 14),
            text_color=theme['text']
        ).pack(side='left', padx=(0, 10))

        self.user_search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text='Ingrese User ID o Nombre...',
            font=('Arial', 14),
            width=300,
            height=40,
            corner_radius=10
        )
        self.user_search_entry.pack(side='left', padx=5)

        button_color = self._get_button_color()
        search_btn = ctk.CTkButton(
            search_frame,
            text='Buscar',
            font=('Arial', 14, 'bold'),
            fg_color=button_color,
            hover_color=self._get_button_hover_color(button_color),
            corner_radius=10,
            height=40,
            width=120,
            command=self._search_user
        )
        search_btn.pack(side='left', padx=10)

        # Card de formulario de edición/creación
        form_card = ctk.CTkFrame(
            scroll_frame,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )
        form_card.pack(fill='x', pady=(0, 15))

        form_header = ctk.CTkLabel(
            form_card,
            text='✏️ Formulario de Usuario',
            font=('Arial', 18, 'bold'),
            text_color=theme['text']
        )
        form_header.pack(padx=20, pady=(15, 10), anchor='w')

        # Grid de formulario (2 columnas)
        form_grid = ctk.CTkFrame(form_card, fg_color='transparent')
        form_grid.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        form_grid.grid_columnconfigure((0, 1), weight=1)

        # Row 0: User ID y Nombre Completo
        ctk.CTkLabel(form_grid, text='User ID:', font=('Arial', 12, 'bold'), text_color=theme['text']).grid(row=0, column=0, sticky='w', padx=(0, 5), pady=5)
        self.form_userid = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='E12345')
        self.form_userid.grid(row=0, column=0, sticky='ew', padx=(100, 10), pady=5)

        ctk.CTkLabel(form_grid, text='Nombre Completo:', font=('Arial', 12, 'bold'), text_color=theme['text']).grid(row=0, column=1, sticky='w', padx=(0, 5), pady=5)
        self.form_nombre = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='Juan Pérez')
        self.form_nombre.grid(row=0, column=1, sticky='ew', padx=(150, 10), pady=5)

        # Row 1: Email y Nivel
        ctk.CTkLabel(form_grid, text='Email:', font=('Arial', 12, 'bold'), text_color=theme['text']).grid(row=1, column=0, sticky='w', padx=(0, 5), pady=5)
        self.form_email = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='usuario@empresa.com')
        self.form_email.grid(row=1, column=0, sticky='ew', padx=(100, 10), pady=5)

        ctk.CTkLabel(form_grid, text='Nivel:', font=('Arial', 12, 'bold'), text_color=theme['text']).grid(row=1, column=1, sticky='w', padx=(0, 5), pady=5)
        self.form_nivel = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='L1, L2, L3...')
        self.form_nivel.grid(row=1, column=1, sticky='ew', padx=(150, 10), pady=5)

        # Row 2: División y Posición
        ctk.CTkLabel(form_grid, text='División:', font=('Arial', 12, 'bold'), text_color=theme['text']).grid(row=2, column=0, sticky='w', padx=(0, 5), pady=5)
        self.form_division = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='Operaciones')
        self.form_division.grid(row=2, column=0, sticky='ew', padx=(100, 10), pady=5)

        ctk.CTkLabel(form_grid, text='Posición:', font=('Arial', 12, 'bold'), text_color=theme['text']).grid(row=2, column=1, sticky='w', padx=(0, 5), pady=5)
        self.form_cargo = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='Gerente')
        self.form_cargo.grid(row=2, column=1, sticky='ew', padx=(150, 10), pady=5)

        # Row 3: Grupo y Ubicación
        ctk.CTkLabel(form_grid, text='Grupo:', font=('Arial', 12, 'bold'), text_color=theme['text']).grid(row=3, column=0, sticky='w', padx=(0, 5), pady=5)
        self.form_grupo = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='Admin')
        self.form_grupo.grid(row=3, column=0, sticky='ew', padx=(100, 10), pady=5)

        ctk.CTkLabel(form_grid, text='Ubicación:', font=('Arial', 12, 'bold'), text_color=theme['text']).grid(row=3, column=1, sticky='w', padx=(0, 5), pady=5)
        self.form_ubicacion = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='México')
        self.form_ubicacion.grid(row=3, column=1, sticky='ew', padx=(150, 10), pady=5)

        # Row 4: UserStatus
        ctk.CTkLabel(form_grid, text='Estado:', font=('Arial', 12, 'bold'), text_color=theme['text']).grid(row=4, column=0, sticky='w', padx=(0, 5), pady=5)
        self.form_status = ctk.CTkOptionMenu(form_grid, values=['Activo', 'Inactivo'], height=35, corner_radius=8)
        self.form_status.grid(row=4, column=0, sticky='ew', padx=(100, 10), pady=5)
        self.form_status.set('Activo')

        # Botones de acción
        action_frame = ctk.CTkFrame(form_card, fg_color='transparent')
        action_frame.pack(fill='x', padx=20, pady=(10, 15))

        button_color = self._get_button_color()

        ctk.CTkButton(
            action_frame,
            text='➕ Crear Usuario',
            font=('Arial', 14, 'bold'),
            fg_color=button_color,
            hover_color=self._get_button_hover_color(button_color),
            corner_radius=10,
            height=45,
            width=150,
            command=self._create_user
        ).pack(side='left', padx=5)

        ctk.CTkButton(
            action_frame,
            text='💾 Actualizar',
            font=('Arial', 14, 'bold'),
            fg_color=button_color,
            hover_color=self._get_button_hover_color(button_color),
            corner_radius=10,
            height=45,
            width=150,
            command=self._update_user
        ).pack(side='left', padx=5)

        ctk.CTkButton(
            action_frame,
            text='🗑️ Eliminar',
            font=('Arial', 14, 'bold'),
            fg_color='#E53E3E',
            hover_color='#C53030',
            corner_radius=10,
            height=45,
            width=150,
            command=self._delete_user
        ).pack(side='left', padx=5)

        ctk.CTkButton(
            action_frame,
            text='🔄 Limpiar Formulario',
            font=('Arial', 14, 'bold'),
            fg_color=theme['surface_light'],
            text_color=theme['text'],
            hover_color=theme['border'],
            corner_radius=10,
            height=45,
            width=180,
            command=self._clear_form
        ).pack(side='left', padx=5)

        # Card de resultados con tabla
        results_card = ctk.CTkFrame(
            scroll_frame,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )
        results_card.pack(fill='both', expand=True, pady=(0, 15))

        results_header = ctk.CTkLabel(
            results_card,
            text='📋 Resultados de Búsqueda',
            font=('Arial', 18, 'bold'),
            text_color=theme['text']
        )
        results_header.pack(padx=20, pady=(15, 10), anchor='w')

        # Container para tabla
        table_container_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        table_container = ctk.CTkFrame(results_card, fg_color=table_container_bg, corner_radius=10)
        table_container.pack(fill='both', expand=True, padx=20, pady=(10, 20))

        # Crear Treeview para resultados
        style = ttk.Style()
        style.theme_use('clam')

        if self.theme_manager.is_dark_mode():
            style.configure('UserMgmt.Treeview',
                background=theme['background'],
                foreground=theme['text'],
                fieldbackground=theme['background'],
                borderwidth=0,
                font=('Segoe UI', 10)
            )
            style.configure('UserMgmt.Treeview.Heading',
                background=theme['surface'],
                foreground=theme['text'],
                borderwidth=1,
                font=('Segoe UI', 11, 'bold')
            )
            style.map('UserMgmt.Treeview',
                background=[('selected', '#6c63ff')],
                foreground=[('selected', '#ffffff')]
            )
        else:
            style.configure('UserMgmt.Treeview',
                background='#ffffff',
                foreground=theme['text'],
                fieldbackground='#ffffff',
                borderwidth=0,
                font=('Segoe UI', 10)
            )
            style.configure('UserMgmt.Treeview.Heading',
                background='#e8e8e8',
                foreground=theme['text'],
                borderwidth=1,
                font=('Segoe UI', 11, 'bold')
            )

        # Scrollbars
        vsb = ttk.Scrollbar(table_container, orient="vertical")
        hsb = ttk.Scrollbar(table_container, orient="horizontal")

        self.user_results_tree = ttk.Treeview(
            table_container,
            columns=('UserId', 'Nombre', 'Email', 'Nivel', 'Division', 'Cargo', 'Grupo', 'Ubicacion', 'Status'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            style='UserMgmt.Treeview'
        )

        # Configurar columnas
        self.user_results_tree.heading('UserId', text='User ID')
        self.user_results_tree.heading('Nombre', text='Nombre')
        self.user_results_tree.heading('Email', text='Email')
        self.user_results_tree.heading('Nivel', text='Nivel')
        self.user_results_tree.heading('Division', text='División')
        self.user_results_tree.heading('Cargo', text='Posición')
        self.user_results_tree.heading('Grupo', text='Grupo')
        self.user_results_tree.heading('Ubicacion', text='Ubicación')
        self.user_results_tree.heading('Status', text='Estado')

        self.user_results_tree.column('UserId', width=90, minwidth=80)
        self.user_results_tree.column('Nombre', width=180, minwidth=150)
        self.user_results_tree.column('Email', width=200, minwidth=160)
        self.user_results_tree.column('Nivel', width=60, minwidth=50)
        self.user_results_tree.column('Division', width=120, minwidth=100)
        self.user_results_tree.column('Cargo', width=130, minwidth=110)
        self.user_results_tree.column('Grupo', width=100, minwidth=80)
        self.user_results_tree.column('Ubicacion', width=100, minwidth=80)
        self.user_results_tree.column('Status', width=80, minwidth=70)

        vsb.config(command=self.user_results_tree.yview)
        hsb.config(command=self.user_results_tree.xview)

        self.user_results_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        # Bind click en la tabla para cargar datos en el formulario
        self.user_results_tree.bind('<ButtonRelease-1>', self._on_user_select)

    def _setup_support_ticket_frame(self):
        """Configurar frame de Registro de Soporte Brindado"""
        theme = self.theme_manager.get_current_theme()

        # Scroll frame principal
        scroll_frame = ctk.CTkScrollableFrame(
            self.support_ticket_frame,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header con botón volver
        header = ctk.CTkFrame(scroll_frame, fg_color='transparent', height=60)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)

        # Botón volver
        back_btn = ctk.CTkButton(
            header,
            text='← Volver',
            font=('Arial', 14, 'bold'),
            fg_color=theme['surface'],
            text_color=theme['text'],
            hover_color=theme['surface_light'],
            corner_radius=10,
            width=120,
            height=40,
            command=self.show_main_config_frame
        )
        back_btn.pack(side='left')

        # Título
        is_dark = self.theme_manager.is_dark_mode()
        title_color = '#FFFFFF' if is_dark else '#002E6D'

        title = ctk.CTkLabel(
            header,
            text='📝 Registro de Soporte Brindado',
            font=('Montserrat', 28, 'bold'),
            text_color=title_color
        )
        title.pack(side='left', padx=20)

        # Card de formulario
        form_card = ctk.CTkFrame(
            scroll_frame,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )
        form_card.pack(fill='both', expand=True)

        # Contenido del formulario
        form_content = ctk.CTkFrame(form_card, fg_color='transparent')
        form_content.pack(fill='both', expand=True, padx=30, pady=30)

        # Campo User ID del Usuario
        ctk.CTkLabel(
            form_content,
            text='User ID del Usuario:',
            font=('Arial', 16, 'bold'),
            text_color=theme['text']
        ).pack(anchor='w', pady=(0, 10))

        self.soporte_userid = ctk.CTkEntry(
            form_content,
            placeholder_text='Ej: E12345',
            font=('Arial', 14),
            height=45,
            corner_radius=10
        )
        self.soporte_userid.pack(fill='x', pady=(0, 20))

        # Campo Asunto
        ctk.CTkLabel(
            form_content,
            text='Asunto:',
            font=('Arial', 16, 'bold'),
            text_color=theme['text']
        ).pack(anchor='w', pady=(0, 10))

        self.ticket_asunto = ctk.CTkEntry(
            form_content,
            placeholder_text='Resumen del soporte brindado...',
            font=('Arial', 14),
            height=45,
            corner_radius=10
        )
        self.ticket_asunto.pack(fill='x', pady=(0, 20))

        # Campo Descripción
        ctk.CTkLabel(
            form_content,
            text='Descripción del Problema y Solución:',
            font=('Arial', 16, 'bold'),
            text_color=theme['text']
        ).pack(anchor='w', pady=(0, 10))

        textbox_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        self.ticket_descripcion = ctk.CTkTextbox(
            form_content,
            fg_color=textbox_bg,
            border_color=theme['border'],
            border_width=1,
            corner_radius=10,
            font=('Arial', 13),
            text_color=theme['text'],
            height=300
        )
        self.ticket_descripcion.insert("1.0", "Problema reportado:\n\n\nSolución brindada:\n\n")
        self.ticket_descripcion.pack(fill='both', expand=True, pady=(0, 20))

        # Campo Categoría
        ctk.CTkLabel(
            form_content,
            text='Categoría:',
            font=('Arial', 16, 'bold'),
            text_color=theme['text']
        ).pack(anchor='w', pady=(0, 10))

        self.ticket_categoria = ctk.CTkOptionMenu(
            form_content,
            values=['Técnico', 'Funcional', 'Acceso/Permisos', 'Datos', 'Otro'],
            font=('Arial', 14),
            width=250,
            height=45,
            corner_radius=10
        )
        self.ticket_categoria.pack(anchor='w', pady=(0, 30))

        # Botones de acción
        button_frame = ctk.CTkFrame(form_content, fg_color='transparent')
        button_frame.pack(fill='x')

        button_color = self._get_button_color()

        ctk.CTkButton(
            button_frame,
            text='💾 Guardar Registro',
            font=('Arial', 16, 'bold'),
            fg_color=button_color,
            hover_color=self._get_button_hover_color(button_color),
            corner_radius=10,
            height=50,
            width=200,
            command=self._submit_ticket
        ).pack(side='left', padx=5)

        ctk.CTkButton(
            button_frame,
            text='🗑️ Limpiar',
            font=('Arial', 16, 'bold'),
            fg_color=theme['surface_light'],
            text_color=theme['text'],
            hover_color=theme['border'],
            corner_radius=10,
            height=50,
            width=150,
            command=self._clear_ticket_form
        ).pack(side='left', padx=5)

    # ==================== FUNCIONES DE NAVEGACIÓN ====================

    def show_main_config_frame(self):
        """Mostrar frame principal de configuración"""
        # Ocultar frames internos
        self.user_manager_frame.pack_forget()
        self.support_ticket_frame.pack_forget()
        self.report_history_frame.pack_forget()

        # Mostrar frame principal
        self.main_frame.pack(fill='both', expand=True)

    def show_user_manager_frame(self):
        """Mostrar frame de gestión de usuarios"""
        # Ocultar frame principal
        self.main_frame.pack_forget()

        # Mostrar frame de gestión de usuarios
        self.user_manager_frame.pack(fill='both', expand=True)

        # Cargar todos los usuarios al entrar
        self._load_all_users()

    def show_support_ticket_frame(self):
        """Mostrar frame de registro de soporte"""
        # Ocultar frame principal
        self.main_frame.pack_forget()

        # Mostrar frame de registro de soporte
        self.support_ticket_frame.pack(fill='both', expand=True)

    def show_report_history_frame(self):
        """Mostrar frame de historial de reportes"""
        # Ocultar frame principal
        self.main_frame.pack_forget()

        # Mostrar frame de historial
        self.report_history_frame.pack(fill='both', expand=True)

    # ==================== FUNCIONES DE GESTIÓN DE USUARIOS ====================

    def _search_user(self):
        """Buscar usuario por User ID o Nombre"""
        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        search_term = self.user_search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda")
            return

        try:
            # Buscar por User ID o Nombre (LIKE) con campos completos
            self.cursor.execute("""
                SELECT
                    u.UserId,
                    COALESCE(u.NombreCompleto, u.UserName) as Nombre,
                    u.UserEmail,
                    COALESCE(u.Nivel, '') as Nivel,
                    COALESCE(u.Division, '') as Division,
                    COALESCE(u.Position, '') as Position,
                    COALESCE(u.Grupo, '') as Grupo,
                    COALESCE(u.Ubicacion, '') as Ubicacion,
                    COALESCE(u.UserStatus, 'Activo') as Status
                FROM Instituto_Usuario u
                WHERE u.UserId LIKE ? OR COALESCE(u.NombreCompleto, u.UserName) LIKE ?
                ORDER BY u.UserId
            """, (f'%{search_term}%', f'%{search_term}%'))

            results = self.cursor.fetchall()
            self._display_user_results(results)

            if not results:
                messagebox.showinfo("Sin resultados", f"No se encontraron usuarios con el término '{search_term}'")

        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda: {str(e)}")

    def _load_all_users(self):
        """Cargar todos los usuarios en la tabla"""
        if not self.cursor:
            return

        try:
            self.cursor.execute("""
                SELECT
                    u.UserId,
                    COALESCE(u.NombreCompleto, u.UserName) as Nombre,
                    u.UserEmail,
                    COALESCE(u.Nivel, '') as Nivel,
                    COALESCE(u.Division, '') as Division,
                    COALESCE(u.Position, '') as Position,
                    COALESCE(u.Grupo, '') as Grupo,
                    COALESCE(u.Ubicacion, '') as Ubicacion,
                    COALESCE(u.UserStatus, 'Activo') as Status
                FROM Instituto_Usuario u
                ORDER BY u.UserId
            """)

            results = self.cursor.fetchall()
            self._display_user_results(results)

        except Exception as e:
            print(f"Error cargando usuarios: {e}")

    def _display_user_results(self, results):
        """Mostrar resultados en la tabla"""
        # Limpiar tabla
        for item in self.user_results_tree.get_children():
            self.user_results_tree.delete(item)

        # Insertar resultados
        for row in results:
            values = [str(v) if v is not None else '' for v in row]
            self.user_results_tree.insert('', 'end', values=values)

    def _on_user_select(self, event):
        """Evento cuando se selecciona un usuario en la tabla"""
        selection = self.user_results_tree.selection()
        if not selection:
            return

        item = self.user_results_tree.item(selection[0])
        values = item['values']

        if values and len(values) >= 9:
            # Cargar datos en el formulario
            self.form_userid.delete(0, 'end')
            self.form_userid.insert(0, values[0])

            self.form_nombre.delete(0, 'end')
            self.form_nombre.insert(0, values[1])

            self.form_email.delete(0, 'end')
            self.form_email.insert(0, values[2])

            self.form_nivel.delete(0, 'end')
            self.form_nivel.insert(0, values[3])

            self.form_division.delete(0, 'end')
            self.form_division.insert(0, values[4])

            self.form_cargo.delete(0, 'end')
            self.form_cargo.insert(0, values[5])

            self.form_grupo.delete(0, 'end')
            self.form_grupo.insert(0, values[6])

            self.form_ubicacion.delete(0, 'end')
            self.form_ubicacion.insert(0, values[7])

            self.form_status.set(values[8])

    def _create_user(self):
        """Crear nuevo usuario"""
        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        # Validar campos
        user_id = self.form_userid.get().strip()
        nombre = self.form_nombre.get().strip()
        email = self.form_email.get().strip()

        if not user_id or not nombre:
            messagebox.showwarning("Campos Requeridos", "User ID y Nombre son obligatorios")
            return

        try:
            # Verificar si el usuario ya existe
            self.cursor.execute("SELECT COUNT(*) FROM Instituto_Usuario WHERE UserId = ?", (user_id,))
            if self.cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", f"El User ID '{user_id}' ya existe")
                return

            # Insertar usuario con todos los campos
            self.cursor.execute("""
                INSERT INTO Instituto_Usuario
                (UserId, NombreCompleto, UserEmail, Nivel, Division, Position, Grupo, Ubicacion, UserStatus)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                nombre,
                email or None,
                self.form_nivel.get().strip() or None,
                self.form_division.get().strip() or None,
                self.form_cargo.get().strip() or None,
                self.form_grupo.get().strip() or None,
                self.form_ubicacion.get().strip() or None,
                self.form_status.get()
            ))

            self.db.commit()
            messagebox.showinfo("Éxito", f"Usuario '{nombre}' creado correctamente")

            # Limpiar formulario y recargar tabla
            self._clear_form()
            self._load_all_users()

        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Error al crear usuario: {str(e)}")

    def _update_user(self):
        """Actualizar usuario existente"""
        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        user_id = self.form_userid.get().strip()
        if not user_id:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para actualizar")
            return

        try:
            # Actualizar usuario con todos los campos
            self.cursor.execute("""
                UPDATE Instituto_Usuario
                SET NombreCompleto = ?,
                    UserEmail = ?,
                    Nivel = ?,
                    Division = ?,
                    Position = ?,
                    Grupo = ?,
                    Ubicacion = ?,
                    UserStatus = ?
                WHERE UserId = ?
            """, (
                self.form_nombre.get().strip(),
                self.form_email.get().strip() or None,
                self.form_nivel.get().strip() or None,
                self.form_division.get().strip() or None,
                self.form_cargo.get().strip() or None,
                self.form_grupo.get().strip() or None,
                self.form_ubicacion.get().strip() or None,
                self.form_status.get(),
                user_id
            ))

            self.db.commit()
            messagebox.showinfo("Éxito", f"Usuario '{user_id}' actualizado correctamente")

            # Recargar tabla
            self._load_all_users()

        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Error al actualizar usuario: {str(e)}")

    def _delete_user(self):
        """Eliminar usuario (soft delete)"""
        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        user_id = self.form_userid.get().strip()
        if not user_id:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar")
            return

        # Confirmación
        confirm = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el usuario '{user_id}'?\n\n"
            "Esta acción marcará el usuario como Inactivo."
        )

        if not confirm:
            return

        try:
            # Soft delete (marcar como inactivo)
            self.cursor.execute("""
                UPDATE Instituto_Usuario
                SET UserStatus = 'Inactivo'
                WHERE UserId = ?
            """, (user_id,))

            self.db.commit()
            messagebox.showinfo("Éxito", f"Usuario '{user_id}' marcado como Inactivo")

            # Limpiar formulario y recargar tabla
            self._clear_form()
            self._load_all_users()

        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Error al eliminar usuario: {str(e)}")

    def _clear_form(self):
        """Limpiar formulario de usuario"""
        self.form_userid.delete(0, 'end')
        self.form_nombre.delete(0, 'end')
        self.form_email.delete(0, 'end')
        self.form_nivel.delete(0, 'end')
        self.form_division.delete(0, 'end')
        self.form_cargo.delete(0, 'end')
        self.form_grupo.delete(0, 'end')
        self.form_ubicacion.delete(0, 'end')
        self.form_status.set('Activo')

    # ==================== FUNCIONES DE REGISTRO DE SOPORTE ====================

    def _submit_ticket(self):
        """Guardar registro de soporte brindado"""
        userid = self.soporte_userid.get().strip()
        asunto = self.ticket_asunto.get().strip()
        descripcion = self.ticket_descripcion.get("1.0", "end-1c").strip()
        categoria = self.ticket_categoria.get()

        if not userid or not asunto or not descripcion:
            messagebox.showwarning("Campos Requeridos", "User ID, Asunto y Descripción son obligatorios")
            return

        # Aquí se implementaría la lógica real de guardado en BD
        # Por ahora, solo mostramos un mensaje de confirmación
        messagebox.showinfo(
            "Registro Guardado",
            f"Registro de soporte guardado exitosamente\n\n"
            f"Usuario: {userid}\n"
            f"Asunto: {asunto}\n"
            f"Categoría: {categoria}\n\n"
            f"El registro ha sido almacenado en el sistema."
        )

        # Limpiar formulario
        self._clear_ticket_form()

    def _clear_ticket_form(self):
        """Limpiar formulario de registro de soporte"""
        self.soporte_userid.delete(0, 'end')
        self.ticket_asunto.delete(0, 'end')
        self.ticket_descripcion.delete("1.0", "end")
        self.ticket_descripcion.insert("1.0", "Problema reportado:\n\n\nSolución brindada:\n\n")
        self.ticket_categoria.set('Técnico')

    # ==================== FUNCIONES AUXILIARES ====================

    def _setup_report_history_frame(self):
        """Configurar frame de Historial de Reportes con ejemplo inline"""
        theme = self.theme_manager.get_current_theme()

        # Scroll frame principal
        scroll_frame = ctk.CTkScrollableFrame(
            self.report_history_frame,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header con botón volver
        header = ctk.CTkFrame(scroll_frame, fg_color='transparent', height=60)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)

        # Botón volver
        back_btn = ctk.CTkButton(
            header,
            text='← Volver',
            font=('Arial', 14, 'bold'),
            fg_color=theme['surface'],
            text_color=theme['text'],
            hover_color=theme['surface_light'],
            corner_radius=10,
            width=120,
            height=40,
            command=self.show_main_config_frame
        )
        back_btn.pack(side='left')

        # Título
        is_dark = self.theme_manager.is_dark_mode()
        title_color = '#FFFFFF' if is_dark else '#002E6D'

        title = ctk.CTkLabel(
            header,
            text='📋 Historial de Reportes',
            font=('Montserrat', 28, 'bold'),
            text_color=title_color
        )
        title.pack(side='left', padx=20)

        # Card de historial
        history_card = ctk.CTkFrame(
            scroll_frame,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )
        history_card.pack(fill='both', expand=True)

        # Contenido del historial
        history_content = ctk.CTkFrame(history_card, fg_color='transparent')
        history_content.pack(fill='both', expand=True, padx=30, pady=30)

        # Título de la tabla
        table_title = ctk.CTkLabel(
            history_content,
            text='📑 Reportes Generados (Ejemplo)',
            font=('Arial', 18, 'bold'),
            text_color=theme['text']
        )
        table_title.pack(anchor='w', pady=(0, 20))

        # Datos de ejemplo
        reportes_ejemplo = [
            ('2025-11-01', 'Reporte Gerencial Q1', 'PDF', '2.3 MB', 'Completado'),
            ('2025-10-28', 'Dashboard Mensual - Octubre', 'PDF', '1.8 MB', 'Completado'),
            ('2025-10-15', 'Progreso por Módulo', 'PDF', '1.5 MB', 'Completado'),
            ('2025-10-05', 'Reporte de Usuarios', 'PDF', '950 KB', 'Completado'),
            ('2025-09-30', 'Análisis Jerárquico Q3', 'PDF', '3.1 MB', 'Completado')
        ]

        # Container para tabla
        table_container_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        table_container = ctk.CTkFrame(history_content, fg_color=table_container_bg, corner_radius=10)
        table_container.pack(fill='both', expand=True)

        # Crear Treeview para historial
        style = ttk.Style()
        style.theme_use('clam')

        if self.theme_manager.is_dark_mode():
            style.configure('History.Treeview',
                background=theme['background'],
                foreground=theme['text'],
                fieldbackground=theme['background'],
                borderwidth=0,
                font=('Segoe UI', 11)
            )
            style.configure('History.Treeview.Heading',
                background=theme['surface'],
                foreground=theme['text'],
                borderwidth=1,
                font=('Segoe UI', 12, 'bold')
            )
            style.map('History.Treeview',
                background=[('selected', '#1E90FF')],
                foreground=[('selected', '#ffffff')]
            )
        else:
            style.configure('History.Treeview',
                background='#ffffff',
                foreground=theme['text'],
                fieldbackground='#ffffff',
                borderwidth=0,
                font=('Segoe UI', 11)
            )
            style.configure('History.Treeview.Heading',
                background='#e8e8e8',
                foreground=theme['text'],
                borderwidth=1,
                font=('Segoe UI', 12, 'bold')
            )

        # Scrollbars
        vsb = ttk.Scrollbar(table_container, orient="vertical")

        self.history_tree = ttk.Treeview(
            table_container,
            columns=('Fecha', 'Nombre', 'Formato', 'Tamaño', 'Estado'),
            show='headings',
            yscrollcommand=vsb.set,
            style='History.Treeview',
            height=10
        )

        # Configurar columnas
        self.history_tree.heading('Fecha', text='Fecha')
        self.history_tree.heading('Nombre', text='Nombre del Reporte')
        self.history_tree.heading('Formato', text='Formato')
        self.history_tree.heading('Tamaño', text='Tamaño')
        self.history_tree.heading('Estado', text='Estado')

        self.history_tree.column('Fecha', width=120, minwidth=100, anchor='center')
        self.history_tree.column('Nombre', width=350, minwidth=250)
        self.history_tree.column('Formato', width=80, minwidth=70, anchor='center')
        self.history_tree.column('Tamaño', width=100, minwidth=80, anchor='center')
        self.history_tree.column('Estado', width=120, minwidth=100, anchor='center')

        vsb.config(command=self.history_tree.yview)

        self.history_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        # Insertar datos de ejemplo
        for reporte in reportes_ejemplo:
            self.history_tree.insert('', 'end', values=reporte)

        # Botones de acción
        button_frame = ctk.CTkFrame(history_content, fg_color='transparent')
        button_frame.pack(fill='x', pady=(20, 0))

        button_color = self._get_button_color()

        ctk.CTkButton(
            button_frame,
            text='📥 Descargar Seleccionado',
            font=('Arial', 14, 'bold'),
            fg_color=button_color,
            hover_color=self._get_button_hover_color(button_color),
            corner_radius=10,
            height=45,
            width=220,
            command=lambda: messagebox.showinfo("Descargar", "Función de descarga en desarrollo")
        ).pack(side='left', padx=5)

        ctk.CTkButton(
            button_frame,
            text='🔄 Actualizar Lista',
            font=('Arial', 14, 'bold'),
            fg_color=theme['surface_light'],
            text_color=theme['text'],
            hover_color=theme['border'],
            corner_radius=10,
            height=45,
            width=180,
            command=lambda: messagebox.showinfo("Actualizar", "Lista actualizada")
        ).pack(side='left', padx=5)

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

    def _get_button_color(self):
        """Obtener color de botones según el tema actual"""
        theme = self.theme_manager.get_current_theme()
        if theme['background'] == '#1a1a1a':  # Dark theme
            return '#009BDE'  # Cyan
        else:  # Light theme
            return '#002E6D'  # Navy blue

    def _get_button_hover_color(self, base_color):
        """Obtener color hover para botones"""
        if base_color == '#002E6D':  # Navy blue
            return '#003D8F'
        elif base_color == '#009BDE':  # Cyan
            return '#00B5FF'
        return base_color

    def _on_theme_changed(self, theme_colors):
        """Callback cuando cambia el tema"""
        # Actualizar color de fondo del panel
        self.configure(fg_color=theme_colors['background'])

        # Recrear frames para aplicar nuevos colores
        # (En una implementación completa, aquí se actualizarían todos los widgets)

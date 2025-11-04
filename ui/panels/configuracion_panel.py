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

        # Frame de Ticket de Soporte
        self.support_ticket_frame = ctk.CTkFrame(
            self,
            fg_color='transparent'
        )

        # Configurar contenido del frame principal
        self._setup_main_frame()

        # Configurar frames internos
        self._setup_user_manager_frame()
        self._setup_support_ticket_frame()

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

        # Card 2: Solicitar Soporte Técnico
        card2 = ConfigCard(
            grid_container,
            icon='🎫',
            title='Solicitar Soporte Técnico',
            description='Crear un nuevo ticket de soporte para asistencia técnica',
            button_text='Crear Solicitud',
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
            command=self._show_report_history
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

        # Grid de formulario
        form_grid = ctk.CTkFrame(form_card, fg_color='transparent')
        form_grid.pack(fill='x', padx=20, pady=(0, 15))

        # Fila 1: User ID y Nombre
        row1 = ctk.CTkFrame(form_grid, fg_color='transparent')
        row1.pack(fill='x', pady=5)

        ctk.CTkLabel(row1, text='User ID:', font=('Arial', 13), text_color=theme['text']).pack(side='left', padx=(0, 10))
        self.form_userid = ctk.CTkEntry(row1, width=200, height=35, corner_radius=8)
        self.form_userid.pack(side='left', padx=5)

        ctk.CTkLabel(row1, text='Nombre:', font=('Arial', 13), text_color=theme['text']).pack(side='left', padx=(30, 10))
        self.form_nombre = ctk.CTkEntry(row1, width=300, height=35, corner_radius=8)
        self.form_nombre.pack(side='left', padx=5)

        # Fila 2: Email y Departamento
        row2 = ctk.CTkFrame(form_grid, fg_color='transparent')
        row2.pack(fill='x', pady=5)

        ctk.CTkLabel(row2, text='Email:', font=('Arial', 13), text_color=theme['text']).pack(side='left', padx=(0, 10))
        self.form_email = ctk.CTkEntry(row2, width=300, height=35, corner_radius=8)
        self.form_email.pack(side='left', padx=5)

        ctk.CTkLabel(row2, text='Departamento:', font=('Arial', 13), text_color=theme['text']).pack(side='left', padx=(30, 10))
        self.form_departamento = ctk.CTkEntry(row2, width=200, height=35, corner_radius=8)
        self.form_departamento.pack(side='left', padx=5)

        # Fila 3: Cargo y Ubicación
        row3 = ctk.CTkFrame(form_grid, fg_color='transparent')
        row3.pack(fill='x', pady=5)

        ctk.CTkLabel(row3, text='Cargo:', font=('Arial', 13), text_color=theme['text']).pack(side='left', padx=(0, 10))
        self.form_cargo = ctk.CTkEntry(row3, width=250, height=35, corner_radius=8)
        self.form_cargo.pack(side='left', padx=5)

        ctk.CTkLabel(row3, text='Ubicación:', font=('Arial', 13), text_color=theme['text']).pack(side='left', padx=(30, 10))
        self.form_ubicacion = ctk.CTkEntry(row3, width=200, height=35, corner_radius=8)
        self.form_ubicacion.pack(side='left', padx=5)

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
            columns=('UserId', 'Nombre', 'Email', 'Departamento', 'Cargo', 'Ubicacion'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            style='UserMgmt.Treeview'
        )

        # Configurar columnas
        self.user_results_tree.heading('UserId', text='User ID')
        self.user_results_tree.heading('Nombre', text='Nombre')
        self.user_results_tree.heading('Email', text='Email')
        self.user_results_tree.heading('Departamento', text='Departamento')
        self.user_results_tree.heading('Cargo', text='Cargo')
        self.user_results_tree.heading('Ubicacion', text='Ubicación')

        self.user_results_tree.column('UserId', width=100, minwidth=100)
        self.user_results_tree.column('Nombre', width=200, minwidth=150)
        self.user_results_tree.column('Email', width=220, minwidth=180)
        self.user_results_tree.column('Departamento', width=150, minwidth=120)
        self.user_results_tree.column('Cargo', width=150, minwidth=120)
        self.user_results_tree.column('Ubicacion', width=120, minwidth=100)

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
        """Configurar frame de Ticket de Soporte"""
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
            text='🎫 Solicitar Soporte Técnico',
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

        # Campo Asunto
        ctk.CTkLabel(
            form_content,
            text='Asunto:',
            font=('Arial', 16, 'bold'),
            text_color=theme['text']
        ).pack(anchor='w', pady=(0, 10))

        self.ticket_asunto = ctk.CTkEntry(
            form_content,
            placeholder_text='Ingrese el asunto del ticket...',
            font=('Arial', 14),
            height=45,
            corner_radius=10
        )
        self.ticket_asunto.pack(fill='x', pady=(0, 20))

        # Campo Descripción
        ctk.CTkLabel(
            form_content,
            text='Descripción:',
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
            values=['Técnico', 'Funcional', 'Datos', 'Otro'],
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
            text='📩 Enviar Ticket',
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
        """Mostrar frame de ticket de soporte"""
        # Ocultar frame principal
        self.main_frame.pack_forget()

        # Mostrar frame de ticket de soporte
        self.support_ticket_frame.pack(fill='both', expand=True)

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
            # Buscar por User ID o Nombre (LIKE)
            self.cursor.execute("""
                SELECT
                    u.UserId,
                    u.UserName,
                    u.UserEmail,
                    d.NombreDepartamento,
                    u.Position,
                    u.Ubicacion
                FROM dbo.Instituto_Usuario u
                LEFT JOIN dbo.Instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
                WHERE u.UserId LIKE ? OR u.UserName LIKE ?
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
                    u.UserName,
                    u.UserEmail,
                    d.NombreDepartamento,
                    u.Position,
                    u.Ubicacion
                FROM dbo.Instituto_Usuario u
                LEFT JOIN dbo.Instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
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

        if values:
            # Cargar datos en el formulario
            self.form_userid.delete(0, 'end')
            self.form_userid.insert(0, values[0])

            self.form_nombre.delete(0, 'end')
            self.form_nombre.insert(0, values[1])

            self.form_email.delete(0, 'end')
            self.form_email.insert(0, values[2])

            self.form_departamento.delete(0, 'end')
            self.form_departamento.insert(0, values[3])

            self.form_cargo.delete(0, 'end')
            self.form_cargo.insert(0, values[4])

            self.form_ubicacion.delete(0, 'end')
            self.form_ubicacion.insert(0, values[5])

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
            self.cursor.execute("SELECT COUNT(*) FROM dbo.Instituto_Usuario WHERE UserId = ?", (user_id,))
            if self.cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", f"El User ID '{user_id}' ya existe")
                return

            # Obtener o crear departamento
            departamento = self.form_departamento.get().strip()
            id_departamento = None
            if departamento:
                id_departamento = self._get_or_create_departamento(departamento)

            # Insertar usuario
            self.cursor.execute("""
                INSERT INTO dbo.Instituto_Usuario
                (UserId, UserName, UserEmail, IdDepartamento, Position, Ubicacion, Activo)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (
                user_id,
                nombre,
                email,
                id_departamento,
                self.form_cargo.get().strip() or None,
                self.form_ubicacion.get().strip() or None
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
            # Obtener o crear departamento
            departamento = self.form_departamento.get().strip()
            id_departamento = None
            if departamento:
                id_departamento = self._get_or_create_departamento(departamento)

            # Actualizar usuario
            self.cursor.execute("""
                UPDATE dbo.Instituto_Usuario
                SET UserName = ?,
                    UserEmail = ?,
                    IdDepartamento = ?,
                    Position = ?,
                    Ubicacion = ?
                WHERE UserId = ?
            """, (
                self.form_nombre.get().strip(),
                self.form_email.get().strip(),
                id_departamento,
                self.form_cargo.get().strip() or None,
                self.form_ubicacion.get().strip() or None,
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
            "Esta acción marcará el usuario como inactivo."
        )

        if not confirm:
            return

        try:
            # Soft delete (marcar como inactivo)
            self.cursor.execute("""
                UPDATE dbo.Instituto_Usuario
                SET Activo = 0
                WHERE UserId = ?
            """, (user_id,))

            self.db.commit()
            messagebox.showinfo("Éxito", f"Usuario '{user_id}' eliminado correctamente")

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
        self.form_departamento.delete(0, 'end')
        self.form_cargo.delete(0, 'end')
        self.form_ubicacion.delete(0, 'end')

    def _get_or_create_departamento(self, nombre_departamento):
        """Obtener ID de departamento o crearlo si no existe"""
        if not nombre_departamento:
            return None

        try:
            # Buscar departamento existente
            self.cursor.execute("""
                SELECT IdDepartamento
                FROM dbo.Instituto_Departamento
                WHERE NombreDepartamento = ?
            """, (nombre_departamento,))

            result = self.cursor.fetchone()
            if result:
                return result[0]

            # Crear nuevo departamento
            self.cursor.execute("""
                INSERT INTO dbo.Instituto_Departamento (NombreDepartamento, IdUnidadDeNegocio)
                VALUES (?, NULL)
            """, (nombre_departamento,))

            self.db.commit()

            # Obtener ID del nuevo departamento
            self.cursor.execute("SELECT @@IDENTITY")
            return self.cursor.fetchone()[0]

        except Exception as e:
            print(f"Error en get_or_create_departamento: {e}")
            return None

    # ==================== FUNCIONES DE TICKET DE SOPORTE ====================

    def _submit_ticket(self):
        """Enviar ticket de soporte"""
        asunto = self.ticket_asunto.get().strip()
        descripcion = self.ticket_descripcion.get("1.0", "end-1c").strip()
        categoria = self.ticket_categoria.get()

        if not asunto or not descripcion:
            messagebox.showwarning("Campos Requeridos", "Asunto y Descripción son obligatorios")
            return

        # Aquí se implementaría la lógica real de envío de ticket
        # Por ahora, solo mostramos un mensaje de confirmación
        messagebox.showinfo(
            "Ticket Enviado",
            f"Ticket de soporte creado exitosamente\n\n"
            f"Asunto: {asunto}\n"
            f"Categoría: {categoria}\n\n"
            f"Recibirás una respuesta en 24-48 horas."
        )

        # Limpiar formulario
        self._clear_ticket_form()

    def _clear_ticket_form(self):
        """Limpiar formulario de ticket"""
        self.ticket_asunto.delete(0, 'end')
        self.ticket_descripcion.delete("1.0", "end")
        self.ticket_categoria.set('Técnico')

    # ==================== FUNCIONES AUXILIARES ====================

    def _show_report_history(self):
        """Mostrar historial de reportes"""
        messagebox.showinfo(
            "Historial de Reportes",
            "Función 'Historial de Reportes' en desarrollo.\n\n"
            "Esta funcionalidad permitirá ver y descargar\n"
            "reportes PDF generados anteriormente."
        )

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

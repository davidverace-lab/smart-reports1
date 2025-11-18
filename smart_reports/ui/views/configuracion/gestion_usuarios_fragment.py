"""
GestionUsuariosFragment - Fragment para gestión completa de usuarios (CRUD)
Separado según arquitectura Android Studio
"""
import customtkinter as ctk
from tkinter import messagebox
import tkinter.ttk as ttk
from src.main.res.config.gestor_temas import get_theme_manager


class GestionUsuariosFragment(ctk.CTkFrame):
    """Fragment de Gestión de Usuarios con CRUD completo"""

    def __init__(self, parent, db_connection=None, on_back=None, **kwargs):
        """
        Args:
            parent: Widget padre
            db_connection: Conexión a la base de datos
            on_back: Callback para volver al menú principal
        """
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.db = db_connection
        self.cursor = db_connection.cursor() if db_connection else None
        self.on_back = on_back
        self.theme_manager = get_theme_manager()

        # Crear interfaz
        self._create_interface()

        # Registrar callback para cambios de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    def _create_interface(self):
        """Crear interfaz completa del fragment"""
        theme = self.theme_manager.get_current_theme()

        # Scroll frame principal
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header con botón volver
        self._create_header(scroll_frame, theme)

        # Card de búsqueda
        self._create_search_card(scroll_frame, theme)

        # Card de formulario CRUD
        self._create_form_card(scroll_frame, theme)

        # Card de resultados
        self._create_results_card(scroll_frame, theme)

        # Card de historial de soportes
        self._create_support_history_card(scroll_frame, theme)

    def _create_header(self, parent, theme):
        """Crear header con título y botón volver"""
        header = ctk.CTkFrame(parent, fg_color='transparent', height=60)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)

        # Botón volver
        back_btn = ctk.CTkButton(
            header,
            text='← Volver',
            font=('Montserrat', 14, 'bold'),
            fg_color=theme['surface'],
            text_color=theme['text'],
            hover_color=theme['surface_light'],
            corner_radius=10,
            width=120,
            height=40,
            command=self.on_back if self.on_back else None
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

    def _create_search_card(self, parent, theme):
        """Card de búsqueda de usuarios"""
        search_card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )
        search_card.pack(fill='x', pady=(0, 15))

        search_header = ctk.CTkLabel(
            search_card,
            text='🔍 Buscar Usuario',
            font=('Montserrat', 18, 'bold'),
            text_color=theme['text']
        )
        search_header.pack(padx=20, pady=(15, 10), anchor='w')

        # Frame de búsqueda
        search_frame = ctk.CTkFrame(search_card, fg_color='transparent')
        search_frame.pack(fill='x', padx=20, pady=(0, 15))

        ctk.CTkLabel(
            search_frame,
            text='User ID o Nombre:',
            font=('Montserrat', 14),
            text_color=theme['text']
        ).pack(side='left', padx=(0, 10))

        self.user_search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text='Ingrese User ID o Nombre...',
            font=('Montserrat', 14),
            width=300,
            height=40,
            corner_radius=10
        )
        self.user_search_entry.pack(side='left', padx=5)
        self.user_search_entry.bind('<Return>', lambda e: self._search_user())

        button_color = self._get_button_color()
        search_btn = ctk.CTkButton(
            search_frame,
            text='Buscar',
            font=('Montserrat', 14, 'bold'),
            fg_color=button_color,
            hover_color=self._get_button_hover_color(button_color),
            corner_radius=10,
            height=40,
            width=120,
            command=self._search_user
        )
        search_btn.pack(side='left', padx=10)

    def _create_form_card(self, parent, theme):
        """Card de formulario de edición/creación"""
        form_card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )
        form_card.pack(fill='x', pady=(0, 15))

        form_header = ctk.CTkLabel(
            form_card,
            text='✏️ Formulario de Usuario',
            font=('Montserrat', 18, 'bold'),
            text_color=theme['text']
        )
        form_header.pack(padx=20, pady=(15, 10), anchor='w')

        # Grid de formulario (2 columnas)
        form_grid = ctk.CTkFrame(form_card, fg_color='transparent')
        form_grid.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        form_grid.grid_columnconfigure((0, 1), weight=1)

        # Row 0: User ID y Nombre Completo
        ctk.CTkLabel(form_grid, text='User ID:', font=('Montserrat', 12, 'bold'), text_color=theme['text']).grid(row=0, column=0, sticky='w', padx=(0, 5), pady=5)
        self.form_userid = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='E12345')
        self.form_userid.grid(row=0, column=0, sticky='ew', padx=(100, 10), pady=5)

        ctk.CTkLabel(form_grid, text='Nombre Completo:', font=('Montserrat', 12, 'bold'), text_color=theme['text']).grid(row=0, column=1, sticky='w', padx=(0, 5), pady=5)
        self.form_nombre = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='Juan Pérez')
        self.form_nombre.grid(row=0, column=1, sticky='ew', padx=(150, 10), pady=5)

        # Row 1: Email y Nivel
        ctk.CTkLabel(form_grid, text='Email:', font=('Montserrat', 12, 'bold'), text_color=theme['text']).grid(row=1, column=0, sticky='w', padx=(0, 5), pady=5)
        self.form_email = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='usuario@empresa.com')
        self.form_email.grid(row=1, column=0, sticky='ew', padx=(100, 10), pady=5)

        ctk.CTkLabel(form_grid, text='Nivel:', font=('Montserrat', 12, 'bold'), text_color=theme['text']).grid(row=1, column=1, sticky='w', padx=(0, 5), pady=5)
        self.form_nivel = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='L1, L2, L3...')
        self.form_nivel.grid(row=1, column=1, sticky='ew', padx=(150, 10), pady=5)

        # Row 2: División y Posición
        ctk.CTkLabel(form_grid, text='División:', font=('Montserrat', 12, 'bold'), text_color=theme['text']).grid(row=2, column=0, sticky='w', padx=(0, 5), pady=5)
        self.form_division = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='Operaciones')
        self.form_division.grid(row=2, column=0, sticky='ew', padx=(100, 10), pady=5)

        ctk.CTkLabel(form_grid, text='Posición:', font=('Montserrat', 12, 'bold'), text_color=theme['text']).grid(row=2, column=1, sticky='w', padx=(0, 5), pady=5)
        self.form_cargo = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='Gerente')
        self.form_cargo.grid(row=2, column=1, sticky='ew', padx=(150, 10), pady=5)

        # Row 3: Grupo y Ubicación
        ctk.CTkLabel(form_grid, text='Grupo:', font=('Montserrat', 12, 'bold'), text_color=theme['text']).grid(row=3, column=0, sticky='w', padx=(0, 5), pady=5)
        self.form_grupo = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='Admin')
        self.form_grupo.grid(row=3, column=0, sticky='ew', padx=(100, 10), pady=5)

        ctk.CTkLabel(form_grid, text='Ubicación:', font=('Montserrat', 12, 'bold'), text_color=theme['text']).grid(row=3, column=1, sticky='w', padx=(0, 5), pady=5)
        self.form_ubicacion = ctk.CTkEntry(form_grid, height=35, corner_radius=8, placeholder_text='México')
        self.form_ubicacion.grid(row=3, column=1, sticky='ew', padx=(150, 10), pady=5)

        # Row 4: UserStatus
        ctk.CTkLabel(form_grid, text='Estado:', font=('Montserrat', 12, 'bold'), text_color=theme['text']).grid(row=4, column=0, sticky='w', padx=(0, 5), pady=5)
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
            font=('Montserrat', 14, 'bold'),
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
            font=('Montserrat', 14, 'bold'),
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
            font=('Montserrat', 14, 'bold'),
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
            font=('Montserrat', 14, 'bold'),
            fg_color=theme['surface_light'],
            text_color=theme['text'],
            hover_color=theme['border'],
            corner_radius=10,
            height=45,
            width=180,
            command=self._clear_form
        ).pack(side='left', padx=5)

    def _create_results_card(self, parent, theme):
        """Card de resultados con tabla"""
        results_card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )
        results_card.pack(fill='both', expand=True, pady=(0, 15))

        results_header = ctk.CTkLabel(
            results_card,
            text='📋 Resultados de Búsqueda',
            font=('Montserrat', 18, 'bold'),
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
                font=('Montserrat', 10)
            )
            style.configure('UserMgmt.Treeview.Heading',
                background=theme['surface'],
                foreground=theme['text'],
                borderwidth=1,
                font=('Montserrat', 11, 'bold')
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
                font=('Montserrat', 10)
            )
            style.configure('UserMgmt.Treeview.Heading',
                background='#e8e8e8',
                foreground=theme['text'],
                borderwidth=1,
                font=('Montserrat', 11, 'bold')
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

    def _create_support_history_card(self, parent, theme):
        """Card de historial de soportes del usuario"""
        support_history_card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )
        support_history_card.pack(fill='both', expand=True, pady=(0, 15))

        support_history_header = ctk.CTkLabel(
            support_history_card,
            text='📋 Historial de Soportes',
            font=('Montserrat', 18, 'bold'),
            text_color=theme['text']
        )
        support_history_header.pack(padx=20, pady=(15, 10), anchor='w')

        # Container para tabla de soportes
        table_container_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        support_table_container = ctk.CTkFrame(support_history_card, fg_color=table_container_bg, corner_radius=10)
        support_table_container.pack(fill='both', expand=True, padx=20, pady=(10, 20))

        # Scrollbars para tabla de soportes
        support_vsb = ttk.Scrollbar(support_table_container, orient="vertical")
        support_hsb = ttk.Scrollbar(support_table_container, orient="horizontal")

        self.support_history_tree = ttk.Treeview(
            support_table_container,
            columns=('Fecha', 'Asunto', 'Categoria', 'Descripcion'),
            show='headings',
            yscrollcommand=support_vsb.set,
            xscrollcommand=support_hsb.set,
            style='UserMgmt.Treeview',
            height=6
        )

        # Configurar columnas
        self.support_history_tree.heading('Fecha', text='Fecha')
        self.support_history_tree.heading('Asunto', text='Asunto')
        self.support_history_tree.heading('Categoria', text='Categoría')
        self.support_history_tree.heading('Descripcion', text='Descripción')

        self.support_history_tree.column('Fecha', width=140, minwidth=120)
        self.support_history_tree.column('Asunto', width=250, minwidth=200)
        self.support_history_tree.column('Categoria', width=120, minwidth=100)
        self.support_history_tree.column('Descripcion', width=400, minwidth=300)

        support_vsb.config(command=self.support_history_tree.yview)
        support_hsb.config(command=self.support_history_tree.xview)

        self.support_history_tree.grid(row=0, column=0, sticky='nsew')
        support_vsb.grid(row=0, column=1, sticky='ns')
        support_hsb.grid(row=1, column=0, sticky='ew')

        support_table_container.grid_rowconfigure(0, weight=1)
        support_table_container.grid_columnconfigure(0, weight=1)

    # ==================== LÓGICA DE NEGOCIO ====================

    def _search_user(self):
        """Buscar usuario por ID o nombre"""
        search_term = self.user_search_entry.get().strip()

        if not search_term:
            # Si está vacío, cargar todos los usuarios
            self._load_all_users()
            return

        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            # Buscar por UserId o Nombre
            if search_term.upper().startswith('E'):
                # Buscar por UserId
                query = """
                    SELECT UserId, FullName, EmailAddress, LevelName,
                           Division, JobTitle, GroupName, Location, UserStatus
                    FROM users
                    WHERE UserId LIKE ?
                """
                self.cursor.execute(query, (f'%{search_term}%',))
            else:
                # Buscar por nombre
                query = """
                    SELECT UserId, FullName, EmailAddress, LevelName,
                           Division, JobTitle, GroupName, Location, UserStatus
                    FROM users
                    WHERE FullName LIKE ?
                """
                self.cursor.execute(query, (f'%{search_term}%',))

            results = self.cursor.fetchall()

            if results:
                self._display_user_results(results)
                messagebox.showinfo("Búsqueda Exitosa", f"Se encontraron {len(results)} usuario(s)")
            else:
                # Limpiar tabla
                self.user_results_tree.delete(*self.user_results_tree.get_children())
                messagebox.showinfo("Sin Resultados", f"No se encontraron usuarios con: {search_term}")

        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda:\n{str(e)}")

    def _load_all_users(self):
        """Cargar todos los usuarios activos"""
        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            query = """
                SELECT UserId, FullName, EmailAddress, LevelName,
                       Division, JobTitle, GroupName, Location, UserStatus
                FROM users
                ORDER BY FullName
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if results:
                self._display_user_results(results)
            else:
                messagebox.showinfo("Sin Datos", "No hay usuarios registrados")

        except Exception as e:
            messagebox.showerror("Error", f"Error cargando usuarios:\n{str(e)}")

    def _display_user_results(self, results):
        """Mostrar resultados en la tabla"""
        # Limpiar tabla
        self.user_results_tree.delete(*self.user_results_tree.get_children())

        # Insertar resultados
        for row in results:
            self.user_results_tree.insert('', 'end', values=row)

    def _on_user_select(self, event):
        """Cargar usuario seleccionado en el formulario"""
        selection = self.user_results_tree.selection()
        if not selection:
            return

        # Obtener datos del usuario seleccionado
        item = self.user_results_tree.item(selection[0])
        values = item['values']

        # Cargar en formulario
        self.form_userid.delete(0, 'end')
        self.form_userid.insert(0, values[0])

        self.form_nombre.delete(0, 'end')
        self.form_nombre.insert(0, values[1])

        self.form_email.delete(0, 'end')
        self.form_email.insert(0, values[2])

        self.form_nivel.delete(0, 'end')
        self.form_nivel.insert(0, values[3] if values[3] else '')

        self.form_division.delete(0, 'end')
        self.form_division.insert(0, values[4] if values[4] else '')

        self.form_cargo.delete(0, 'end')
        self.form_cargo.insert(0, values[5] if values[5] else '')

        self.form_grupo.delete(0, 'end')
        self.form_grupo.insert(0, values[6] if values[6] else '')

        self.form_ubicacion.delete(0, 'end')
        self.form_ubicacion.insert(0, values[7] if values[7] else '')

        self.form_status.set(values[8] if values[8] else 'Activo')

        # Cargar historial de soportes
        self._load_user_support_history(values[0])

    def _load_user_support_history(self, userid):
        """Cargar historial de soportes del usuario"""
        if not self.cursor:
            return

        try:
            # Limpiar tabla
            self.support_history_tree.delete(*self.support_history_tree.get_children())

            query = """
                SELECT SupportDate, Subject, Category, Description
                FROM support_history
                WHERE UserId = ?
                ORDER BY SupportDate DESC
            """
            self.cursor.execute(query, (userid,))
            results = self.cursor.fetchall()

            # Insertar resultados
            for row in results:
                # Truncar descripción si es muy larga
                desc = row[3][:100] + '...' if len(row[3]) > 100 else row[3]
                self.support_history_tree.insert('', 'end', values=(row[0], row[1], row[2], desc))

        except Exception as e:
            print(f"Error cargando historial de soportes: {str(e)}")

    def _create_user(self):
        """Crear nuevo usuario"""
        if not self.cursor or not self.db:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        # Validar campos requeridos
        userid = self.form_userid.get().strip()
        nombre = self.form_nombre.get().strip()
        email = self.form_email.get().strip()

        if not userid or not nombre or not email:
            messagebox.showwarning("Advertencia", "User ID, Nombre y Email son obligatorios")
            return

        try:
            # Verificar si ya existe
            self.cursor.execute("SELECT UserId FROM users WHERE UserId = ?", (userid,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", f"El usuario {userid} ya existe")
                return

            # Insertar usuario
            query = """
                INSERT INTO users (UserId, FullName, EmailAddress, LevelName,
                                   Division, JobTitle, GroupName, Location, UserStatus)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (
                userid,
                nombre,
                email,
                self.form_nivel.get().strip() or None,
                self.form_division.get().strip() or None,
                self.form_cargo.get().strip() or None,
                self.form_grupo.get().strip() or None,
                self.form_ubicacion.get().strip() or None,
                self.form_status.get()
            ))

            self.db.commit()
            messagebox.showinfo("Éxito", f"Usuario {userid} creado correctamente")

            # Limpiar formulario y recargar
            self._clear_form()
            self._load_all_users()

        except Exception as e:
            messagebox.showerror("Error", f"Error creando usuario:\n{str(e)}")

    def _update_user(self):
        """Actualizar usuario existente"""
        if not self.cursor or not self.db:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        userid = self.form_userid.get().strip()
        if not userid:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para actualizar")
            return

        try:
            query = """
                UPDATE users
                SET FullName = ?, EmailAddress = ?, LevelName = ?,
                    Division = ?, JobTitle = ?, GroupName = ?,
                    Location = ?, UserStatus = ?
                WHERE UserId = ?
            """
            self.cursor.execute(query, (
                self.form_nombre.get().strip(),
                self.form_email.get().strip(),
                self.form_nivel.get().strip() or None,
                self.form_division.get().strip() or None,
                self.form_cargo.get().strip() or None,
                self.form_grupo.get().strip() or None,
                self.form_ubicacion.get().strip() or None,
                self.form_status.get(),
                userid
            ))

            self.db.commit()
            messagebox.showinfo("Éxito", f"Usuario {userid} actualizado correctamente")

            # Recargar resultados
            self._load_all_users()

        except Exception as e:
            messagebox.showerror("Error", f"Error actualizando usuario:\n{str(e)}")

    def _delete_user(self):
        """Eliminar usuario"""
        if not self.cursor or not self.db:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        userid = self.form_userid.get().strip()
        if not userid:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar")
            return

        # Confirmar eliminación
        confirm = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el usuario {userid}?\n\nEsta acción no se puede deshacer."
        )

        if not confirm:
            return

        try:
            self.cursor.execute("DELETE FROM users WHERE UserId = ?", (userid,))
            self.db.commit()
            messagebox.showinfo("Éxito", f"Usuario {userid} eliminado correctamente")

            # Limpiar formulario y recargar
            self._clear_form()
            self._load_all_users()

        except Exception as e:
            messagebox.showerror("Error", f"Error eliminando usuario:\n{str(e)}")

    def _clear_form(self):
        """Limpiar formulario"""
        self.form_userid.delete(0, 'end')
        self.form_nombre.delete(0, 'end')
        self.form_email.delete(0, 'end')
        self.form_nivel.delete(0, 'end')
        self.form_division.delete(0, 'end')
        self.form_cargo.delete(0, 'end')
        self.form_grupo.delete(0, 'end')
        self.form_ubicacion.delete(0, 'end')
        self.form_status.set('Activo')

        # Limpiar historial de soportes
        self.support_history_tree.delete(*self.support_history_tree.get_children())

    # ==================== UTILIDADES ====================

    def _get_button_color(self):
        """Obtener color de botón según tema"""
        is_dark = self.theme_manager.is_dark_mode()
        return '#6c63ff' if is_dark else '#002E6D'

    def _get_button_hover_color(self, base_color):
        """Obtener color hover"""
        if base_color == '#6c63ff':
            return '#5a52d5'
        elif base_color == '#002E6D':
            return '#00509E'
        return base_color

    def _on_theme_changed(self, theme_colors):
        """Callback para cambios de tema"""
        # Recargar interfaz con nuevo tema
        # (Aquí podrías actualizar colores dinámicamente si es necesario)
        pass

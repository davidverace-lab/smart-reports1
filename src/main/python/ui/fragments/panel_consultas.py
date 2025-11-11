"""
PanelConsultas - Panel completo de consultas a la base de datos
Separado para mejor organización (Android Studio style)
"""
import customtkinter as ctk
from tkinter import messagebox, ttk
from src.main.res.config.themes import HUTCHISON_COLORS
from src.main.res.config.gestor_temas import get_theme_manager
from src.main.python.viewmodels.database_query_controller import DatabaseQueryController


class PanelConsultas(ctk.CTkFrame):
    """
    Panel de Consultas - Búsquedas y filtros en la base de datos

    Funcionalidades:
    - Buscar usuario por ID
    - Consultar usuarios por unidad de negocio
    - Consultar usuarios nuevos
    - Visualización de resultados en tabla
    """

    def __init__(self, parent, db_connection, cursor, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection
        self.cursor = cursor

        # ViewModel para lógica de consultas
        self.db_controller = DatabaseQueryController(db_connection, cursor)

        # Variables
        self.current_results = []
        self.current_columns = []

        # Crear UI
        self._create_interface()

    def _create_interface(self):
        """Crear interfaz completa del panel"""
        theme = self.theme_manager.get_current_theme()

        # Container con scroll
        main_container = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # === HEADER ===
        self._create_header(main_container, theme)

        # === SECCIÓN 1: BÚSQUEDA POR ID ===
        self._create_search_by_id_section(main_container, theme)

        # === SECCIÓN 2: BÚSQUEDA POR UNIDAD ===
        self._create_search_by_unit_section(main_container, theme)

        # === SECCIÓN 3: USUARIOS NUEVOS ===
        self._create_new_users_section(main_container, theme)

        # === SECCIÓN 4: ESTADÍSTICAS GLOBALES ===
        self._create_stats_section(main_container, theme)

        # === RESULTADOS ===
        self._create_results_section(main_container, theme)

    def _create_header(self, parent, theme):
        """Crear header del panel"""
        header_frame = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=2,
            border_color=HUTCHISON_COLORS['aqua_green']
        )
        header_frame.pack(fill='x', pady=(0, 20))

        header_content = ctk.CTkFrame(header_frame, fg_color='transparent')
        header_content.pack(fill='x', padx=30, pady=20)

        # Título
        ctk.CTkLabel(
            header_content,
            text="🔍 Panel de Consultas",
            font=('Montserrat', 28, 'bold'),
            text_color=HUTCHISON_COLORS['aqua_green']
        ).pack(anchor='w', pady=(0, 5))

        # Subtítulo
        ctk.CTkLabel(
            header_content,
            text="Búsquedas y filtros en la base de datos de capacitación",
            font=('Montserrat', 14),
            text_color=theme['text_secondary']
        ).pack(anchor='w')

    def _create_search_by_id_section(self, parent, theme):
        """Sección: Buscar usuario por ID"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=12
        )
        section_frame.pack(fill='x', pady=(0, 15))

        content = ctk.CTkFrame(section_frame, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=20)

        # Título de sección
        ctk.CTkLabel(
            content,
            text="👤 Buscar Usuario por ID",
            font=('Montserrat', 18, 'bold'),
            text_color=theme['text']
        ).pack(anchor='w', pady=(0, 15))

        # Input frame
        input_frame = ctk.CTkFrame(content, fg_color='transparent')
        input_frame.pack(fill='x')
        input_frame.grid_columnconfigure(1, weight=1)

        # Label
        ctk.CTkLabel(
            input_frame,
            text="ID Usuario:",
            font=('Montserrat', 13),
            text_color=theme['text']
        ).grid(row=0, column=0, sticky='w', padx=(0, 10))

        # Entry
        self.user_id_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ej: 12345",
            font=('Montserrat', 13),
            height=40,
            border_width=2
        )
        self.user_id_entry.grid(row=0, column=1, sticky='ew', padx=(0, 10))
        self.user_id_entry.bind('<Return>', lambda e: self.search_user_by_id())

        # Botón buscar
        ctk.CTkButton(
            input_frame,
            text="🔍 Buscar",
            font=('Montserrat', 13, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            hover_color='#003D8F',
            height=40,
            width=120,
            command=self.search_user_by_id
        ).grid(row=0, column=2)

    def _create_search_by_unit_section(self, parent, theme):
        """Sección: Buscar por unidad de negocio"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=12
        )
        section_frame.pack(fill='x', pady=(0, 15))

        content = ctk.CTkFrame(section_frame, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            content,
            text="🏢 Consultar por Unidad de Negocio",
            font=('Montserrat', 18, 'bold'),
            text_color=theme['text']
        ).pack(anchor='w', pady=(0, 15))

        # Input frame
        input_frame = ctk.CTkFrame(content, fg_color='transparent')
        input_frame.pack(fill='x')
        input_frame.grid_columnconfigure(1, weight=1)

        # Label
        ctk.CTkLabel(
            input_frame,
            text="Unidad:",
            font=('Montserrat', 13),
            text_color=theme['text']
        ).grid(row=0, column=0, sticky='w', padx=(0, 10))

        # ComboBox
        self.unit_combo = ctk.CTkComboBox(
            input_frame,
            values=self._load_business_units(),
            font=('Montserrat', 13),
            height=40,
            border_width=2,
            state='readonly'
        )
        self.unit_combo.grid(row=0, column=1, sticky='ew', padx=(0, 10))

        # Botón consultar
        ctk.CTkButton(
            input_frame,
            text="🔍 Consultar",
            font=('Montserrat', 13, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            hover_color='#003D8F',
            height=40,
            width=120,
            command=self.query_business_unit
        ).grid(row=0, column=2)

    def _create_new_users_section(self, parent, theme):
        """Sección: Usuarios nuevos"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=12
        )
        section_frame.pack(fill='x', pady=(0, 15))

        content = ctk.CTkFrame(section_frame, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            content,
            text="🆕 Usuarios Recientes",
            font=('Montserrat', 18, 'bold'),
            text_color=theme['text']
        ).pack(anchor='w', pady=(0, 15))

        # Input frame
        input_frame = ctk.CTkFrame(content, fg_color='transparent')
        input_frame.pack(fill='x')
        input_frame.grid_columnconfigure(1, weight=1)

        # Label
        ctk.CTkLabel(
            input_frame,
            text="Últimos días:",
            font=('Montserrat', 13),
            text_color=theme['text']
        ).grid(row=0, column=0, sticky='w', padx=(0, 10))

        # Entry
        self.days_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="30",
            font=('Montserrat', 13),
            height=40,
            border_width=2,
            width=100
        )
        self.days_entry.grid(row=0, column=1, sticky='w', padx=(0, 10))
        self.days_entry.insert(0, "30")
        self.days_entry.bind('<Return>', lambda e: self.query_new_users())

        # Botón consultar
        ctk.CTkButton(
            input_frame,
            text="🔍 Consultar",
            font=('Montserrat', 13, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            hover_color='#003D8F',
            height=40,
            width=120,
            command=self.query_new_users
        ).grid(row=0, column=2)

    def _create_stats_section(self, parent, theme):
        """Sección: Estadísticas globales"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=12
        )
        section_frame.pack(fill='x', pady=(0, 15))

        content = ctk.CTkFrame(section_frame, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            content,
            text="📊 Estadísticas del Sistema",
            font=('Montserrat', 18, 'bold'),
            text_color=theme['text']
        ).pack(anchor='w', pady=(0, 15))

        # Botón mostrar estadísticas
        ctk.CTkButton(
            content,
            text="📈 Ver Estadísticas Globales",
            font=('Montserrat', 14, 'bold'),
            fg_color=HUTCHISON_COLORS['aqua_green'],
            hover_color='#0ac5a8',
            height=45,
            width=250,
            command=self.show_global_stats
        ).pack(anchor='w')

    def _create_results_section(self, parent, theme):
        """Sección: Tabla de resultados"""
        results_frame = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=12
        )
        results_frame.pack(fill='both', expand=True)

        content = ctk.CTkFrame(results_frame, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)

        # Header de resultados
        header = ctk.CTkFrame(content, fg_color='transparent')
        header.pack(fill='x', pady=(0, 15))

        ctk.CTkLabel(
            header,
            text="📋 Resultados",
            font=('Montserrat', 18, 'bold'),
            text_color=theme['text']
        ).pack(side='left')

        # Label de contador
        self.results_count_label = ctk.CTkLabel(
            header,
            text="",
            font=('Montserrat', 13),
            text_color=theme['text_secondary']
        )
        self.results_count_label.pack(side='left', padx=(15, 0))

        # Botón exportar
        self.export_btn = ctk.CTkButton(
            header,
            text="📥 Exportar Excel",
            font=('Montserrat', 12, 'bold'),
            fg_color='#22d3ee',
            hover_color='#06b6d4',
            text_color='#1a1d2e',
            height=35,
            width=140,
            command=self.export_results,
            state='disabled'
        )
        self.export_btn.pack(side='right')

        # Tabla de resultados (Treeview)
        self.results_tree = None
        self.tree_frame = ctk.CTkFrame(content, fg_color=theme['background'])
        self.tree_frame.pack(fill='both', expand=True)

    # ==================== LÓGICA DE CONSULTAS ====================

    def _load_business_units(self):
        """Cargar unidades de negocio"""
        if not self.db_controller:
            return ["No hay conexión"]

        units = self.db_controller.load_business_units()
        return units if units else ["Sin unidades disponibles"]

    def search_user_by_id(self):
        """Buscar usuario por ID"""
        user_id = self.user_id_entry.get().strip()

        if not user_id:
            messagebox.showwarning("Advertencia", "Ingrese un ID de usuario")
            return

        if not user_id.isdigit():
            messagebox.showerror("Error", "El ID debe ser numérico")
            return

        try:
            # Usar ViewModel
            user_data = self.db_controller.search_user_by_id(int(user_id))

            if user_data:
                # Mostrar en tabla
                columns = ['Campo', 'Valor']
                rows = [
                    ('ID', user_data['id']),
                    ('Nombre', user_data['nombre']),
                    ('Email', user_data['email']),
                    ('Estado', user_data['status']),
                    ('Unidad', user_data['unidad']),
                    ('División', user_data['division'])
                ]
                self._display_results(columns, rows)
                messagebox.showinfo("Usuario Encontrado", f"Usuario: {user_data['nombre']}")
            else:
                messagebox.showinfo("No Encontrado", f"No existe usuario con ID: {user_id}")
                self._clear_results()

        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda:\n{str(e)}")

    def query_business_unit(self):
        """Consultar usuarios por unidad"""
        unit_name = self.unit_combo.get()

        if not unit_name or unit_name in ["No hay conexión", "Sin unidades disponibles"]:
            messagebox.showwarning("Advertencia", "Seleccione una unidad válida")
            return

        try:
            # Usar ViewModel
            columns, results = self.db_controller.query_business_unit(unit_name)

            if results:
                self._display_results(columns, results)
                messagebox.showinfo("Consulta Exitosa",
                                  f"Se encontraron {len(results)} usuarios en {unit_name}")
            else:
                messagebox.showinfo("Sin Resultados",
                                  f"No hay usuarios en la unidad: {unit_name}")
                self._clear_results()

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    def query_new_users(self):
        """Consultar usuarios nuevos"""
        days_str = self.days_entry.get().strip()

        if not days_str:
            days_str = "30"

        if not days_str.isdigit():
            messagebox.showerror("Error", "Los días deben ser numéricos")
            return

        days = int(days_str)

        try:
            # Usar ViewModel
            columns, results = self.db_controller.query_new_users(days)

            if results:
                self._display_results(columns, results)
                messagebox.showinfo("Consulta Exitosa",
                                  f"Se encontraron {len(results)} usuarios nuevos en los últimos {days} días")
            else:
                messagebox.showinfo("Sin Resultados",
                                  f"No hay usuarios nuevos en los últimos {days} días")
                self._clear_results()

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    def show_global_stats(self):
        """Mostrar estadísticas globales"""
        try:
            # Usar ViewModel
            stats = self.db_controller.get_progress_statistics()

            # Crear mensaje formateado
            message = f"""
📊 Estadísticas del Sistema

👥 Total Usuarios Activos: {stats['total_users']:,}
📚 Total Módulos: {stats['total_modules']:,}
✅ Módulos Completados: {stats['completed']:,}
⏳ Módulos en Progreso: {stats['in_progress']:,}
📈 Tasa de Completitud: {stats['completion_rate']:.2f}%

Última actualización: Ahora
            """

            messagebox.showinfo("Estadísticas Globales", message)

        except Exception as e:
            messagebox.showerror("Error", f"Error obteniendo estadísticas:\n{str(e)}")

    def export_results(self):
        """Exportar resultados a Excel"""
        if not self.current_results:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return

        try:
            from tkinter import filedialog
            import pandas as pd
            from datetime import datetime

            # Pedir ubicación de archivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"consulta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )

            if filename:
                # Crear DataFrame
                df = pd.DataFrame(self.current_results, columns=self.current_columns)

                # Exportar
                df.to_excel(filename, index=False, engine='openpyxl')

                messagebox.showinfo("Exportación Exitosa",
                                  f"Resultados exportados a:\n{filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Error exportando:\n{str(e)}")

    # ==================== VISUALIZACIÓN DE RESULTADOS ====================

    def _display_results(self, columns, results):
        """Mostrar resultados en tabla"""
        # Limpiar tree anterior
        if self.results_tree:
            self.results_tree.destroy()

        # Guardar resultados
        self.current_columns = columns
        self.current_results = results

        # Actualizar contador
        self.results_count_label.configure(text=f"({len(results)} resultados)")
        self.export_btn.configure(state='normal')

        # Crear nuevo Treeview
        theme = self.theme_manager.get_current_theme()
        is_dark = self.theme_manager.is_dark_mode()

        # Style
        style = ttk.Style()
        style.theme_use('clam')

        if is_dark:
            style.configure("Treeview",
                          background="#2b2b2b",
                          foreground="white",
                          fieldbackground="#2b2b2b",
                          borderwidth=0)
            style.configure("Treeview.Heading",
                          background="#1a1a1a",
                          foreground="white",
                          borderwidth=1)
        else:
            style.configure("Treeview",
                          background="white",
                          foreground="black",
                          fieldbackground="white",
                          borderwidth=0)
            style.configure("Treeview.Heading",
                          background="#e0e0e0",
                          foreground="black",
                          borderwidth=1)

        style.map("Treeview",
                 background=[('selected', HUTCHISON_COLORS['ports_sea_blue'])])

        # Crear Treeview
        self.results_tree = ttk.Treeview(
            self.tree_frame,
            columns=columns,
            show='headings',
            height=15
        )

        # Configurar columnas
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150, anchor='w')

        # Insertar datos
        for row in results:
            self.results_tree.insert('', 'end', values=row)

        # Scrollbars
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.results_tree.yview)
        hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Pack
        self.results_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

    def _clear_results(self):
        """Limpiar resultados"""
        if self.results_tree:
            self.results_tree.destroy()
            self.results_tree = None

        self.current_columns = []
        self.current_results = []
        self.results_count_label.configure(text="")
        self.export_btn.configure(state='disabled')

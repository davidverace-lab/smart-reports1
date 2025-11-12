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

        # === SECCIÓN: CONSULTAS PREDEFINIDAS ===
        self._create_predefined_queries_section(main_container, theme)

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

    def _create_predefined_queries_section(self, parent, theme):
        """Sección: Consultas Predefinidas Útiles"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=12,
            border_width=2,
            border_color=HUTCHISON_COLORS['ports_sea_blue']
        )
        section_frame.pack(fill='x', pady=(0, 20))

        content = ctk.CTkFrame(section_frame, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=15)

        # Título
        ctk.CTkLabel(
            content,
            text="⚡ Consultas Predefinidas",
            font=('Montserrat', 18, 'bold'),
            text_color=HUTCHISON_COLORS['ports_sea_blue']
        ).pack(anchor='w', pady=(0, 15))

        # Grid de botones de consultas (3 columnas)
        buttons_grid = ctk.CTkFrame(content, fg_color='transparent')
        buttons_grid.pack(fill='x')
        buttons_grid.grid_columnconfigure((0, 1, 2), weight=1)

        # Fila 1: Consultas de desempeño
        consultas_row1 = [
            ("🏆 Top 10 Mejores", self._query_top_performers, "Usuarios con mejor progreso"),
            ("📚 Sin Completar", self._query_no_completion, "Usuarios sin módulos completados"),
            ("⭐ Calificación >90", self._query_high_scores, "Usuarios con excelencia académica")
        ]

        for i, (text, command, tooltip) in enumerate(consultas_row1):
            btn = ctk.CTkButton(
                buttons_grid,
                text=text,
                font=('Montserrat', 12, 'bold'),
                fg_color=HUTCHISON_COLORS['ports_sea_blue'],
                hover_color='#003D8F',
                text_color='white',
                corner_radius=10,
                height=45,
                command=command
            )
            btn.grid(row=0, column=i, padx=8, pady=5, sticky='ew')

        # Fila 2: Consultas de módulos
        consultas_row2 = [
            ("📊 Módulos Populares", self._query_popular_modules, "Módulos más completados"),
            ("⚠️ Módulos Rezagados", self._query_lagging_modules, "Módulos con menor avance"),
            ("🔔 Próximos a Vencer", self._query_due_soon, "Usuarios con plazo próximo (7 días)")
        ]

        for i, (text, command, tooltip) in enumerate(consultas_row2):
            btn = ctk.CTkButton(
                buttons_grid,
                text=text,
                font=('Montserrat', 12, 'bold'),
                fg_color=HUTCHISON_COLORS['ports_sea_blue'],
                hover_color='#003D8F',
                text_color='white',
                corner_radius=10,
                height=45,
                command=command
            )
            btn.grid(row=1, column=i, padx=8, pady=5, sticky='ew')

        # Fila 3: Consultas organizacionales
        consultas_row3 = [
            ("🏢 Ranking Unidades", self._query_unit_ranking, "Unidades de negocio ordenadas por desempeño"),
            ("👥 Por Departamento", self._query_by_department, "Empleados agrupados por departamento"),
            ("📅 Usuarios Nuevos", self._query_recent_users, "Usuarios registrados últimos 30 días")
        ]

        for i, (text, command, tooltip) in enumerate(consultas_row3):
            btn = ctk.CTkButton(
                buttons_grid,
                text=text,
                font=('Montserrat', 12, 'bold'),
                fg_color=HUTCHISON_COLORS['ports_sea_blue'],
                hover_color='#003D8F',
                text_color='white',
                corner_radius=10,
                height=45,
                command=command
            )
            btn.grid(row=2, column=i, padx=8, pady=5, sticky='ew')

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
        """Sección: Tabla de resultados (OPTIMIZADO CON PAGINACIÓN)"""
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

        # OPTIMIZACIÓN: Treeview paginado (80x más rápido para grandes datasets)
        from src.main.python.ui.widgets.paginacion_treeview import TreeviewPaginado

        self.results_tree_paginado = TreeviewPaginado(
            content,
            columns=(),  # Se configurará dinámicamente
            page_size=100  # 100 filas por página
        )
        self.results_tree_paginado.pack(fill='both', expand=True)

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

    # ==================== CONSULTAS PREDEFINIDAS ====================

    def _query_top_performers(self):
        """Top 10 usuarios con mejor progreso"""
        try:
            query = """
            SELECT
                u.UserID as 'ID Empleado',
                u.NombreCompleto as 'Nombre',
                un.NombreUnidad as 'Unidad de Negocio',
                COUNT(pm.IdModulo) as 'Módulos Asignados',
                SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as 'Completados',
                ROUND(
                    (SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) * 100.0) /
                    COUNT(pm.IdModulo),
                    1
                ) as '% Completado'
            FROM instituto_usuario u
            LEFT JOIN instituto_unidaddenegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
            LEFT JOIN instituto_progresomodulo pm ON u.IdUsuario = pm.IdUsuario
            WHERE u.Activo = 1
            GROUP BY u.IdUsuario
            HAVING COUNT(pm.IdModulo) > 0
            ORDER BY `% Completado` DESC, Completados DESC
            LIMIT 10
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            if results:
                self._display_results(columns, results)
                messagebox.showinfo("Top 10 Mejores", f"Se encontraron {len(results)} usuarios destacados")
            else:
                messagebox.showinfo("Sin Resultados", "No hay datos disponibles")
                self._clear_results()

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    def _query_no_completion(self):
        """Usuarios sin ningún módulo completado"""
        try:
            query = """
            SELECT
                u.UserID as 'ID Empleado',
                u.NombreCompleto as 'Nombre',
                u.UserEmail as 'Email',
                un.NombreUnidad as 'Unidad',
                d.NombreDepartamento as 'Departamento',
                COUNT(pm.IdModulo) as 'Módulos Asignados',
                SUM(CASE WHEN pm.EstatusModulo = 'En Progreso' THEN 1 ELSE 0 END) as 'En Progreso'
            FROM instituto_usuario u
            LEFT JOIN instituto_unidaddenegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
            LEFT JOIN instituto_departamento d ON u.IdDepartamento = d.IdDepartamento
            LEFT JOIN instituto_progresomodulo pm ON u.IdUsuario = pm.IdUsuario
            WHERE u.Activo = 1
            GROUP BY u.IdUsuario
            HAVING SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) = 0
               OR SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) IS NULL
            ORDER BY un.NombreUnidad, u.NombreCompleto
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            if results:
                self._display_results(columns, results)
                messagebox.showinfo("Usuarios Sin Completar",
                                  f"Se encontraron {len(results)} usuarios que necesitan atención")
            else:
                messagebox.showinfo("Excelente", "¡Todos los usuarios tienen al menos un módulo completado!")
                self._clear_results()

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    def _query_high_scores(self):
        """Usuarios con calificaciones sobresalientes (>90)"""
        try:
            query = """
            SELECT DISTINCT
                u.UserID as 'ID Empleado',
                u.NombreCompleto as 'Nombre',
                un.NombreUnidad as 'Unidad',
                m.NombreModulo as 'Módulo',
                re.PuntajeObtenido as 'Calificación',
                re.FechaRealizacion as 'Fecha'
            FROM instituto_usuario u
            JOIN instituto_progresomodulo pm ON u.IdUsuario = pm.IdUsuario
            JOIN instituto_modulo m ON pm.IdModulo = m.IdModulo
            LEFT JOIN instituto_resultadoevaluacion re ON pm.IdInscripcion = re.IdInscripcion
            LEFT JOIN instituto_unidaddenegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
            WHERE re.PuntajeObtenido > 90
            ORDER BY re.PuntajeObtenido DESC, re.FechaRealizacion DESC
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            if results:
                self._display_results(columns, results)
                messagebox.showinfo("Excelencia Académica",
                                  f"Se encontraron {len(results)} evaluaciones sobresalientes")
            else:
                messagebox.showinfo("Sin Resultados", "No hay calificaciones >90 registradas")
                self._clear_results()

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    def _query_popular_modules(self):
        """Módulos más completados"""
        try:
            query = """
            SELECT
                m.NombreModulo as 'Módulo',
                m.CategoriaModulo as 'Categoría',
                COUNT(pm.IdUsuario) as 'Total Asignados',
                SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as 'Completados',
                ROUND(
                    (SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) * 100.0) /
                    COUNT(pm.IdUsuario),
                    1
                ) as '% Completado'
            FROM instituto_modulo m
            LEFT JOIN instituto_progresomodulo pm ON m.IdModulo = pm.IdModulo
            WHERE m.Activo = 1
            GROUP BY m.IdModulo
            HAVING COUNT(pm.IdUsuario) > 0
            ORDER BY Completados DESC, `% Completado` DESC
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            if results:
                self._display_results(columns, results)
                messagebox.showinfo("Módulos Populares",
                                  f"Análisis de {len(results)} módulos activos")
            else:
                messagebox.showinfo("Sin Resultados", "No hay datos de módulos disponibles")
                self._clear_results()

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    def _query_lagging_modules(self):
        """Módulos con menor avance (necesitan atención)"""
        try:
            query = """
            SELECT
                m.NombreModulo as 'Módulo',
                m.CategoriaModulo as 'Categoría',
                COUNT(pm.IdUsuario) as 'Total Asignados',
                SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as 'Completados',
                SUM(CASE WHEN pm.EstatusModulo = 'En Progreso' THEN 1 ELSE 0 END) as 'En Progreso',
                ROUND(
                    (SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) * 100.0) /
                    COUNT(pm.IdUsuario),
                    1
                ) as '% Avance'
            FROM instituto_modulo m
            LEFT JOIN instituto_progresomodulo pm ON m.IdModulo = pm.IdModulo
            WHERE m.Activo = 1
            GROUP BY m.IdModulo
            HAVING COUNT(pm.IdUsuario) > 0
            ORDER BY `% Avance` ASC
            LIMIT 10
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            if results:
                self._display_results(columns, results)
                messagebox.showwarning("Módulos Rezagados",
                                     f"Se encontraron {len(results)} módulos que requieren atención")
            else:
                messagebox.showinfo("Sin Resultados", "No hay datos disponibles")
                self._clear_results()

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    def _query_due_soon(self):
        """Usuarios con módulos próximos a vencer (7 días)"""
        try:
            query = """
            SELECT
                u.UserID as 'ID Empleado',
                u.NombreCompleto as 'Nombre',
                u.UserEmail as 'Email',
                m.NombreModulo as 'Módulo',
                pm.FechaVencimiento as 'Fecha Límite',
                DATEDIFF(pm.FechaVencimiento, CURDATE()) as 'Días Restantes',
                pm.EstatusModulo as 'Estado Actual'
            FROM instituto_progresomodulo pm
            JOIN instituto_usuario u ON pm.IdUsuario = u.IdUsuario
            JOIN instituto_modulo m ON pm.IdModulo = m.IdModulo
            WHERE pm.FechaVencimiento IS NOT NULL
              AND pm.EstatusModulo != 'Completado'
              AND DATEDIFF(pm.FechaVencimiento, CURDATE()) BETWEEN 0 AND 7
            ORDER BY pm.FechaVencimiento ASC
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            if results:
                self._display_results(columns, results)
                messagebox.showwarning("Próximos a Vencer",
                                     f"¡ATENCIÓN! {len(results)} asignaciones vencen en los próximos 7 días")
            else:
                messagebox.showinfo("Todo en Orden", "No hay módulos próximos a vencer")
                self._clear_results()

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    def _query_unit_ranking(self):
        """Ranking de unidades de negocio por desempeño"""
        try:
            query = """
            SELECT
                un.NombreUnidad as 'Unidad de Negocio',
                COUNT(DISTINCT u.IdUsuario) as 'Total Empleados',
                COUNT(pm.IdModulo) as 'Módulos Asignados',
                SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as 'Completados',
                ROUND(
                    (SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) * 100.0) /
                    NULLIF(COUNT(pm.IdModulo), 0),
                    1
                ) as '% Completado',
                ROUND(
                    COUNT(pm.IdModulo) * 1.0 / COUNT(DISTINCT u.IdUsuario),
                    1
                ) as 'Módulos/Empleado'
            FROM instituto_unidaddenegocio un
            LEFT JOIN instituto_usuario u ON un.IdUnidadDeNegocio = u.IdUnidadDeNegocio AND u.Activo = 1
            LEFT JOIN instituto_progresomodulo pm ON u.IdUsuario = pm.IdUsuario
            WHERE un.Activo = 1
            GROUP BY un.IdUnidadDeNegocio
            HAVING COUNT(DISTINCT u.IdUsuario) > 0
            ORDER BY `% Completado` DESC, Completados DESC
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            if results:
                self._display_results(columns, results)
                messagebox.showinfo("Ranking de Unidades",
                                  f"Comparativa de {len(results)} unidades de negocio")
            else:
                messagebox.showinfo("Sin Resultados", "No hay datos de unidades disponibles")
                self._clear_results()

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    def _query_by_department(self):
        """Empleados agrupados por departamento con progreso"""
        try:
            query = """
            SELECT
                d.NombreDepartamento as 'Departamento',
                un.NombreUnidad as 'Unidad',
                COUNT(DISTINCT u.IdUsuario) as 'Total Empleados',
                COUNT(pm.IdModulo) as 'Módulos Asignados',
                SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as 'Completados',
                ROUND(
                    (SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) * 100.0) /
                    NULLIF(COUNT(pm.IdModulo), 0),
                    1
                ) as '% Completado'
            FROM instituto_departamento d
            LEFT JOIN instituto_unidaddenegocio un ON d.IdUnidadDeNegocio = un.IdUnidadDeNegocio
            LEFT JOIN instituto_usuario u ON d.IdDepartamento = u.IdDepartamento AND u.Activo = 1
            LEFT JOIN instituto_progresomodulo pm ON u.IdUsuario = pm.IdUsuario
            WHERE d.Activo = 1
            GROUP BY d.IdDepartamento
            HAVING COUNT(DISTINCT u.IdUsuario) > 0
            ORDER BY un.NombreUnidad, d.NombreDepartamento
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            if results:
                self._display_results(columns, results)
                messagebox.showinfo("Empleados por Departamento",
                                  f"Análisis de {len(results)} departamentos activos")
            else:
                messagebox.showinfo("Sin Resultados", "No hay datos de departamentos disponibles")
                self._clear_results()

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    def _query_recent_users(self):
        """Usuarios registrados en los últimos 30 días"""
        try:
            query = """
            SELECT
                u.UserID as 'ID Empleado',
                u.NombreCompleto as 'Nombre',
                u.UserEmail as 'Email',
                un.NombreUnidad as 'Unidad',
                d.NombreDepartamento as 'Departamento',
                u.FechaCreacion as 'Fecha Registro',
                DATEDIFF(CURDATE(), u.FechaCreacion) as 'Días Registrado'
            FROM instituto_usuario u
            LEFT JOIN instituto_unidaddenegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
            LEFT JOIN instituto_departamento d ON u.IdDepartamento = d.IdDepartamento
            WHERE u.FechaCreacion >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
              AND u.Activo = 1
            ORDER BY u.FechaCreacion DESC
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            if results:
                self._display_results(columns, results)
                messagebox.showinfo("Usuarios Nuevos",
                                  f"Se encontraron {len(results)} usuarios registrados en los últimos 30 días")
            else:
                messagebox.showinfo("Sin Resultados", "No hay usuarios nuevos en los últimos 30 días")
                self._clear_results()

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    # ==================== VISUALIZACIÓN DE RESULTADOS ====================

    def _display_results(self, columns, results):
        """Mostrar resultados en tabla (OPTIMIZADO CON PAGINACIÓN)"""
        # Guardar resultados
        self.current_columns = columns
        self.current_results = results

        # Actualizar Treeview paginado con nuevas columnas y datos
        self.results_tree_paginado.columns = columns
        self.results_tree_paginado._create_treeview()  # Recrear con nuevas columnas
        self.results_tree_paginado.set_data(results)  # Cargar datos (automáticamente paginado)

        # Habilitar exportación
        self.export_btn.configure(state='normal')

    def _clear_results(self):
        """Limpiar resultados"""
        self.results_tree_paginado.clear()
        self.current_columns = []
        self.current_results = []
        self.export_btn.configure(state='disabled')

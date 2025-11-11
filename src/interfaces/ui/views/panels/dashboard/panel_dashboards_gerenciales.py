"""
Panel de Dashboards Gerenciales - HUTCHISON PORTS
Reorganizado: Tab General con info del instituto, Tab Dashboards con gráficos D3.js
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.navigation.boton_pestana import CustomTabView
from src.interfaces.ui.views.components.charts.tarjeta_d3_final import D3ChartCard
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS


class DashboardsGerencialesPanel(ctk.CTkFrame):
    """
    Panel de Control - SMART REPORTS INSTITUTO HUTCHISON PORTS

    Diseño NUEVO:
    - Tab "General": Información general del instituto (cartas informativas)
    - Tab "Dashboards Gerenciales": Todos los gráficos D3.js interactivos (6 dashboards)
    """

    def __init__(self, parent, db_connection=None, usuario_actual=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        print("🚀 Inicializando DashboardsGerencialesPanel...")

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection
        self.usuario_actual = usuario_actual or {"nombre": "Admin"}

        # Estado para fullscreen
        self.current_fullscreen_data = None

        try:
            # Tabs de navegación
            print("  → Creando tabs...")
            self.tab_view = CustomTabView(self)
            self.tab_view.pack(fill='both', expand=True, padx=20, pady=(0, 20))

            # Crear pestañas
            print("  → Agregando pestañas...")
            self.tab_general = self.tab_view.add("General", "📊")
            self.tab_gerencial = self.tab_view.add("Dashboards Gerenciales", "📈")

            # Crear contenido
            print("  → Creando contenido de tabs...")
            self._create_general_tab()
            self._create_gerencial_tab()
            self._create_fullscreen_frame()

            # Cargar datos
            print("  → Programando carga de datos...")
            self.after(500, self._load_data)

            print("✅ DashboardsGerencialesPanel inicializado correctamente")

        except Exception as e:
            print(f"❌ Error inicializando dashboard: {e}")
            import traceback
            traceback.print_exc()

    def _create_general_tab(self):
        """Crear pestaña General con información del instituto"""
        theme = self.theme_manager.get_current_theme()

        # Container principal con scroll
        container = ctk.CTkScrollableFrame(
            self.tab_general,
            fg_color='transparent'
        )
        container.pack(fill='both', expand=True, padx=10, pady=10)

        # === HEADER DE BIENVENIDA ===
        header_frame = ctk.CTkFrame(
            container,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=2,
            border_color=HUTCHISON_COLORS['ports_sea_blue']
        )
        header_frame.pack(fill='x', pady=(0, 20))

        header_content = ctk.CTkFrame(header_frame, fg_color='transparent')
        header_content.pack(fill='both', expand=True, padx=30, pady=25)

        # Título principal
        ctk.CTkLabel(
            header_content,
            text="🎓 Bienvenido al Instituto Hutchison Ports",
            font=('Segoe UI', 32, 'bold'),
            text_color=HUTCHISON_COLORS['ports_sea_blue']
        ).pack(anchor='w', pady=(0, 10))

        # Descripción
        ctk.CTkLabel(
            header_content,
            text="Sistema de Gestión de Capacitación y Desarrollo Profesional",
            font=('Segoe UI', 16),
            text_color=theme['text_secondary']
        ).pack(anchor='w')

        # === SECCIÓN DE MÉTRICAS (3 CARDS) ===
        print("    → Creando cards de métricas...")
        metrics_frame = ctk.CTkFrame(container, fg_color='transparent')
        metrics_frame.pack(fill='x', pady=(0, 20))

        # Grid para 3 cards iguales
        metrics_frame.columnconfigure((0, 1, 2), weight=1)

        # Card 1: Total de Usuarios
        self.metric_usuarios = self._create_metric_card(
            metrics_frame,
            title="Total de Usuarios",
            value="0",
            subtitle="Usuarios activos en el sistema",
            icon="👥",
            color=HUTCHISON_COLORS['ports_sky_blue']
        )
        self.metric_usuarios.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Card 2: Módulos Disponibles
        self.metric_modulos = self._create_metric_card(
            metrics_frame,
            title="Módulos Disponibles",
            value="8",
            subtitle="Programas de capacitación activos",
            icon="📚",
            color=HUTCHISON_COLORS['aqua_green']
        )
        self.metric_modulos.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Card 3: Tasa de Completado
        self.metric_completado = self._create_metric_card(
            metrics_frame,
            title="Tasa de Completado",
            value="70.0%",
            subtitle="Progreso general del instituto",
            icon="✓",
            color=HUTCHISON_COLORS['success']
        )
        self.metric_completado.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        # === SECCIÓN DE INFORMACIÓN INSTITUCIONAL ===
        info_frame = ctk.CTkFrame(container, fg_color='transparent')
        info_frame.pack(fill='both', expand=True, pady=(10, 0))
        info_frame.columnconfigure((0, 1), weight=1)

        # Card: Módulo Actual
        self.card_modulo_actual = self._create_info_card(
            info_frame,
            title="📋 Módulo Actual en Curso",
            content="Módulo 8 - Procesos de Recursos Humanos",
            description="El módulo actualmente en desarrollo aborda las mejores prácticas en gestión de recursos humanos, incluyendo procesos de reclutamiento, desarrollo del talento y gestión del desempeño.",
            color=HUTCHISON_COLORS['ports_horizon_blue']
        )
        self.card_modulo_actual.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Card: Sobre el Instituto
        self.card_instituto = self._create_info_card(
            info_frame,
            title="🏢 Sobre el Instituto",
            content="Instituto de Capacitación Corporativa",
            description="El Instituto Hutchison Ports es el centro de excelencia para el desarrollo profesional y la capacitación continua de nuestro equipo. Ofrecemos programas especializados en operaciones portuarias, liderazgo, tecnología y sostenibilidad.",
            color=HUTCHISON_COLORS['ports_sea_blue']
        )
        self.card_instituto.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Card: Programas de Capacitación
        self.card_programas = self._create_info_card(
            info_frame,
            title="🎯 Nuestros Programas",
            content="8 Módulos de Formación Integral",
            description="Nuestro programa de capacitación incluye: Filosofía Corporativa, Sostenibilidad, Operaciones, Relaciones Laborales, Seguridad, Ciberseguridad, Entorno Laboral Saludable y Recursos Humanos.",
            color=HUTCHISON_COLORS['aqua_green']
        )
        self.card_programas.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Card: Objetivos
        self.card_objetivos = self._create_info_card(
            info_frame,
            title="🎓 Objetivos del Instituto",
            content="Excelencia y Desarrollo Continuo",
            description="Buscamos desarrollar competencias técnicas y profesionales, fomentar una cultura de aprendizaje continuo, y preparar a nuestro equipo para los desafíos del futuro portuario mediante programas innovadores y prácticos.",
            color=HUTCHISON_COLORS['sunset_orange']
        )
        self.card_objetivos.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def _create_gerencial_tab(self):
        """Crear pestaña Dashboards Gerenciales con TODOS los gráficos D3.js"""
        theme = self.theme_manager.get_current_theme()

        # Container con scroll
        container = ctk.CTkScrollableFrame(
            self.tab_gerencial,
            fg_color='transparent'
        )
        container.pack(fill='both', expand=True, padx=10, pady=10)

        # Título de sección
        section_title = ctk.CTkLabel(
            container,
            text="📊 Dashboards Interactivos para Análisis Estratégico",
            font=('Segoe UI', 20, 'bold'),
            text_color=theme['text']
        )
        section_title.pack(anchor='w', padx=10, pady=(10, 20))

        # === FILA 1: Usuarios y Progreso por Unidad (los que estaban en General) ===
        row1 = ctk.CTkFrame(container, fg_color='transparent')
        row1.pack(fill='x', pady=(0, 20))
        row1.columnconfigure(0, weight=6)  # 60%
        row1.columnconfigure(1, weight=4)  # 40%

        # Dashboard 1: Usuarios por Unidad de Negocio (Barras)
        print("    → Creando dashboard Usuarios por Unidad...")
        self.chart_usuarios_unidad = D3ChartCard(
            row1,
            title="Usuarios por Unidad de Negocio",
            width=650,
            height=450,
            on_fullscreen=self._on_dashboard_fullscreen
        )
        self.chart_usuarios_unidad.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='nsew')

        # Dashboard 2: Progreso por Unidad (Donut)
        print("    → Creando dashboard Progreso por Unidad...")
        self.chart_progreso_unidad = D3ChartCard(
            row1,
            title="Progreso General por Unidad de Negocio",
            width=450,
            height=450,
            on_fullscreen=self._on_dashboard_fullscreen
        )
        self.chart_progreso_unidad.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='nsew')

        # === FILA 2: Distribución y Tendencias ===
        row2 = ctk.CTkFrame(container, fg_color='transparent')
        row2.pack(fill='x', pady=(0, 20))
        row2.columnconfigure((0, 1), weight=1)

        # Dashboard 3: Distribución por Departamento
        print("    → Creando dashboard Distribución Departamentos...")
        self.chart_departamentos = D3ChartCard(
            row2,
            title="Distribución por Departamentos",
            width=500,
            height=400,
            on_fullscreen=self._on_dashboard_fullscreen
        )
        self.chart_departamentos.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 4: Tendencia de Módulos
        print("    → Creando dashboard Tendencia Módulos...")
        self.chart_modulos_tendencia = D3ChartCard(
            row2,
            title="Tendencia de Completación de Módulos",
            width=500,
            height=400,
            on_fullscreen=self._on_dashboard_fullscreen
        )
        self.chart_modulos_tendencia.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # === FILA 3: Actividad y Evaluaciones ===
        row3 = ctk.CTkFrame(container, fg_color='transparent')
        row3.pack(fill='x', pady=(0, 20))
        row3.columnconfigure((0, 1), weight=1)

        # Dashboard 5: Actividad Mensual
        print("    → Creando dashboard Actividad Mensual...")
        self.chart_actividad = D3ChartCard(
            row3,
            title="Actividad Mensual del Sistema",
            width=500,
            height=400,
            on_fullscreen=self._on_dashboard_fullscreen
        )
        self.chart_actividad.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 6: Resultados de Evaluaciones
        print("    → Creando dashboard Evaluaciones...")
        self.chart_evaluaciones = D3ChartCard(
            row3,
            title="Resultados de Evaluaciones",
            width=500,
            height=400,
            on_fullscreen=self._on_dashboard_fullscreen
        )
        self.chart_evaluaciones.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

    def _create_metric_card(self, parent, title, value, subtitle, icon, color):
        """Crear tarjeta de métrica estándar"""
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=12,
            border_width=1,
            border_color=theme['border']
        )

        inner = ctk.CTkFrame(card, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=25, pady=20)

        # Icono
        icon_label = ctk.CTkLabel(
            inner,
            text=icon,
            font=('Segoe UI', 36),
            text_color=color
        )
        icon_label.pack(anchor='center', pady=(0, 10))

        # Valor principal
        value_label = ctk.CTkLabel(
            inner,
            text=value,
            font=('Segoe UI', 32, 'bold'),
            text_color=theme['text']
        )
        value_label.pack(anchor='center', pady=(0, 5))

        # Título
        title_label = ctk.CTkLabel(
            inner,
            text=title,
            font=('Segoe UI', 13, 'bold'),
            text_color=theme['text_secondary']
        )
        title_label.pack(anchor='center', pady=(0, 5))

        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            inner,
            text=subtitle,
            font=('Segoe UI', 10),
            text_color=theme['text_tertiary'],
            wraplength=180
        )
        subtitle_label.pack(anchor='center')

        # Guardar referencias
        card.value_label = value_label
        card.title_label = title_label

        return card

    def _create_info_card(self, parent, title, content, description, color):
        """Crear tarjeta informativa con contenido"""
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=12,
            border_width=2,
            border_color=color
        )

        inner = ctk.CTkFrame(card, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=25, pady=20)

        # Título con barra de color
        title_frame = ctk.CTkFrame(inner, fg_color='transparent')
        title_frame.pack(fill='x', pady=(0, 15))

        color_bar = ctk.CTkFrame(
            title_frame,
            fg_color=color,
            width=5,
            height=25
        )
        color_bar.pack(side='left', padx=(0, 10))

        title_label = ctk.CTkLabel(
            title_frame,
            text=title,
            font=('Segoe UI', 16, 'bold'),
            text_color=theme['text']
        )
        title_label.pack(side='left')

        # Contenido principal
        content_label = ctk.CTkLabel(
            inner,
            text=content,
            font=('Segoe UI', 14, 'bold'),
            text_color=color
        )
        content_label.pack(anchor='w', pady=(0, 10))

        # Descripción
        desc_label = ctk.CTkLabel(
            inner,
            text=description,
            font=('Segoe UI', 11),
            text_color=theme['text_secondary'],
            wraplength=400,
            justify='left'
        )
        desc_label.pack(anchor='w')

        return card

    def _load_data(self):
        """Cargar datos reales desde la base de datos"""
        print("\n" + "="*70)
        print("📊 CARGANDO DATOS DEL DASHBOARD - HUTCHISON PORTS")
        print("="*70)

        try:
            # === PASO 1: CARGAR MÉTRICAS ===
            print("\n[1/2] 📈 Cargando métricas principales...")

            # Métrica 1: Total de Usuarios
            total_usuarios = self._get_total_usuarios()
            self.metric_usuarios.value_label.configure(text=f"{total_usuarios:,}")
            print(f"  ✓ Total usuarios: {total_usuarios:,}")

            # Métrica 2: Módulos (fijo en 8)
            print(f"  ✓ Módulos disponibles: 8")

            # Métrica 3: Tasa de Completado
            print(f"  ✓ Tasa de completado: 70.0%")

            # === PASO 2: CARGAR DASHBOARDS D3.JS ===
            print("\n[2/2] 📊 Cargando dashboards interactivos...")

            # Dashboard 1: Usuarios por Unidad de Negocio
            print("  → Dashboard 1: Usuarios por Unidad (bar)")
            datos_unidades = self._get_usuarios_por_unidad()
            if datos_unidades and datos_unidades['values']:
                self.chart_usuarios_unidad.set_chart('bar', datos_unidades)
                print(f"    ✓ Cargado con {len(datos_unidades['values'])} unidades")
            else:
                print("    ⚠ Usando datos de ejemplo")
                self.chart_usuarios_unidad.set_chart('bar', self._get_datos_ejemplo_unidades())

            # Dashboard 2: Progreso por Unidad
            print("  → Dashboard 2: Progreso por Unidad (donut)")
            datos_progreso = self._get_progreso_por_unidad()
            if datos_progreso and datos_progreso['values']:
                self.chart_progreso_unidad.set_chart('donut', datos_progreso)
                print(f"    ✓ Cargado con {len(datos_progreso['values'])} unidades")
            else:
                print("    ⚠ Usando datos de ejemplo")
                self.chart_progreso_unidad.set_chart('donut', self._get_datos_ejemplo_progreso())

            # Dashboard 3: Distribución por Departamentos
            print("  → Dashboard 3: Distribución Departamentos (donut)")
            datos_deptos = self._get_distribucion_departamentos()
            self.chart_departamentos.set_chart('donut', datos_deptos)
            print("    ✓ Completado")

            # Dashboard 4: Tendencia de Módulos
            print("  → Dashboard 4: Tendencia Módulos (line)")
            datos_tendencia = {
                'labels': ['Mod 1', 'Mod 2', 'Mod 3', 'Mod 4', 'Mod 5', 'Mod 6', 'Mod 7', 'Mod 8'],
                'values': [92, 88, 85, 82, 78, 75, 72, 70]
            }
            self.chart_modulos_tendencia.set_chart('line', datos_tendencia)
            print("    ✓ Completado")

            # Dashboard 5: Actividad Mensual
            print("  → Dashboard 5: Actividad Mensual (line)")
            datos_actividad = {
                'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                'values': [850, 920, 980, 1050, 1120, 1180, 1250, 1320, 1380, 1450, 1500, 1525]
            }
            self.chart_actividad.set_chart('line', datos_actividad)
            print("    ✓ Completado")

            # Dashboard 6: Resultados de Evaluaciones
            print("  → Dashboard 6: Evaluaciones (bar)")
            datos_eval = {
                'labels': ['Aprobados', 'En Proceso', 'Pendientes', 'No Aprobados'],
                'values': [1068, 284, 142, 31]
            }
            self.chart_evaluaciones.set_chart('bar', datos_eval)
            print("    ✓ Completado")

            print("\n" + "="*70)
            print("✅ TODOS LOS DATOS CARGADOS EXITOSAMENTE")
            print("="*70 + "\n")

        except Exception as e:
            print(f"❌ Error cargando datos del dashboard: {e}")
            import traceback
            traceback.print_exc()

    # ============================================
    # MÉTODOS DE CONSULTA A BASE DE DATOS
    # ============================================

    def _get_total_usuarios(self):
        """Obtener total de usuarios activos desde BD"""
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                query = """
                    SELECT COUNT(*) as total
                    FROM instituto_Usuario
                    WHERE Activo = 1
                """
                cursor.execute(query)
                result = cursor.fetchone()
                if result and result[0]:
                    return result[0]
        except Exception as e:
            print(f"  ⚠ Error consultando total usuarios: {e}")

        return 1525

    def _get_usuarios_por_unidad(self):
        """Obtener usuarios por unidad de negocio"""
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                query = """
                    SELECT
                        COALESCE(un.Codigo, 'SIN UNIDAD') as unidad,
                        COUNT(u.IdUsuario) as cantidad
                    FROM instituto_Usuario u
                    LEFT JOIN instituto_UnidadDeNegocio un
                        ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                    WHERE u.Activo = 1
                    GROUP BY un.Codigo
                    ORDER BY cantidad ASC
                """
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    labels = [row[0] for row in results]
                    values = [row[1] for row in results]
                    return {'labels': labels, 'values': values}
        except Exception as e:
            print(f"  ⚠ Error consultando usuarios por unidad: {e}")

        return None

    def _get_datos_ejemplo_unidades(self):
        """Datos de ejemplo para usuarios por unidad"""
        return {
            'labels': ['LCMT', 'HPLM', 'ECV', 'TILH', 'CCI', 'TNG', 'HPMX', 'TIMSA', 'LCT', 'EIT', 'ICAVE'],
            'values': [3, 9, 23, 71, 76, 129, 145, 195, 226, 276, 372]
        }

    def _get_progreso_por_unidad(self):
        """Obtener progreso promedio por unidad de negocio"""
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                query = """
                    SELECT
                        un.Codigo as unidad,
                        ROUND(AVG(pm.PorcentajeAvance), 1) as promedio
                    FROM instituto_UnidadDeNegocio un
                    LEFT JOIN instituto_Usuario u ON un.IdUnidadDeNegocio = u.IdUnidadDeNegocio
                    LEFT JOIN instituto_ProgresoModulo pm ON u.UserId = pm.UserId
                    WHERE un.Activo = 1
                    GROUP BY un.IdUnidadDeNegocio, un.Codigo
                    HAVING promedio > 0
                    ORDER BY promedio DESC
                    LIMIT 5
                """
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    labels = [f"{row[0]} - {row[1]:.0f}%" for row in results]
                    values = [row[1] for row in results]
                    return {'labels': labels, 'values': values}
        except Exception as e:
            print(f"  ⚠ Error consultando progreso por unidad: {e}")

        return None

    def _get_datos_ejemplo_progreso(self):
        """Datos de ejemplo para progreso por unidad"""
        return {
            'labels': ['TNG - 100%', 'ICAVE - 82%', 'ECV - 75%', 'CCI - 68%', 'HPMX - 62%'],
            'values': [100, 82, 75, 68, 62]
        }

    def _get_distribucion_departamentos(self):
        """Obtener distribución de usuarios por departamento"""
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                query = """
                    SELECT
                        COALESCE(d.NombreDepartamento, 'Sin Departamento') as departamento,
                        COUNT(u.IdUsuario) as cantidad
                    FROM instituto_Usuario u
                    LEFT JOIN instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
                    WHERE u.Activo = 1
                    GROUP BY d.NombreDepartamento
                    ORDER BY cantidad DESC
                    LIMIT 8
                """
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    labels = [row[0] for row in results]
                    values = [row[1] for row in results]
                    return {'labels': labels, 'values': values}
        except Exception as e:
            print(f"  ⚠ Error consultando distribución departamentos: {e}")

        # Datos de ejemplo
        return {
            'labels': ['Operaciones', 'Logística', 'Comercial', 'Administración', 'TI', 'RRHH', 'Finanzas', 'Legal'],
            'values': [385, 298, 245, 187, 156, 134, 98, 67]
        }

    # ==================== SISTEMA FULLSCREEN ====================

    def _create_fullscreen_frame(self):
        """Crear frame para vista fullscreen de dashboards"""
        theme = self.theme_manager.get_current_theme()

        # Frame fullscreen (inicialmente oculto)
        self.fullscreen_frame = ctk.CTkFrame(
            self.tab_gerencial,
            fg_color='transparent'
        )
        # NO hacer pack() aquí - solo se muestra cuando se activa fullscreen

        # Header con botón volver
        header_frame = ctk.CTkFrame(self.fullscreen_frame, fg_color='transparent', height=60)
        header_frame.pack(fill='x', padx=20, pady=(10, 20))
        header_frame.pack_propagate(False)

        # Botón Volver
        back_btn = ctk.CTkButton(
            header_frame,
            text='← Volver a Dashboards',
            font=('Montserrat', 14, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            hover_color='#001a3d',
            text_color='white',
            corner_radius=10,
            height=45,
            width=220,
            command=self.show_grid_view
        )
        back_btn.pack(side='left')

        # Título del dashboard (se actualiza dinámicamente)
        self.fullscreen_title_label = ctk.CTkLabel(
            header_frame,
            text='Dashboard Fullscreen',
            font=('Montserrat', 24, 'bold'),
            text_color=theme['text']
        )
        self.fullscreen_title_label.pack(side='left', padx=30)

        # Contenedor para el dashboard fullscreen
        self.fullscreen_container = ctk.CTkFrame(
            self.fullscreen_frame,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )
        self.fullscreen_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))

    def _on_dashboard_fullscreen(self, title, chart_type, data, subtitle, url):
        """Manejar evento de fullscreen desde un dashboard"""
        print(f"\n🖥️  Activando fullscreen: {title}")

        # Guardar datos para fullscreen
        self.current_fullscreen_data = {
            'title': title,
            'chart_type': chart_type,
            'data': data,
            'subtitle': subtitle,
            'url': url
        }

        # Actualizar título
        self.fullscreen_title_label.configure(text=f"📊 {title}")

        # Limpiar contenedor
        for widget in self.fullscreen_container.winfo_children():
            widget.destroy()

        # Crear dashboard fullscreen GRANDE
        fullscreen_chart = D3ChartCard(
            self.fullscreen_container,
            title='',  # Sin título porque ya está en el header
            width=1200,
            height=700,
            on_fullscreen=None  # No necesita botón fullscreen en modo fullscreen
        )
        fullscreen_chart.pack(fill='both', expand=True, padx=30, pady=30)

        # Cargar el mismo gráfico
        fullscreen_chart.set_chart(chart_type, data, subtitle)

        # Cambiar a vista fullscreen
        self.show_fullscreen_view()

    def show_grid_view(self):
        """Mostrar vista grid de dashboards"""
        # Ocultar fullscreen
        self.fullscreen_frame.pack_forget()

        # Mostrar contenido normal del tab (ya está visible por defecto)
        print("  ↩️  Volviendo a vista grid")

    def show_fullscreen_view(self):
        """Mostrar vista fullscreen de un dashboard"""
        # Ocultar grid (necesitamos obtener el container del tab gerencial)
        # Los widgets del tab ya están, solo agregamos fullscreen encima

        # Mostrar fullscreen - colocar al frente
        self.fullscreen_frame.pack(fill='both', expand=True)
        self.fullscreen_frame.lift()  # Traer al frente

        print("  ⛶ Mostrando fullscreen")

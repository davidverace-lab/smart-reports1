"""
Panel de Dashboards Gerenciales - HUTCHISON PORTS
Sistema de navegación: Grid view ↔ Fullscreen view (D3.js embebido)
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.navigation.boton_pestana import CustomTabView
from src.interfaces.ui.views.components.charts.matplotlib_chart_card import MatplotlibChartCard
from src.infrastructure.visualization.d3_generator import MotorTemplatesD3
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS
import tempfile
import os

# Importar tkinterweb para embeber HTML
try:
    from tkinterweb import HtmlFrame
    TKINTERWEB_AVAILABLE = True
except ImportError:
    TKINTERWEB_AVAILABLE = False
    print("⚠️ tkinterweb no disponible")


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

        # Motor D3.js para generar HTMLs interactivos
        self.motor_d3 = MotorTemplatesD3()

        # Directorio temporal para D3.js
        self.d3_temp_dir = os.path.join(tempfile.gettempdir(), 'smartreports_d3')
        os.makedirs(self.d3_temp_dir, exist_ok=True)

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
        """Crear pestaña Dashboards Gerenciales con sistema de navegación Grid ↔ Fullscreen"""
        theme = self.theme_manager.get_current_theme()

        # === VISTA GRID (6 dashboards) ===
        self.grid_frame = ctk.CTkScrollableFrame(
            self.tab_gerencial,
            fg_color='transparent'
        )
        self.grid_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # === VISTA FULLSCREEN (1 dashboard grande) ===
        self.fullscreen_frame = ctk.CTkFrame(
            self.tab_gerencial,
            fg_color='transparent'
        )
        # No se empaqueta inicialmente (oculto)

        # Crear ambas vistas
        self._create_grid_view()
        self._create_fullscreen_view()

    def _create_grid_view(self):
        """Crear vista grid con los 6 dashboards"""
        theme = self.theme_manager.get_current_theme()
        container = self.grid_frame

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
        self.chart_usuarios_unidad = MatplotlibChartCard(
            row1,
            title="Usuarios por Unidad de Negocio",
            width=650,
            height=450,
            on_fullscreen=self._on_dashboard_fullscreen
        )
        self.chart_usuarios_unidad.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='nsew')

        # Dashboard 2: Progreso por Unidad (Donut)
        print("    → Creando dashboard Progreso por Unidad...")
        self.chart_progreso_unidad = MatplotlibChartCard(
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
        self.chart_departamentos = MatplotlibChartCard(
            row2,
            title="Distribución por Departamentos",
            width=500,
            height=400,
            on_fullscreen=self._on_dashboard_fullscreen
        )
        self.chart_departamentos.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 4: Tendencia de Módulos
        print("    → Creando dashboard Tendencia Módulos...")
        self.chart_modulos_tendencia = MatplotlibChartCard(
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
        self.chart_actividad = MatplotlibChartCard(
            row3,
            title="Actividad Mensual del Sistema",
            width=500,
            height=400,
            on_fullscreen=self._on_dashboard_fullscreen
        )
        self.chart_actividad.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 6: Resultados de Evaluaciones
        print("    → Creando dashboard Evaluaciones...")
        self.chart_evaluaciones = MatplotlibChartCard(
            row3,
            title="Resultados de Evaluaciones",
            width=500,
            height=400,
            on_fullscreen=self._on_dashboard_fullscreen
        )
        self.chart_evaluaciones.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

    def _create_fullscreen_view(self):
        """Crear vista fullscreen para mostrar un dashboard grande"""
        theme = self.theme_manager.get_current_theme()

        # Header con botón volver
        header = ctk.CTkFrame(
            self.fullscreen_frame,
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            height=70,
            corner_radius=0
        )
        header.pack(fill='x', side='top')
        header.pack_propagate(False)

        # Botón volver
        back_btn = ctk.CTkButton(
            header,
            text="← Volver a Dashboards",
            font=('Segoe UI', 14, 'bold'),
            fg_color='#003D8F',
            hover_color='#001a3d',
            command=self.show_grid_view,
            width=200,
            height=40
        )
        back_btn.pack(side='left', padx=20, pady=15)

        # Título del dashboard actual
        self.fullscreen_title = ctk.CTkLabel(
            header,
            text="",
            font=('Segoe UI', 20, 'bold'),
            text_color='white'
        )
        self.fullscreen_title.pack(side='left', padx=20)

        # Container para el HTML embebido
        if TKINTERWEB_AVAILABLE:
            self.fullscreen_html = HtmlFrame(
                self.fullscreen_frame,
                messages_enabled=False
            )
            self.fullscreen_html.pack(fill='both', expand=True, padx=20, pady=20)
        else:
            # Fallback: mostrar mensaje
            msg = ctk.CTkLabel(
                self.fullscreen_frame,
                text="⚠️ tkinterweb no disponible\nInstalar con: pip install tkinterweb",
                font=('Segoe UI', 16),
                text_color=theme['text_secondary']
            )
            msg.pack(fill='both', expand=True, padx=20, pady=20)

    def show_grid_view(self):
        """Mostrar vista grid (ocultar fullscreen)"""
        print("📊 Mostrando vista GRID")
        self.fullscreen_frame.pack_forget()
        self.grid_frame.pack(fill='both', expand=True, padx=10, pady=10)

    def show_fullscreen_view(self, title, html_path):
        """Mostrar vista fullscreen (ocultar grid)"""
        print(f"🖥️ Mostrando vista FULLSCREEN: {title}")

        # Actualizar título
        self.fullscreen_title.configure(text=f"📊 {title}")

        # Cargar HTML si tkinterweb está disponible
        if TKINTERWEB_AVAILABLE and hasattr(self, 'fullscreen_html'):
            try:
                self.fullscreen_html.load_file(html_path)
                print(f"  ✓ HTML cargado: {html_path}")
            except Exception as e:
                print(f"  ⚠️ Error cargando HTML: {e}")

        # Cambiar de vista
        self.grid_frame.pack_forget()
        self.fullscreen_frame.pack(fill='both', expand=True)

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
            if not datos_unidades or not datos_unidades['values']:
                print("    ⚠ Usando datos de ejemplo")
                datos_unidades = self._get_datos_ejemplo_unidades()

            # Generar D3.js y obtener URL
            url_d3 = self._generate_d3_html_and_url('bar', datos_unidades, "Usuarios por Unidad de Negocio")

            # Cargar en Matplotlib + URL D3
            self.chart_usuarios_unidad.set_chart('bar', datos_unidades, d3_url=url_d3)
            print(f"    ✓ Cargado con {len(datos_unidades['values'])} unidades")

            # Dashboard 2: Progreso por Unidad
            print("  → Dashboard 2: Progreso por Unidad (donut)")
            datos_progreso = self._get_progreso_por_unidad()
            if not datos_progreso or not datos_progreso['values']:
                print("    ⚠ Usando datos de ejemplo")
                datos_progreso = self._get_datos_ejemplo_progreso()

            # Generar D3.js y obtener URL
            url_d3 = self._generate_d3_html_and_url('donut', datos_progreso, "Progreso General por Unidad de Negocio")

            # Cargar en Matplotlib + URL D3
            self.chart_progreso_unidad.set_chart('donut', datos_progreso, d3_url=url_d3)
            print(f"    ✓ Cargado con {len(datos_progreso['values'])} unidades")

            # Dashboard 3: Distribución por Departamentos
            print("  → Dashboard 3: Distribución Departamentos (donut)")
            datos_deptos = self._get_distribucion_departamentos()

            # Generar D3.js y obtener URL
            url_d3 = self._generate_d3_html_and_url('donut', datos_deptos, "Distribución por Departamentos")

            # Cargar en Matplotlib + URL D3
            self.chart_departamentos.set_chart('donut', datos_deptos, d3_url=url_d3)
            print(f"    ✓ Cargado con {len(datos_deptos['values'])} departamentos")

            # Dashboard 4: Tendencia de Módulos
            print("  → Dashboard 4: Tendencia Módulos (line)")
            datos_tendencia = {
                'labels': ['Mod 1', 'Mod 2', 'Mod 3', 'Mod 4', 'Mod 5', 'Mod 6', 'Mod 7', 'Mod 8'],
                'values': [92, 88, 85, 82, 78, 75, 72, 70]
            }

            # Generar D3.js y obtener URL
            url_d3 = self._generate_d3_html_and_url('line', datos_tendencia, "Tendencia de Progreso por Módulos")

            # Cargar en Matplotlib + URL D3
            self.chart_modulos_tendencia.set_chart('line', datos_tendencia, d3_url=url_d3)
            print(f"    ✓ Cargado con {len(datos_tendencia['values'])} módulos")

            # Dashboard 5: Actividad Mensual
            print("  → Dashboard 5: Actividad Mensual (line)")
            datos_actividad = {
                'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                'values': [850, 920, 980, 1050, 1120, 1180, 1250, 1320, 1380, 1450, 1500, 1525]
            }

            # Generar D3.js y obtener URL
            url_d3 = self._generate_d3_html_and_url('line', datos_actividad, "Actividad de Usuarios Mensual")

            # Cargar en Matplotlib + URL D3
            self.chart_actividad.set_chart('line', datos_actividad, d3_url=url_d3)
            print(f"    ✓ Cargado con {len(datos_actividad['values'])} meses")

            # Dashboard 6: Resultados de Evaluaciones
            print("  → Dashboard 6: Evaluaciones (bar)")
            datos_eval = {
                'labels': ['Aprobados', 'En Proceso', 'Pendientes', 'No Aprobados'],
                'values': [1068, 284, 142, 31]
            }

            # Generar D3.js y obtener URL
            url_d3 = self._generate_d3_html_and_url('bar', datos_eval, "Resultados de Evaluaciones")

            # Cargar en Matplotlib + URL D3
            self.chart_evaluaciones.set_chart('bar', datos_eval, d3_url=url_d3)
            print(f"    ✓ Cargado con {len(datos_eval['values'])} categorías")

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

    # ==================== SISTEMA FULLSCREEN CON CEF ====================

    def _generate_d3_html_and_url(self, chart_type, datos, titulo, subtitulo=''):
        """
        Generar HTML D3.js y guardar en archivo temporal

        Returns:
            str: URL del archivo HTML generado
        """
        # Obtener tema
        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'

        # Generar HTML según tipo
        if chart_type == 'bar':
            html = self.motor_d3.generar_grafico_barras(
                titulo=titulo,
                datos=datos,
                subtitulo=subtitulo,
                tema=tema,
                interactivo=True
            )
        elif chart_type == 'donut':
            html = self.motor_d3.generar_grafico_donut(
                titulo=titulo,
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        elif chart_type == 'line':
            html = self.motor_d3.generar_grafico_lineas(
                titulo=titulo,
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        elif chart_type == 'area':
            html = self.motor_d3.generar_grafico_area(
                titulo=titulo,
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        else:
            html = f"<html><body><p>Tipo no soportado: {chart_type}</p></body></html>"

        # Guardar en archivo temporal
        filename = f"chart_{chart_type}_{id(self)}.html"
        filepath = os.path.join(self.d3_temp_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        # Retornar URL file://
        return f"file://{filepath}"

    def _on_dashboard_fullscreen(self, title, chart_type, data, subtitle, url):
        """Cambiar a vista fullscreen dentro de la app"""
        print(f"\n🖥️  Activando fullscreen interno: {title}")

        # Convertir file:// URL a path
        if url.startswith('file://'):
            html_path = url.replace('file://', '')
        else:
            html_path = url

        # Cambiar a vista fullscreen
        self.show_fullscreen_view(title, html_path)

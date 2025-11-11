"""
Panel de Dashboards Gerenciales - HUTCHISON PORTS (CON DATOS ESTÁTICOS)
Sistema de navegación: Grid view ↔ Modal Fullscreen con animación
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.navigation.boton_pestana import CustomTabView
from src.interfaces.ui.views.components.charts.interactive_chart_card import InteractiveChartCard
from src.interfaces.ui.views.components.charts.modal_fullscreen_chart import ModalFullscreenChart
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS


# ============================================
# DATOS ESTÁTICOS PARA DASHBOARDS
# ============================================

# Dashboard 1: Avance por Módulo - CCI
AVANCE_CCI_DATA = {
    'labels': ['Mod 1\nFilosofía', 'Mod 2\nSostenibilidad', 'Mod 3\nOperaciones', 'Mod 4\nRel. Laborales',
               'Mod 5\nSeguridad', 'Mod 6\nCiberseguridad', 'Mod 7\nSalud Laboral', 'Mod 8\nRRHH'],
    'values': [95, 92, 88, 85, 82, 78, 75, 70]
}

# Dashboard 2: Avance por Módulo - ECV/EIT
AVANCE_ECV_EIT_DATA = {
    'labels': ['Mod 1\nFilosofía', 'Mod 2\nSostenibilidad', 'Mod 3\nOperaciones', 'Mod 4\nRel. Laborales',
               'Mod 5\nSeguridad', 'Mod 6\nCiberseguridad', 'Mod 7\nSalud Laboral', 'Mod 8\nRRHH'],
    'values': [90, 87, 84, 80, 77, 73, 70, 65]
}

# Dashboard 3: Población por Unidad de Negocio
POBLACION_UN_DATA = {
    'labels': ['CCI', 'ECV', 'EIT', 'HPML', 'HPMX', 'ICAVE', 'LCTM', 'LCT TILH', 'TIMSA', 'TNG', 'CORPORATIVO'],
    'values': [145, 178, 223, 156, 195, 134, 189, 167, 145, 178, 95]
}

# Dashboard 4: Comportamiento Jerárquico - Resumen
COMPORTAMIENTO_JERARQUICO_RESUMEN = {
    'labels': ['Directores\ny Alta Gerencia', 'Gerentes\nMedios', 'Supervisores\ny Coordinadores',
               'Analistas\ny Especialistas', 'Personal\nOperativo'],
    'values': [98, 92, 85, 78, 70]
}

# Dashboard 5: Comportamiento Generacional
COMPORTAMIENTO_GENERACIONAL = {
    'labels': ['Baby Boomers\n(1946-1964)', 'Gen X\n(1965-1980)', 'Millennials\n(1981-1996)',
               'Gen Z\n(1997-2012)', 'Gen Alpha\n(2013+)'],
    'values': [88, 92, 85, 78, 65]
}

# Dashboard 6: Top 10 Posiciones con Mejor Avance
TOP_10_POSICIONES = {
    'labels': ['Director\nGeneral', 'Gerente\nOperaciones', 'Coordinador\nLogística', 'Jefe\nSeguridad',
               'Supervisor\nPatio', 'Analista\nFinanzas', 'Especialista\nIT', 'Jefe\nRRHH',
               'Coordinador\nCalidad', 'Supervisor\nMantenimiento'],
    'values': [98, 95, 93, 91, 89, 87, 85, 83, 81, 79]
}


class DashboardsGerencialesPanel(ctk.CTkFrame):
    """
    Panel de Control - SMART REPORTS INSTITUTO HUTCHISON PORTS

    Diseño:
    - Tab "General": Información general del instituto (cartas informativas)
    - Tab "Dashboards Gerenciales": 6 gráficos interactivos con datos estáticos
    """

    def __init__(self, parent, db_connection=None, usuario_actual=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        print("🚀 Inicializando DashboardsGerencialesPanel (DATOS ESTÁTICOS)...")

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection
        self.usuario_actual = usuario_actual or {"nombre": "Admin"}

        try:
            # Tabs de navegación
            print("  → Creando tabs...")
            self.tab_view = CustomTabView(self)
            self.tab_view.pack(fill='both', expand=True, padx=20, pady=(0, 20))

            # Crear pestañas
            print("  → Agregando pestañas...")
            self.tab_general = self.tab_view.add("General", "📊")
            self.tab_gerencial = self.tab_view.add("Dashboard", "📈")

            # Crear contenido
            print("  → Creando contenido de tabs...")
            self._create_general_tab()
            self._create_gerencial_tab()

            # Cargar datos estáticos
            print("  → Programando carga de datos estáticos...")
            self.after(500, self._load_static_data)

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
            value="1,805",
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
            value="82.5%",
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

        # === FILA 1: Avance por Módulo CCI y ECV/EIT ===
        row1 = ctk.CTkFrame(container, fg_color='transparent')
        row1.pack(fill='x', pady=(0, 20))
        row1.columnconfigure((0, 1), weight=1)

        # Dashboard 1: Avance CCI
        print("    → Creando dashboard Avance CCI...")
        self.chart_avance_cci = InteractiveChartCard(
            row1,
            title="Avance por Módulo - CCI",
            width=550,
            height=450,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_avance_cci.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='nsew')

        # Dashboard 2: Avance ECV/EIT
        print("    → Creando dashboard Avance ECV/EIT...")
        self.chart_avance_ecv = InteractiveChartCard(
            row1,
            title="Avance por Módulo - ECV/EIT",
            width=550,
            height=450,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_avance_ecv.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='nsew')

        # === FILA 2: Población UN y Comportamiento Jerárquico ===
        row2 = ctk.CTkFrame(container, fg_color='transparent')
        row2.pack(fill='x', pady=(0, 20))
        row2.columnconfigure(0, weight=6)  # 60%
        row2.columnconfigure(1, weight=4)  # 40%

        # Dashboard 3: Población por Unidad de Negocio
        print("    → Creando dashboard Población UN...")
        self.chart_poblacion_un = InteractiveChartCard(
            row2,
            title="Población por Unidad de Negocio",
            width=650,
            height=400,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_poblacion_un.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='nsew')

        # Dashboard 4: Comportamiento Jerárquico
        print("    → Creando dashboard Comportamiento Jerárquico...")
        self.chart_jerarquico = InteractiveChartCard(
            row2,
            title="Comportamiento Jerárquico",
            width=450,
            height=400,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_jerarquico.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='nsew')

        # === FILA 3: Generacional y Top 10 Posiciones ===
        row3 = ctk.CTkFrame(container, fg_color='transparent')
        row3.pack(fill='x', pady=(0, 20))
        row3.columnconfigure((0, 1), weight=1)

        # Dashboard 5: Comportamiento Generacional
        print("    → Creando dashboard Comportamiento Generacional...")
        self.chart_generacional = InteractiveChartCard(
            row3,
            title="Comportamiento Generacional",
            width=500,
            height=400,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_generacional.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 6: Top 10 Posiciones
        print("    → Creando dashboard Top 10 Posiciones...")
        self.chart_top_posiciones = InteractiveChartCard(
            row3,
            title="Top 10 Posiciones con Mejor Avance",
            width=500,
            height=400,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_top_posiciones.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

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

        # Container para el gráfico ampliado
        self.fullscreen_chart_container = ctk.CTkFrame(
            self.fullscreen_frame,
            fg_color='transparent'
        )
        self.fullscreen_chart_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Crear InteractiveChartCard grande para fullscreen
        self.fullscreen_chart = InteractiveChartCard(
            self.fullscreen_chart_container,
            title="",
            width=1200,
            height=700
        )
        self.fullscreen_chart.pack(fill='both', expand=True)

    def show_grid_view(self):
        """Mostrar vista grid (ocultar fullscreen)"""
        print("📊 Mostrando vista GRID")
        self.fullscreen_frame.pack_forget()
        self.grid_frame.pack(fill='both', expand=True, padx=10, pady=10)

    def _show_fullscreen_chart(self, chart):
        """
        Mostrar un gráfico en modo fullscreen usando MODAL con animación

        Args:
            chart: InteractiveChartCard a ampliar
        """
        print(f"🔍 Ampliando gráfico en MODAL: {chart.title_text}")

        # Crear y mostrar modal fullscreen con animación
        if chart.chart_data and chart.chart_type:
            modal = ModalFullscreenChart(
                parent=self,
                title=chart.title_text,
                chart_type=chart.chart_type,
                chart_data={
                    'labels': chart.chart_data['labels'].copy(),
                    'values': chart.chart_data['values'].copy()
                }
            )

            # Mantener foco en el modal
            modal.focus_force()
            modal.grab_set()

            print(f"  ✅ Modal fullscreen creado con animación deslizante")

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

    def _load_static_data(self):
        """Cargar datos estáticos en los dashboards"""
        print("\n" + "="*70)
        print("📊 CARGANDO DATOS ESTÁTICOS - HUTCHISON PORTS INSTITUTO")
        print("="*70)

        try:
            print("\n[1/6] 📈 Dashboard 1: Avance por Módulo - CCI")
            self.chart_avance_cci.set_chart('bar', AVANCE_CCI_DATA)
            print(f"  ✓ Cargado con {len(AVANCE_CCI_DATA['values'])} módulos")

            print("\n[2/6] 📈 Dashboard 2: Avance por Módulo - ECV/EIT")
            self.chart_avance_ecv.set_chart('line', AVANCE_ECV_EIT_DATA)
            print(f"  ✓ Cargado con {len(AVANCE_ECV_EIT_DATA['values'])} módulos")

            print("\n[3/6] 📊 Dashboard 3: Población por Unidad de Negocio")
            self.chart_poblacion_un.set_chart('bar', POBLACION_UN_DATA)
            print(f"  ✓ Cargado con {len(POBLACION_UN_DATA['values'])} unidades")

            print("\n[4/6] 🔵 Dashboard 4: Comportamiento Jerárquico")
            self.chart_jerarquico.set_chart('donut', COMPORTAMIENTO_JERARQUICO_RESUMEN)
            print(f"  ✓ Cargado con {len(COMPORTAMIENTO_JERARQUICO_RESUMEN['values'])} niveles")

            print("\n[5/6] 👥 Dashboard 5: Comportamiento Generacional")
            self.chart_generacional.set_chart('donut', COMPORTAMIENTO_GENERACIONAL)
            print(f"  ✓ Cargado con {len(COMPORTAMIENTO_GENERACIONAL['values'])} generaciones")

            print("\n[6/6] 🏆 Dashboard 6: Top 10 Posiciones con Mejor Avance")
            self.chart_top_posiciones.set_chart('bar', TOP_10_POSICIONES)
            print(f"  ✓ Cargado con {len(TOP_10_POSICIONES['values'])} posiciones")

            print("\n" + "="*70)
            print("✅ TODOS LOS DASHBOARDS CARGADOS EXITOSAMENTE")
            print("="*70 + "\n")

        except Exception as e:
            print(f"❌ Error cargando datos estáticos: {e}")
            import traceback
            traceback.print_exc()

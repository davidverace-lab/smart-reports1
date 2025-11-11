"""
╔════════════════════════════════════════════════════════════════════╗
║  PANEL DE CONTROL - HUTCHISON PORTS                               ║
║  Sistema de Dashboards Gerenciales Profesional                    ║
╚════════════════════════════════════════════════════════════════════╝

Diseño EXACTO según especificaciones del usuario:
✅ Tab "General" con métricas + gráficas principales (Panel de Control)
✅ Tab "Dashboards" con grid de 6 cards interactivas
✅ Sistema de expansión IN-PLACE (sin navegador)
✅ Gráficas matplotlib profesionales con gradientes navy blue
✅ Botón "Exportar Interactivo" cyan (#22d3ee)
✅ Modo claro/oscuro integrado
✅ Datos estáticos según diseño del usuario
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.navigation.boton_pestana import CustomTabView
from src.interfaces.ui.views.components.charts.interactive_chart_card import InteractiveChartCard
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS


# ═══════════════════════════════════════════════════════════════════
#  DATOS ESTÁTICOS - PANEL DE CONTROL EJECUTIVO
# ═══════════════════════════════════════════════════════════════════

# 📊 Gráfica 1: Usuarios por Unidad de Negocio (Barras Horizontales)
# Datos EXACTOS del diseño del usuario
USUARIOS_POR_UNIDAD_DATA = {
    'labels': ['LCMT', 'HPLM', 'ECV', 'TILH', 'CCI', 'TNG', 'HPMX', 'TIMSA', 'LCT', 'EIT', 'ICAVE'],
    'values': [3, 9, 23, 71, 76, 129, 145, 195, 226, 276, 372]
}

# 🍩 Gráfica 2: Progreso General por Unidad de Negocio (Dona)
# Con porcentajes exactos del diseño
PROGRESO_UNIDADES_DATA = {
    'labels': ['TNG - 100%', 'ICAVE - 82%', 'ECV - 75%', 'Container - 68%', 'HPMX - 62%'],
    'values': [100, 82, 75, 68, 62]
}

# 📈 Gráfica 3: Tendencia Semanal
TENDENCIA_SEMANAL_DATA = {
    'labels': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
    'values': [65, 72, 78, 85, 92, 88, 95]
}

# 📊 Gráfica 4: Top 5 Unidades de Mayor Progreso (Barras Verticales)
TOP_5_UNIDADES_DATA = {
    'labels': ['TNG', 'ICAVE', 'ECV', 'Container', 'HPMX'],
    'values': [100, 85, 75, 68, 62]
}

# 🎯 Gráfica 5: Cumplimiento de Objetivos (Dona)
CUMPLIMIENTO_OBJETIVOS_DATA = {
    'labels': ['Completados', 'En Progreso', 'Pendientes', 'Retrasados'],
    'values': [70, 20, 8, 2]
}

# 📉 Gráfica 6: Módulos con Menor Avance (Barras Horizontales)
MODULOS_MENOR_AVANCE_DATA = {
    'labels': ['Mod 8 - RRHH', 'Mod 7 - Salud', 'Mod 6 - Ciber', 'Mod 5 - Seguridad', 'Mod 4 - Rel. Lab.'],
    'values': [45, 52, 58, 65, 72]
}


class DashboardsGerencialesPanel(ctk.CTkFrame):
    """
    Panel de Control - HUTCHISON PORTS

    Diseño EXACTO del usuario:
    ┌─────────────────────────────────────────────────────────────┐
    │  Panel de Control                                           │
    │  ┌─────────────┐ ┌──────────────────────┐                 │
    │  │  General    │ │ Dashboards          │                  │
    │  │  (activo)   │ │ Gerenciales         │                  │
    │  └─────────────┘ └──────────────────────┘                 │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  TAB GENERAL:                                               │
    │  ┌──────┐  ┌─────────────────────┐  ┌───────────┐        │
    │  │ 👥  │  │ 📄 Módulo Actual    │  │ ✓ Tasa   │        │
    │  │1,525│  │ Módulo 8 - RRHH     │  │ 70.0%    │        │
    │  └──────┘  └─────────────────────┘  └───────────┘        │
    │                                                             │
    │  ┌────────────────────┐  ┌─────────────────────────┐      │
    │  │ Usuarios por UN    │  │ Progreso General por UN │      │
    │  │ (Barras Horiz.)    │  │ (Dona con leyenda)      │      │
    │  │ [Exportar]         │  │ [Exportar]              │      │
    │  └────────────────────┘  └─────────────────────────┘      │
    │                                                             │
    │  TAB DASHBOARDS:                                            │
    │  Grid 2x3 con 6 gráficas mini (cada una expandible)        │
    └─────────────────────────────────────────────────────────────┘
    """

    def __init__(self, parent, db_connection=None, usuario_actual=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        print("🚀 Inicializando Panel de Control - Dashboards Gerenciales...")

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection
        self.usuario_actual = usuario_actual or {"nombre": "Admin"}

        # Referencias a gráficas para fullscreen
        self.chart_usuarios_unidad = None
        self.chart_progreso_dona = None
        self.chart_tendencia = None
        self.chart_top5 = None
        self.chart_cumplimiento = None
        self.chart_menor_avance = None

        # Referencias para grid
        self.chart_usuarios_unidad_grid = None
        self.chart_progreso_dona_grid = None

        try:
            self._create_tabs()
            self._create_general_tab()
            self._create_dashboards_tab()

            # Cargar datos después de 500ms
            self.after(500, self._load_all_data)

            print("✅ Panel de Control inicializado correctamente")

        except Exception as e:
            print(f"❌ Error inicializando panel: {e}")
            import traceback
            traceback.print_exc()

    def _create_tabs(self):
        """Crear sistema de tabs: General | Dashboards Gerenciales"""
        print("  → Creando tabs de navegación...")

        self.tab_view = CustomTabView(self)
        self.tab_view.pack(fill='both', expand=True, padx=20, pady=(10, 20))

        # Tab 1: General (Panel de Control con métricas + 2 gráficas grandes)
        self.tab_general = self.tab_view.add("General", "📊")

        # Tab 2: Dashboards Gerenciales (grid de 6 dashboards)
        self.tab_dashboards = self.tab_view.add("Dashboards Gerenciales", "📈")

    # ═══════════════════════════════════════════════════════════════
    #  TAB 1: GENERAL (Panel de Control Principal)
    # ═══════════════════════════════════════════════════════════════

    def _create_general_tab(self):
        """
        Crear Tab "General" con diseño EXACTO del usuario:

        ╔═══════════════════════════════════════════════════════════╗
        ║  Panel de Control                                         ║
        ╠═══════════════════════════════════════════════════════════╣
        ║  ┌─────────┐  ┌──────────────────────┐  ┌─────────────┐ ║
        ║  │ 👥      │  │ 📄 Módulo Actual     │  │ ✓ Tasa de  ║ ║
        ║  │ Total   │  │ Módulo 8 - RRHH      │  │ Completado ║ ║
        ║  │ 1,525   │  │                       │  │   70.0%    ║ ║
        ║  └─────────┘  └──────────────────────┘  └─────────────┘ ║
        ╠═══════════════════════════════════════════════════════════╣
        ║  ┌──────────────────────┐  ┌──────────────────────────┐ ║
        ║  │ Usuarios por Unidad  │  │ Progreso General por UN  ║ ║
        ║  │ [📥 Exportar]        │  │ [📥 Exportar]            ║ ║
        ║  │  ICAVE  ████████ 372 │  │      ╭──────╮            ║ ║
        ║  │  EIT    ███████ 276  │  │    ╱  TNG    ╲           ║ ║
        ║  │  LCT    ██████ 226   │  │   │   100%   │          ║ ║
        ║  │  ...                 │  │    ╲  387    ╱           ║ ║
        ║  └──────────────────────┘  │      ╰──────╯            ║ ║
        ║                             │  Leyenda: TNG-100%...    ║ ║
        ║                             └──────────────────────────┘ ║
        ╚═══════════════════════════════════════════════════════════╝
        """
        theme = self.theme_manager.get_current_theme()

        # Container principal con scroll
        container = ctk.CTkScrollableFrame(
            self.tab_general,
            fg_color='transparent'
        )
        container.pack(fill='both', expand=True, padx=10, pady=10)

        # ═══ SECCIÓN 1: TARJETAS DE MÉTRICAS (3 CARDS) ═══
        print("  → Creando tarjetas de métricas...")

        metrics_frame = ctk.CTkFrame(container, fg_color='transparent')
        metrics_frame.pack(fill='x', pady=(0, 20))
        metrics_frame.columnconfigure((0, 1, 2), weight=1)

        # Card 1: Total de Usuarios
        self._create_metric_card(
            metrics_frame,
            icon="👥",
            title="Total de Usuarios",
            value="1,525",
            subtitle="Usuarios activos en el sistema",
            color=HUTCHISON_COLORS['ports_sky_blue']
        ).grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Card 2: Módulo Actual (EXACTO del diseño)
        self._create_metric_card_modulo(
            metrics_frame,
            icon="📄",
            title="Módulo Actual",
            value="Módulo 8 - Procesos de\nRecursos Humanos",
            color=HUTCHISON_COLORS['aqua_green']
        ).grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Card 3: Tasa de Completado
        self._create_metric_card(
            metrics_frame,
            icon="✓",
            title="Tasa de Completado",
            value="70.0%",
            subtitle="Progreso general del instituto",
            color=HUTCHISON_COLORS['success']
        ).grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        # ═══ SECCIÓN 2: GRÁFICAS PRINCIPALES (2 GRANDES) ═══
        print("  → Creando gráficas principales...")

        charts_frame = ctk.CTkFrame(container, fg_color='transparent')
        charts_frame.pack(fill='both', expand=True, pady=(10, 0))
        charts_frame.columnconfigure(0, weight=6)  # 60% para barras horizontales
        charts_frame.columnconfigure(1, weight=4)  # 40% para dona

        # Gráfica 1: Usuarios por Unidad de Negocio (Barras Horizontales)
        # CON DATOS EXACTOS: LCMT(3), HPLM(9), ECV(23)... ICAVE(372)
        self.chart_usuarios_unidad = InteractiveChartCard(
            charts_frame,
            title="Usuarios por Unidad de Negocio",
            width=750,
            height=580,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_usuarios_unidad.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='nsew')

        # Gráfica 2: Progreso General por Unidad de Negocio (Dona)
        # CON LEYENDA: TNG-100%, ICAVE-82%, ECV-75%, Container-68%, HPMX-62%
        self.chart_progreso_dona = InteractiveChartCard(
            charts_frame,
            title="Progreso General por Unidad de Negocio\n(TNG 100% - 8 Módulos)",
            width=500,
            height=580,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_progreso_dona.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='nsew')

    # ═══════════════════════════════════════════════════════════════
    #  TAB 2: DASHBOARDS (Grid de 6 Tarjetas)
    # ═══════════════════════════════════════════════════════════════

    def _create_dashboards_tab(self):
        """
        Crear Tab "Dashboards Gerenciales" con grid 2x3:

        ╔═══════════════════════════════════════════════════════════╗
        ║  📊 Dashboards                                    [🔍] [⚙️]║
        ╠═══════════════════════════════════════════════════════════╣
        ║  ┌────────────┐  ┌────────────┐  ┌────────────┐         ║
        ║  │ 📊 Usuarios│  │ 🍩 Progreso│  │ 📈 Tendenc.│         ║
        ║  │   por UN   │  │   General  │  │   Semanal  │         ║
        ║  │ [preview]  │  │ [preview]  │  │ [preview]  │         ║
        ║  │ [↗Expandir]│  │ [↗Expandir]│  │ [↗Expandir]│         ║
        ║  └────────────┘  └────────────┘  └────────────┘         ║
        ║  ┌────────────┐  ┌────────────┐  ┌────────────┐         ║
        ║  │ 📊 Top 5   │  │ 🎯 Cumpli. │  │ 📉 Menor   │         ║
        ║  │  Unidades  │  │  Objetivos │  │   Avance   │         ║
        ║  │ [preview]  │  │ [preview]  │  │ [preview]  │         ║
        ║  │ [↗Expandir]│  │ [↗Expandir]│  │ [↗Expandir]│         ║
        ║  └────────────┘  └────────────┘  └────────────┘         ║
        ╚═══════════════════════════════════════════════════════════╝
        """
        theme = self.theme_manager.get_current_theme()

        # Container con scroll
        container = ctk.CTkScrollableFrame(
            self.tab_dashboards,
            fg_color='transparent'
        )
        container.pack(fill='both', expand=True, padx=10, pady=10)

        # Título de sección
        section_title = ctk.CTkLabel(
            container,
            text="📊 Dashboards Interactivos - Sistema Ejecutivo",
            font=('Segoe UI', 24, 'bold'),
            text_color=HUTCHISON_COLORS['ports_sea_blue']
        )
        section_title.pack(anchor='w', padx=20, pady=(10, 20))

        # Grid Frame para 6 dashboards (2 filas x 3 columnas)
        grid_frame = ctk.CTkFrame(container, fg_color='transparent')
        grid_frame.pack(fill='both', expand=True, padx=10, pady=10)
        grid_frame.columnconfigure((0, 1, 2), weight=1)
        grid_frame.rowconfigure((0, 1), weight=1)

        # ═══ FILA 1 ═══

        # Dashboard 1: Usuarios por Unidad
        self.chart_usuarios_unidad_grid = InteractiveChartCard(
            grid_frame,
            title="📊 Usuarios por Unidad",
            width=400,
            height=370,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_usuarios_unidad_grid.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 2: Progreso General
        self.chart_progreso_dona_grid = InteractiveChartCard(
            grid_frame,
            title="🍩 Progreso General por Unidad",
            width=400,
            height=370,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_progreso_dona_grid.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Dashboard 3: Tendencia Semanal
        self.chart_tendencia = InteractiveChartCard(
            grid_frame,
            title="📈 Tendencia Semanal",
            width=400,
            height=370,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_tendencia.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        # ═══ FILA 2 ═══

        # Dashboard 4: Top 5 Unidades
        self.chart_top5 = InteractiveChartCard(
            grid_frame,
            title="📊 Top 5 Unidades de Mayor Progreso",
            width=400,
            height=370,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_top5.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 5: Cumplimiento de Objetivos
        self.chart_cumplimiento = InteractiveChartCard(
            grid_frame,
            title="🎯 Cumplimiento de Objetivos",
            width=400,
            height=370,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_cumplimiento.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        # Dashboard 6: Módulos con Menor Avance
        self.chart_menor_avance = InteractiveChartCard(
            grid_frame,
            title="📉 Módulos con Menor Avance",
            width=400,
            height=370,
            on_fullscreen=self._show_fullscreen_chart
        )
        self.chart_menor_avance.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

    # ═══════════════════════════════════════════════════════════════
    #  COMPONENTES AUXILIARES
    # ═══════════════════════════════════════════════════════════════

    def _create_metric_card(self, parent, icon, title, value, subtitle, color):
        """
        Crear tarjeta de métrica estándar con diseño corporativo

        ┌─────────────────┐
        │       👥        │
        │     1,525       │
        │ Total Usuarios  │
        │  (activos)      │
        └─────────────────┘
        """
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=16,
            border_width=2,
            border_color=color
        )

        inner = ctk.CTkFrame(card, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=25, pady=25)

        # Ícono grande
        icon_label = ctk.CTkLabel(
            inner,
            text=icon,
            font=('Segoe UI', 44),
            text_color=color
        )
        icon_label.pack(anchor='center', pady=(0, 15))

        # Valor principal (grande y destacado)
        value_label = ctk.CTkLabel(
            inner,
            text=value,
            font=('Segoe UI', 38, 'bold'),
            text_color=theme['text']
        )
        value_label.pack(anchor='center', pady=(0, 8))

        # Título
        title_label = ctk.CTkLabel(
            inner,
            text=title,
            font=('Segoe UI', 14, 'bold'),
            text_color=theme['text_secondary']
        )
        title_label.pack(anchor='center', pady=(0, 5))

        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            inner,
            text=subtitle,
            font=('Segoe UI', 11),
            text_color=theme['text_tertiary'],
            wraplength=200
        )
        subtitle_label.pack(anchor='center')

        return card

    def _create_metric_card_modulo(self, parent, icon, title, value, color):
        """
        Crear tarjeta ESPECIAL para "Módulo Actual" (más ancha)

        ┌─────────────────────────────┐
        │           📄                │
        │     Módulo Actual           │
        │                             │
        │  Módulo 8 - Procesos de     │
        │  Recursos Humanos           │
        └─────────────────────────────┘
        """
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=16,
            border_width=2,
            border_color=color
        )

        inner = ctk.CTkFrame(card, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=25, pady=25)

        # Ícono
        icon_label = ctk.CTkLabel(
            inner,
            text=icon,
            font=('Segoe UI', 44),
            text_color=color
        )
        icon_label.pack(anchor='center', pady=(0, 10))

        # Título
        title_label = ctk.CTkLabel(
            inner,
            text=title,
            font=('Segoe UI', 14, 'bold'),
            text_color=theme['text_secondary']
        )
        title_label.pack(anchor='center', pady=(0, 15))

        # Valor (módulo actual con saltos de línea)
        value_label = ctk.CTkLabel(
            inner,
            text=value,
            font=('Segoe UI', 16, 'bold'),
            text_color=theme['text'],
            justify='center'
        )
        value_label.pack(anchor='center')

        return card

    def _show_fullscreen_chart(self, chart):
        """
        Mostrar gráfica en modo fullscreen (IN-PLACE con modal)

        Comportamiento según diseño del usuario:
        ╔═══════════════════════════════════════════════════════════╗
        ║  [← Regresar]         📊 Usuarios por Unidad        [⋮]  ║
        ╠═══════════════════════════════════════════════════════════╣
        ║  📥 Exportar    📧 Compartir    🖨️ Imprimir              ║
        ║                                                           ║
        ║  ┌─ Ordenar: ──────────────────────────────────────────┐ ║
        ║  │  [🔼 Ascendente]  [🔽 Descendente]  [↻ Restablecer]│ ║
        ║  └────────────────────────────────────────────────────┘ ║
        ║                                                           ║
        ║  [GRÁFICA GIGANTE INTERACTIVA]                           ║
        ║                                                           ║
        ║  📊 Total: 1,525 | 📈 Promedio: 138.6 | ⭐ Mayor: ICAVE  ║
        ╚═══════════════════════════════════════════════════════════╝
        """
        print(f"🔍 Expandiendo gráfica: {chart.title_text}")

        # Importar modal fullscreen
        from src.interfaces.ui.views.components.charts.modal_fullscreen_chart import ModalFullscreenChart

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
            modal.focus_force()
            modal.grab_set()

            print(f"  ✅ Modal fullscreen creado con controles completos")

    # ═══════════════════════════════════════════════════════════════
    #  CARGA DE DATOS
    # ═══════════════════════════════════════════════════════════════

    def _load_all_data(self):
        """Cargar todos los datos estáticos en las gráficas"""
        print("\n" + "═"*70)
        print("📊 CARGANDO DATOS - PANEL DE CONTROL EJECUTIVO")
        print("═"*70)

        try:
            # ═══ TAB GENERAL ═══
            print("\n[TAB GENERAL - Panel de Control]")

            print("  [1/2] 📊 Usuarios por Unidad de Negocio (Barras Horizontales)")
            print("        Datos: LCMT(3), HPLM(9), ECV(23)... ICAVE(372)")
            self.chart_usuarios_unidad.set_chart('bar', USUARIOS_POR_UNIDAD_DATA)
            print(f"        ✓ {len(USUARIOS_POR_UNIDAD_DATA['values'])} unidades cargadas")

            print("  [2/2] 🍩 Progreso General por Unidad (Dona)")
            print("        Datos: TNG-100%, ICAVE-82%, ECV-75%, Container-68%, HPMX-62%")
            self.chart_progreso_dona.set_chart('donut', PROGRESO_UNIDADES_DATA)
            print(f"        ✓ {len(PROGRESO_UNIDADES_DATA['values'])} unidades cargadas")

            # ═══ TAB DASHBOARDS ═══
            print("\n[TAB DASHBOARDS - GRID 2x3]")

            print("  [1/6] 📊 Usuarios por Unidad (Grid)")
            self.chart_usuarios_unidad_grid.set_chart('bar', USUARIOS_POR_UNIDAD_DATA)

            print("  [2/6] 🍩 Progreso General (Grid)")
            self.chart_progreso_dona_grid.set_chart('donut', PROGRESO_UNIDADES_DATA)

            print("  [3/6] 📈 Tendencia Semanal")
            self.chart_tendencia.set_chart('line', TENDENCIA_SEMANAL_DATA)

            print("  [4/6] 📊 Top 5 Unidades")
            self.chart_top5.set_chart('bar', TOP_5_UNIDADES_DATA)

            print("  [5/6] 🎯 Cumplimiento de Objetivos")
            self.chart_cumplimiento.set_chart('donut', CUMPLIMIENTO_OBJETIVOS_DATA)

            print("  [6/6] 📉 Módulos con Menor Avance")
            self.chart_menor_avance.set_chart('bar', MODULOS_MENOR_AVANCE_DATA)

            print("\n" + "═"*70)
            print("✅ PANEL DE CONTROL COMPLETAMENTE CARGADO")
            print("   • Tab General: 3 métricas + 2 gráficas grandes")
            print("   • Tab Dashboards: 6 gráficas en grid 2x3")
            print("   • Datos exactos según diseño del usuario")
            print("   • Colores navy blue corporativos (#002E6D → #009BDE)")
            print("   • Botón 'Exportar Interactivo' cyan (#22d3ee)")
            print("   • Sistema de expansión in-place funcional")
            print("═"*70 + "\n")

        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            import traceback
            traceback.print_exc()


# ═══════════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA PARA TESTING
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import customtkinter as ctk
    from config.gestor_temas import initialize_theme_manager

    # Configurar tema
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Crear ventana
    root = ctk.CTk()
    root.title("Panel de Control - HUTCHISON PORTS")
    root.geometry("1600x950")

    # Inicializar gestor de temas
    initialize_theme_manager(root)

    # Crear panel
    panel = DashboardsGerencialesPanel(root)
    panel.pack(fill='both', expand=True)

    root.mainloop()

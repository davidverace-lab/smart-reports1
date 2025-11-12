"""
╔════════════════════════════════════════════════════════════════════╗
║  PANEL DE CONTROL EJECUTIVO - HUTCHISON PORTS                     ║
║  Sistema de Dashboards Gerenciales Profesional                    ║
╚════════════════════════════════════════════════════════════════════╝

Diseño EXACTO según especificaciones:
✅ Tab "General" con métricas + gráficas principales
✅ Tab "Dashboards" con grid de 6 cards interactivas
✅ Sistema de expansión IN-PLACE (sin navegador)
✅ Gráficas matplotlib profesionales con gradientes navy blue
✅ Modo claro/oscuro integrado
"""
import customtkinter as ctk
from src.main.python.ui.widgets.navigation.boton_pestana import CustomTabView
from src.main.python.ui.widgets.charts.grafica_expandible import GraficaExpandible
from src.main.res.config.gestor_temas import get_theme_manager
from src.main.res.config.themes import HUTCHISON_COLORS


# ═══════════════════════════════════════════════════════════════════
#  DATOS ESTÁTICOS - PANEL DE CONTROL EJECUTIVO
# ═══════════════════════════════════════════════════════════════════

# 📊 Gráfica 1: Usuarios por Unidad de Negocio (Barras Horizontales)
USUARIOS_POR_UNIDAD_DATA = {
    'labels': ['LCMT', 'HPLM', 'ECV', 'TILH', 'CCI', 'TNG', 'HPMX', 'TIMSA', 'LCT', 'EIT', 'ICAVE'],
    'values': [3, 9, 23, 71, 76, 129, 145, 195, 226, 276, 372]
}

# 🍩 Gráfica 2: Progreso General por Unidad de Negocio (Dona)
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


class PanelControlEjecutivo(ctk.CTkFrame):
    """
    Panel de Control Ejecutivo - HUTCHISON PORTS

    Estructura:
    ┌─────────────────────────────────────────────────────────────┐
    │  Panel de Control                                           │
    │  ┌─────────────┐ ┌──────────────────────┐                 │
    │  │  General    │ │ Dashboards          │                  │
    │  │  (activo)   │ │ Gerenciales         │                  │
    │  └─────────────┘ └──────────────────────┘                 │
    ├─────────────────────────────────────────────────────────────┤
    │  [Vista General: 3 métricas + 2 gráficas grandes]          │
    │  [Vista Dashboards: Grid 2x3 con 6 gráficas]               │
    └─────────────────────────────────────────────────────────────┘
    """

    def __init__(self, parent, db_connection=None, usuario_actual=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        print("🚀 Inicializando Panel de Control Ejecutivo...")

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

        # Estado de navegación
        self.fullscreen_chart = None  # Gráfica actualmente en fullscreen

        try:
            self._create_tabs()
            self._create_general_tab()
            self._create_dashboards_tab()

            # Cargar datos después de 500ms
            self.after(500, self._load_all_data)

            print("✅ Panel de Control Ejecutivo inicializado correctamente")

        except Exception as e:
            print(f"❌ Error inicializando panel: {e}")
            import traceback
            traceback.print_exc()

    def _create_tabs(self):
        """Crear sistema de tabs: General | Dashboards Gerenciales"""
        print("  → Creando tabs de navegación...")

        self.tab_view = CustomTabView(self)
        self.tab_view.pack(fill='both', expand=True, padx=20, pady=(10, 20))

        # Tab 1: General (métricas + gráficas principales)
        self.tab_general = self.tab_view.add("General", "📊")

        # Tab 2: Dashboards Gerenciales (grid de 6 dashboards)
        self.tab_dashboards = self.tab_view.add("Dashboards Gerenciales", "📈")

    # ═══════════════════════════════════════════════════════════════
    #  TAB 1: GENERAL (Panel de Control Principal)
    # ═══════════════════════════════════════════════════════════════

    def _create_general_tab(self):
        """
        Crear Tab "General" con diseño EXACTO:

        ┌───────────────────────────────────────────────────────────┐
        │  Panel de Control                                         │
        ├───────────────────────────────────────────────────────────┤
        │  ┌─────────┐  ┌──────────────────────┐  ┌─────────────┐ │
        │  │ 👥      │  │ 📄 Módulo Actual     │  │ ✓ Tasa de  │ │
        │  │ Total   │  │ Módulo 8 - RRHH      │  │ Completado │ │
        │  │ 1,525   │  │                       │  │   70.0%    │ │
        │  └─────────┘  └──────────────────────┘  └─────────────┘ │
        ├───────────────────────────────────────────────────────────┤
        │  ┌──────────────────────┐  ┌──────────────────────────┐ │
        │  │ Usuarios por Unidad  │  │ Progreso General por UN  │ │
        │  │ (Barras Horizontales)│  │ (Gráfica de Dona)        │ │
        │  │                      │  │                          │ │
        │  │  [Gráfica Grande]    │  │    [Gráfica Grande]      │ │
        │  │                      │  │                          │ │
        │  └──────────────────────┘  └──────────────────────────┘ │
        └───────────────────────────────────────────────────────────┘
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

        # Card 2: Módulo Actual
        self._create_metric_card(
            metrics_frame,
            icon="📄",
            title="Módulo Actual",
            value="Módulo 8",
            subtitle="Procesos de Recursos Humanos",
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
        charts_frame.columnconfigure(0, weight=6)  # 60% para barras
        charts_frame.columnconfigure(1, weight=4)  # 40% para dona

        # Gráfica 1: Usuarios por Unidad de Negocio (Barras Horizontales)
        self.chart_usuarios_unidad = GraficaExpandible(
            charts_frame,
            tipo='barras',
            titulo="📊 Usuarios por Unidad de Negocio",
            altura_compacta=550
        )
        self.chart_usuarios_unidad.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='nsew')

        # Gráfica 2: Progreso General por Unidad de Negocio (Dona)
        self.chart_progreso_dona = GraficaExpandible(
            charts_frame,
            tipo='dona',
            titulo="🍩 Progreso General por Unidad de Negocio (TNG 100% - 8 Módulos)",
            altura_compacta=550
        )
        self.chart_progreso_dona.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='nsew')

    # ═══════════════════════════════════════════════════════════════
    #  TAB 2: DASHBOARDS (Grid de 6 Tarjetas)
    # ═══════════════════════════════════════════════════════════════

    def _create_dashboards_tab(self):
        """
        Crear Tab "Dashboards Gerenciales" con grid 2x3:

        ┌──────────────────────────────────────────────────────┐
        │  ┌────────────┐  ┌────────────┐  ┌────────────┐    │
        │  │ 📊 Usuarios│  │ 🍩 Progreso│  │ 📈 Tendenc.│    │
        │  │   por UN   │  │   General  │  │   Semanal  │    │
        │  │ [preview]  │  │ [preview]  │  │ [preview]  │    │
        │  │ [Expandir] │  │ [Expandir] │  │ [Expandir] │    │
        │  └────────────┘  └────────────┘  └────────────┘    │
        │  ┌────────────┐  ┌────────────┐  ┌────────────┐    │
        │  │ 📊 Top 5   │  │ 🎯 Cumpli. │  │ 📉 Menor   │    │
        │  │  Unidades  │  │  Objetivos │  │   Avance   │    │
        │  │ [preview]  │  │ [preview]  │  │ [preview]  │    │
        │  │ [Expandir] │  │ [Expandir] │  │ [Expandir] │    │
        │  └────────────┘  └────────────┘  └────────────┘    │
        └──────────────────────────────────────────────────────┘
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
            font=('Segoe UI', 22, 'bold'),
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
        self.chart_usuarios_unidad_grid = GraficaExpandible(
            grid_frame,
            tipo='barras',
            titulo="📊 Usuarios por Unidad",
            altura_compacta=350
        )
        self.chart_usuarios_unidad_grid.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 2: Progreso General
        self.chart_progreso_dona_grid = GraficaExpandible(
            grid_frame,
            tipo='dona',
            titulo="🍩 Progreso General por Unidad",
            altura_compacta=350
        )
        self.chart_progreso_dona_grid.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Dashboard 3: Tendencia Semanal
        self.chart_tendencia = GraficaExpandible(
            grid_frame,
            tipo='linea',
            titulo="📈 Tendencia Semanal",
            altura_compacta=350
        )
        self.chart_tendencia.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        # ═══ FILA 2 ═══

        # Dashboard 4: Top 5 Unidades
        self.chart_top5 = GraficaExpandible(
            grid_frame,
            tipo='barras',
            titulo="📊 Top 5 Unidades de Mayor Progreso",
            altura_compacta=350
        )
        self.chart_top5.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 5: Cumplimiento de Objetivos
        self.chart_cumplimiento = GraficaExpandible(
            grid_frame,
            tipo='dona',
            titulo="🎯 Cumplimiento de Objetivos",
            altura_compacta=350
        )
        self.chart_cumplimiento.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        # Dashboard 6: Módulos con Menor Avance
        self.chart_menor_avance = GraficaExpandible(
            grid_frame,
            tipo='barras',
            titulo="📉 Módulos con Menor Avance",
            altura_compacta=350
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
            corner_radius=15,
            border_width=2,
            border_color=color
        )

        inner = ctk.CTkFrame(card, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=25, pady=25)

        # Ícono grande
        icon_label = ctk.CTkLabel(
            inner,
            text=icon,
            font=('Segoe UI', 42),
            text_color=color
        )
        icon_label.pack(anchor='center', pady=(0, 15))

        # Valor principal (grande y destacado)
        value_label = ctk.CTkLabel(
            inner,
            text=value,
            font=('Segoe UI', 36, 'bold'),
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

    def _show_fullscreen_chart(self, chart):
        """
        Mostrar gráfica en modo fullscreen (IN-PLACE, sin nueva ventana)

        Comportamiento:
        - Oculta el contenido del tab actual
        - Muestra la gráfica ampliada con controles
        - Botón "← Regresar" para volver
        """
        print(f"🔍 Expandiendo gráfica: {chart.title_text}")

        # TODO: Implementar vista fullscreen in-place
        # Por ahora, usamos el modal existente del sistema
        from src.main.python.ui.widgets.charts.modal_fullscreen_chart import ModalFullscreenChart

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
            print("\n[TAB GENERAL]")

            print("  [1/2] 📊 Usuarios por Unidad de Negocio (Barras Horizontales)")
            self.chart_usuarios_unidad.set_data(USUARIOS_POR_UNIDAD_DATA['labels'], USUARIOS_POR_UNIDAD_DATA['values'])
            print(f"        ✓ {len(USUARIOS_POR_UNIDAD_DATA['values'])} unidades cargadas")

            print("  [2/2] 🍩 Progreso General por Unidad (Dona)")
            self.chart_progreso_dona.set_data(PROGRESO_UNIDADES_DATA['labels'], PROGRESO_UNIDADES_DATA['values'])
            print(f"        ✓ {len(PROGRESO_UNIDADES_DATA['values'])} unidades cargadas")

            # ═══ TAB DASHBOARDS ═══
            print("\n[TAB DASHBOARDS - GRID 2x3]")

            print("  [1/6] 📊 Usuarios por Unidad (Grid)")
            self.chart_usuarios_unidad_grid.set_data(USUARIOS_POR_UNIDAD_DATA['labels'], USUARIOS_POR_UNIDAD_DATA['values'])

            print("  [2/6] 🍩 Progreso General (Grid)")
            self.chart_progreso_dona_grid.set_data(PROGRESO_UNIDADES_DATA['labels'], PROGRESO_UNIDADES_DATA['values'])

            print("  [3/6] 📈 Tendencia Semanal")
            self.chart_tendencia.set_data(TENDENCIA_SEMANAL_DATA['labels'], TENDENCIA_SEMANAL_DATA['values'])

            print("  [4/6] 📊 Top 5 Unidades")
            self.chart_top5.set_data(TOP_5_UNIDADES_DATA['labels'], TOP_5_UNIDADES_DATA['values'])

            print("  [5/6] 🎯 Cumplimiento de Objetivos")
            self.chart_cumplimiento.set_data(CUMPLIMIENTO_OBJETIVOS_DATA['labels'], CUMPLIMIENTO_OBJETIVOS_DATA['values'])

            print("  [6/6] 📉 Módulos con Menor Avance")
            self.chart_menor_avance.set_data(MODULOS_MENOR_AVANCE_DATA['labels'], MODULOS_MENOR_AVANCE_DATA['values'])

            print("\n" + "═"*70)
            print("✅ TODOS LOS DASHBOARDS CARGADOS EXITOSAMENTE")
            print("   • Tab General: 3 métricas + 2 gráficas grandes")
            print("   • Tab Dashboards: 6 gráficas en grid 2x3")
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

    # Configurar tema
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Crear ventana
    root = ctk.CTk()
    root.title("Panel de Control Ejecutivo - HUTCHISON PORTS")
    root.geometry("1400x900")

    # Crear panel
    panel = PanelControlEjecutivo(root)
    panel.pack(fill='both', expand=True)

    root.mainloop()

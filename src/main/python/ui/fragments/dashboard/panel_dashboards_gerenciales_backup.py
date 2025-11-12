"""
╔════════════════════════════════════════════════════════════════════╗
║  PANEL DE CONTROL - HUTCHISON PORTS                               ║
║  Sistema de Dashboards Gerenciales Profesional                    ║
║  CON NAVEGACIÓN IN-PLACE Y ANIMACIONES 60 FPS                     ║
╚════════════════════════════════════════════════════════════════════╝

✅ Navegación IN-PLACE (sin ventanas modales)
✅ Animaciones a 60 FPS (16ms por frame)
✅ Botón "← Regresar" como en Gestionar Usuario
✅ Transiciones suaves entre vistas
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

# 📊 Gráfica 4: Top 5 Unidades de Mayor Progreso
TOP_5_UNIDADES_DATA = {
    'labels': ['TNG', 'ICAVE', 'ECV', 'Container', 'HPMX'],
    'values': [100, 85, 75, 68, 62]
}

# 🎯 Gráfica 5: Cumplimiento de Objetivos
CUMPLIMIENTO_OBJETIVOS_DATA = {
    'labels': ['Completados', 'En Progreso', 'Pendientes', 'Retrasados'],
    'values': [70, 20, 8, 2]
}

# 📉 Gráfica 6: Módulos con Menor Avance
MODULOS_MENOR_AVANCE_DATA = {
    'labels': ['Mod 8 - RRHH', 'Mod 7 - Salud', 'Mod 6 - Ciber', 'Mod 5 - Seguridad', 'Mod 4 - Rel. Lab.'],
    'values': [45, 52, 58, 65, 72]
}


class DashboardsGerencialesPanel(ctk.CTkFrame):
    """
    Panel de Control - HUTCHISON PORTS

    Sistema de navegación IN-PLACE:
    ┌─────────────────────────────────────────────────────────────┐
    │  [General] [Dashboards]                                     │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  VISTA GRID (Normal):                                       │
    │  ┌────┐ ┌────┐ ┌────┐                                      │
    │  │ G1 │ │ G2 │ │ G3 │  [Click en ↗]                       │
    │  └────┘ └────┘ └────┘                                      │
    │                                                             │
    │  VISTA EXPANDIDA (Al hacer click en ↗):                    │
    │  ┌──────────────────────────────────────────────────────┐  │
    │  │ [← Regresar]    GRÁFICA GRANDE                      │  │
    │  │                                                      │  │
    │  │  [Gráfica Gigante con todos los controles]         │  │
    │  └──────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────┘
    """

    def __init__(self, parent, db_connection=None, usuario_actual=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        print("🚀 Inicializando Panel de Control con navegación IN-PLACE...")

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection
        self.usuario_actual = usuario_actual or {"nombre": "Admin"}

        # Referencias para vistas (GRID y EXPANDED)
        self.grid_view_frame = None
        self.expanded_view_frame = None

        # Referencias a gráficas
        self.chart_usuarios_unidad = None
        self.chart_progreso_dona = None
        self.chart_tendencia = None
        self.chart_top5 = None
        self.chart_cumplimiento = None
        self.chart_menor_avance = None

        # Gráfica expandida actual
        self.expanded_chart = None
        self.expanded_chart_card = None

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

        # Tab 1: General
        self.tab_general = self.tab_view.add("General", "📊")

        # Tab 2: Dashboards Gerenciales (con navegación interna)
        self.tab_dashboards = self.tab_view.add("Dashboards Gerenciales", "📈")

    # ═══════════════════════════════════════════════════════════════
    #  TAB 1: GENERAL
    # ═══════════════════════════════════════════════════════════════

    def _create_general_tab(self):
        """Crear Tab General con métricas + 2 gráficas"""
        theme = self.theme_manager.get_current_theme()

        container = ctk.CTkScrollableFrame(self.tab_general, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=10, pady=10)

        # ═══ MÉTRICAS ═══
        metrics_frame = ctk.CTkFrame(container, fg_color='transparent')
        metrics_frame.pack(fill='x', pady=(0, 20))
        metrics_frame.columnconfigure((0, 1, 2), weight=1)

        self._create_metric_card(
            metrics_frame, "👥", "Total de Usuarios", "1,525",
            "Usuarios activos en el sistema", HUTCHISON_COLORS['ports_sky_blue']
        ).grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self._create_metric_card_modulo(
            metrics_frame, "📄", "Módulo Actual",
            "Módulo 8 - Procesos de\nRecursos Humanos", HUTCHISON_COLORS['aqua_green']
        ).grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self._create_metric_card(
            metrics_frame, "✓", "Tasa de Completado", "70.0%",
            "Progreso general del instituto", HUTCHISON_COLORS['success']
        ).grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        # ═══ GRÁFICAS PRINCIPALES ═══
        charts_frame = ctk.CTkFrame(container, fg_color='transparent')
        charts_frame.pack(fill='both', expand=True, pady=(10, 0))
        charts_frame.columnconfigure(0, weight=6)
        charts_frame.columnconfigure(1, weight=4)

        self.chart_usuarios_unidad = GraficaExpandible(
            charts_frame,
            tipo='barras',
            titulo="Usuarios por Unidad de Negocio",
            altura_compacta=580
        )
        self.chart_usuarios_unidad.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='nsew')

        self.chart_progreso_dona = GraficaExpandible(
            charts_frame,
            tipo='dona',
            titulo="Progreso General por Unidad de Negocio\n(TNG 100% - 8 Módulos)",
            altura_compacta=580
        )
        self.chart_progreso_dona.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='nsew')

    # ═══════════════════════════════════════════════════════════════
    #  TAB 2: DASHBOARDS (con GRID VIEW y EXPANDED VIEW)
    # ═══════════════════════════════════════════════════════════════

    def _create_dashboards_tab(self):
        """
        Crear Tab Dashboards con navegación interna:
        - GRID VIEW: 6 dashboards en grid 2x3
        - EXPANDED VIEW: 1 dashboard gigante con botón "← Regresar"
        """
        # ═══ GRID VIEW (Vista inicial) ═══
        self.grid_view_frame = ctk.CTkScrollableFrame(
            self.tab_dashboards, fg_color='transparent'
        )

        # ═══ EXPANDED VIEW (Vista de gráfica grande) ═══
        self.expanded_view_frame = ctk.CTkFrame(
            self.tab_dashboards, fg_color='transparent'
        )

        # Crear contenido de ambas vistas
        self._create_grid_view()
        self._create_expanded_view()

        # Mostrar GRID VIEW por defecto
        self.grid_view_frame.pack(fill='both', expand=True, padx=10, pady=10)

    def _create_grid_view(self):
        """Crear vista GRID con 6 dashboards"""
        container = self.grid_view_frame
        theme = self.theme_manager.get_current_theme()

        # Título
        title = ctk.CTkLabel(
            container, text="📊 Dashboards Interactivos - Sistema Ejecutivo",
            font=('Segoe UI', 24, 'bold'), text_color=HUTCHISON_COLORS['ports_sea_blue']
        )
        title.pack(anchor='w', padx=20, pady=(10, 20))

        # Grid 2x3
        grid = ctk.CTkFrame(container, fg_color='transparent')
        grid.pack(fill='both', expand=True, padx=10, pady=10)
        grid.columnconfigure((0, 1, 2), weight=1)
        grid.rowconfigure((0, 1), weight=1)

        # Fila 1
        self.chart_usuarios_unidad_grid = GraficaExpandible(
            grid,
            tipo='barras',
            titulo="📊 Usuarios por Unidad",
            altura_compacta=370
        )
        self.chart_usuarios_unidad_grid.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.chart_progreso_dona_grid = GraficaExpandible(
            grid,
            tipo='dona',
            titulo="🍩 Progreso General por Unidad",
            altura_compacta=370
        )
        self.chart_progreso_dona_grid.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.chart_tendencia = GraficaExpandible(
            grid,
            tipo='linea',
            titulo="📈 Tendencia Semanal",
            altura_compacta=370
        )
        self.chart_tendencia.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        # Fila 2
        self.chart_top5 = GraficaExpandible(
            grid,
            tipo='barras',
            titulo="📊 Top 5 Unidades de Mayor Progreso",
            altura_compacta=370
        )
        self.chart_top5.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.chart_cumplimiento = GraficaExpandible(
            grid,
            tipo='dona',
            titulo="🎯 Cumplimiento de Objetivos",
            altura_compacta=370
        )
        self.chart_cumplimiento.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        self.chart_menor_avance = GraficaExpandible(
            grid,
            tipo='barras',
            titulo="📉 Módulos con Menor Avance",
            altura_compacta=370
        )
        self.chart_menor_avance.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

    def _create_expanded_view(self):
        """
        Crear vista EXPANDED con gráfica gigante + botón "← Regresar"

        ╔═══════════════════════════════════════════════════════════╗
        ║  [← Regresar]         GRÁFICA GRANDE             [⋮]     ║
        ╠═══════════════════════════════════════════════════════════╣
        ║  📥 Exportar    🔼 Ordenar    ↻ Reset                    ║
        ║                                                           ║
        ║  ┌────────────────────────────────────────────────────┐  ║
        ║  │                                                    │  ║
        ║  │        [GRÁFICA GIGANTE INTERACTIVA]             │  ║
        ║  │                                                    │  ║
        ║  └────────────────────────────────────────────────────┘  ║
        ║                                                           ║
        ║  📊 Total: 1,525 | 📈 Promedio: 138.6 | ⭐ Mayor: ICAVE  ║
        ╚═══════════════════════════════════════════════════════════╝
        """
        theme = self.theme_manager.get_current_theme()

        # ═══ HEADER CON BOTÓN "← REGRESAR" ═══
        header = ctk.CTkFrame(
            self.expanded_view_frame,
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            height=80
        )
        header.pack(fill='x', side='top')
        header.pack_propagate(False)

        # Botón "← Regresar" (MISMO ESTILO que Gestionar Usuario)
        back_btn = ctk.CTkButton(
            header,
            text='← Regresar',
            font=('Segoe UI', 16, 'bold'),
            fg_color='#003D8F',
            hover_color='#001a3d',
            text_color='white',
            corner_radius=10,
            width=150,
            height=50,
            command=self._show_grid_view  # ← NAVEGAR DE VUELTA
        )
        back_btn.pack(side='left', padx=30, pady=15)

        # Título de la gráfica expandida
        self.expanded_title_label = ctk.CTkLabel(
            header,
            text="",
            font=('Segoe UI', 26, 'bold'),
            text_color='white'
        )
        self.expanded_title_label.pack(side='left', expand=True, padx=30)

        # ═══ CONTAINER PARA GRÁFICA GIGANTE ═══
        self.expanded_chart_container = ctk.CTkFrame(
            self.expanded_view_frame,
            fg_color='transparent'
        )
        self.expanded_chart_container.pack(fill='both', expand=True, padx=30, pady=30)

        # ═══ FOOTER CON ESTADÍSTICAS ═══
        self.expanded_stats_frame = ctk.CTkFrame(
            self.expanded_view_frame,
            fg_color=theme['surface'],
            height=60,
            corner_radius=12
        )
        self.expanded_stats_frame.pack(fill='x', side='bottom', padx=30, pady=(0, 30))
        self.expanded_stats_frame.pack_propagate(False)

        self.expanded_stats_label = ctk.CTkLabel(
            self.expanded_stats_frame,
            text="",
            font=('Segoe UI', 14, 'bold'),
            text_color=theme['text']
        )
        self.expanded_stats_label.pack(expand=True, pady=15)

    # ═══════════════════════════════════════════════════════════════
    #  NAVEGACIÓN IN-PLACE (pack_forget + pack)
    # ═══════════════════════════════════════════════════════════════

    def _show_expanded_chart(self, chart):
        """
        NAVEGAR a vista expandida (IN-PLACE)

        Comportamiento:
        1. Ocultar grid_view_frame (pack_forget)
        2. Mostrar expanded_view_frame (pack)
        3. Renderizar gráfica gigante
        4. Animar entrada a 60 FPS
        """
        print(f"🔍 Expandiendo gráfica: {chart.title_text}")

        if not chart.chart_data or not chart.chart_type:
            print("⚠️ No hay datos para expandir")
            return

        # PASO 1: OCULTAR GRID VIEW
        self.grid_view_frame.pack_forget()

        # PASO 2: MOSTRAR EXPANDED VIEW
        self.expanded_view_frame.pack(fill='both', expand=True)

        # PASO 3: ACTUALIZAR TÍTULO
        self.expanded_title_label.configure(text=f"📊 {chart.title_text}")

        # PASO 4: LIMPIAR CONTAINER ANTERIOR
        for widget in self.expanded_chart_container.winfo_children():
            widget.destroy()

        # PASO 5: CREAR GRÁFICA GIGANTE
        self.expanded_chart_card = InteractiveChartCard(
            self.expanded_chart_container,
            title=chart.title_text,
            width=1400,
            height=700
        )
        self.expanded_chart_card.pack(fill='both', expand=True)

        # PASO 6: CARGAR DATOS
        self.expanded_chart_card.set_chart(
            chart.chart_type,
            {
                'labels': chart.chart_data['labels'].copy(),
                'values': chart.chart_data['values'].copy()
            }
        )

        # PASO 7: CALCULAR Y MOSTRAR ESTADÍSTICAS
        self._update_expanded_stats(chart.chart_data)

        # PASO 8: ANIMAR ENTRADA A 60 FPS
        self._animate_expanded_entrance()

        print(f"  ✅ Gráfica expandida mostrada (IN-PLACE)")

    def _show_grid_view(self):
        """
        NAVEGAR de vuelta a grid view (IN-PLACE)

        Comportamiento:
        1. Animar salida a 60 FPS (slide out hacia abajo)
        2. Ocultar expanded_view_frame (pack_forget)
        3. Mostrar grid_view_frame (pack)
        """
        print("📊 Regresando a vista GRID...")

        # PASO 1: ANIMAR SALIDA (slide out hacia abajo)
        frame = [0]

        def animate_exit():
            """Animar salida (60 FPS)"""
            if frame[0] < 12:  # 200ms / 16ms = ~12 frames
                progress = frame[0] / 12.0
                # Ease-in para salida rápida
                eased = progress ** 2

                # Mover hacia abajo (30px → 80px)
                current_pady_top = 30 + (50 * eased)
                self.expanded_chart_container.pack_configure(pady=(int(current_pady_top), 30))

                frame[0] += 1
                self.after(16, animate_exit)
            else:
                # Al terminar animación, cambiar de vista
                self._complete_grid_transition()

        # Iniciar animación de salida
        animate_exit()

    def _complete_grid_transition(self):
        """Completar transición a grid view (llamado después de animación)"""
        # OCULTAR EXPANDED VIEW
        self.expanded_view_frame.pack_forget()

        # MOSTRAR GRID VIEW
        self.grid_view_frame.pack(fill='both', expand=True, padx=10, pady=10)

        print("  ✅ Vista GRID restaurada con animación")

    def _animate_expanded_entrance(self):
        """
        Animar entrada de vista expandida a 60 FPS

        Animación:
        - Slide in desde abajo (Y: 50px → 0px)
        - Duración: 300ms (18 frames a 60 FPS)
        """
        # Preparar para animación (posición inicial desplazada)
        self.expanded_chart_container.pack_configure(pady=(80, 30))  # Offset inicial

        frame = [0]  # Usar lista para poder modificar en nested function

        def animate_frame():
            """Animar un frame (llamado cada 16ms para 60 FPS)"""
            if frame[0] < 18:  # 300ms / 16ms = ~18 frames
                # Calcular progreso (0.0 → 1.0 con easing)
                progress = frame[0] / 18.0
                # Easing suave (ease-out)
                eased = 1 - (1 - progress) ** 3

                # Interpolar padding (80px → 30px)
                current_pady_top = 80 - (50 * eased)
                self.expanded_chart_container.pack_configure(pady=(int(current_pady_top), 30))

                frame[0] += 1
                self.after(16, animate_frame)  # 60 FPS = 16ms por frame
            else:
                # Asegurar posición final exacta
                self.expanded_chart_container.pack_configure(pady=(30, 30))

        # Iniciar animación
        animate_frame()

    def _update_expanded_stats(self, data):
        """Actualizar estadísticas en footer de vista expandida"""
        if not data or 'values' not in data:
            return

        values = data['values']
        total = sum(values)
        promedio = total / len(values) if values else 0
        maximo = max(values) if values else 0
        max_index = values.index(maximo) if values else 0
        max_label = data['labels'][max_index] if max_index < len(data['labels']) else "N/A"

        stats_text = f"📊 Total: {int(total):,} | 📈 Promedio: {promedio:.1f} | ⭐ Mayor: {max_label} ({int(maximo)})"
        self.expanded_stats_label.configure(text=stats_text)

    # ═══════════════════════════════════════════════════════════════
    #  COMPONENTES AUXILIARES
    # ═══════════════════════════════════════════════════════════════

    def _create_metric_card(self, parent, icon, title, value, subtitle, color):
        """Crear tarjeta de métrica"""
        theme = self.theme_manager.get_current_theme()
        card = ctk.CTkFrame(parent, fg_color=theme['surface'], corner_radius=16, border_width=2, border_color=color)
        inner = ctk.CTkFrame(card, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=25, pady=25)

        ctk.CTkLabel(inner, text=icon, font=('Segoe UI', 44), text_color=color).pack(anchor='center', pady=(0, 15))
        ctk.CTkLabel(inner, text=value, font=('Segoe UI', 38, 'bold'), text_color=theme['text']).pack(anchor='center', pady=(0, 8))
        ctk.CTkLabel(inner, text=title, font=('Segoe UI', 14, 'bold'), text_color=theme['text_secondary']).pack(anchor='center', pady=(0, 5))
        ctk.CTkLabel(inner, text=subtitle, font=('Segoe UI', 11), text_color=theme['text_tertiary'], wraplength=200).pack(anchor='center')

        return card

    def _create_metric_card_modulo(self, parent, icon, title, value, color):
        """Crear tarjeta especial para Módulo Actual"""
        theme = self.theme_manager.get_current_theme()
        card = ctk.CTkFrame(parent, fg_color=theme['surface'], corner_radius=16, border_width=2, border_color=color)
        inner = ctk.CTkFrame(card, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=25, pady=25)

        ctk.CTkLabel(inner, text=icon, font=('Segoe UI', 44), text_color=color).pack(anchor='center', pady=(0, 10))
        ctk.CTkLabel(inner, text=title, font=('Segoe UI', 14, 'bold'), text_color=theme['text_secondary']).pack(anchor='center', pady=(0, 15))
        ctk.CTkLabel(inner, text=value, font=('Segoe UI', 16, 'bold'), text_color=theme['text'], justify='center').pack(anchor='center')

        return card

    # ═══════════════════════════════════════════════════════════════
    #  CARGA DE DATOS
    # ═══════════════════════════════════════════════════════════════

    def _load_all_data(self):
        """Cargar todos los datos estáticos"""
        print("\n" + "═"*70)
        print("📊 CARGANDO DATOS - PANEL DE CONTROL")
        print("═"*70)

        try:
            # TAB GENERAL
            print("\n[TAB GENERAL]")
            self.chart_usuarios_unidad.set_data(USUARIOS_POR_UNIDAD_DATA['labels'], USUARIOS_POR_UNIDAD_DATA['values'])
            print("  ✅ Usuarios por Unidad")
            self.chart_progreso_dona.set_data(PROGRESO_UNIDADES_DATA['labels'], PROGRESO_UNIDADES_DATA['values'])
            print("  ✅ Progreso por Unidad")

            # TAB DASHBOARDS - GRID
            print("\n[TAB DASHBOARDS - GRID 2x3]")
            self.chart_usuarios_unidad_grid.set_data(USUARIOS_POR_UNIDAD_DATA['labels'], USUARIOS_POR_UNIDAD_DATA['values'])
            self.chart_progreso_dona_grid.set_data(PROGRESO_UNIDADES_DATA['labels'], PROGRESO_UNIDADES_DATA['values'])
            self.chart_tendencia.set_data(TENDENCIA_SEMANAL_DATA['labels'], TENDENCIA_SEMANAL_DATA['values'])
            self.chart_top5.set_data(TOP_5_UNIDADES_DATA['labels'], TOP_5_UNIDADES_DATA['values'])
            self.chart_cumplimiento.set_data(CUMPLIMIENTO_OBJETIVOS_DATA['labels'], CUMPLIMIENTO_OBJETIVOS_DATA['values'])
            self.chart_menor_avance.set_data(MODULOS_MENOR_AVANCE_DATA['labels'], MODULOS_MENOR_AVANCE_DATA['values'])
            print("  ✅ Todos los dashboards cargados")

            print("\n" + "═"*70)
            print("✅ PANEL DE CONTROL COMPLETAMENTE CARGADO")
            print("   • Navegación IN-PLACE implementada")
            print("   • Botón '← Regresar' funcional")
            print("   • Animaciones 60 FPS preparadas")
            print("═"*70 + "\n")

        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            import traceback
            traceback.print_exc()


# ═══════════════════════════════════════════════════════════════════
#  TESTING
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import customtkinter as ctk

    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Panel de Control - HUTCHISON PORTS")
    root.geometry("1600x950")

    panel = DashboardsGerencialesPanel(root)
    panel.pack(fill='both', expand=True)

    root.mainloop()

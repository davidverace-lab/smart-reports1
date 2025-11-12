"""
Panel de Dashboards Gerenciales - HUTCHISON PORTS
Sistema de navegación: GRID ↔ EXPANDIDA (pantalla completa)
Dashboards gerenciales con gráficas interactivas expandibles
"""
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from src.main.python.ui.widgets.navigation.boton_pestana import CustomTabView
from src.main.res.config.gestor_temas import get_theme_manager
from src.main.res.config.themes import HUTCHISON_COLORS


# ═══════════════════════════════════════════════════════════════════
#  DATOS ESTÁTICOS - DASHBOARDS GERENCIALES
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
    Panel de Dashboards Gerenciales con navegación expandible

    Sistema de navegación:
    GRID VIEW → Todas las gráficas en miniatura
    EXPANDED VIEW → Una gráfica en pantalla completa con botón volver
    """

    def __init__(self, parent, db_connection=None, usuario_actual=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        print("🚀 Inicializando Panel de Dashboards Gerenciales con navegación expandible...")

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection
        self.usuario_actual = usuario_actual or {"nombre": "Admin"}

        # Datos de las gráficas
        self.datos_graficas = {
            'usuarios_unidad': USUARIOS_POR_UNIDAD_DATA,
            'progreso_unidades': PROGRESO_UNIDADES_DATA,
            'tendencia_semanal': TENDENCIA_SEMANAL_DATA,
            'top5_unidades': TOP_5_UNIDADES_DATA,
            'cumplimiento': CUMPLIMIENTO_OBJETIVOS_DATA,
            'menor_avance': MODULOS_MENOR_AVANCE_DATA
        }

        # Estado de navegación
        self.current_view = 'grid'  # 'grid' o 'expanded'
        self.current_chart_id = None
        self.current_chart_title = None
        self.current_chart_type = None
        self.current_chart_data = None

        # Referencias a vistas
        self.grid_view = None
        self.expanded_view = None
        self.expanded_chart_container = None
        self.expanded_title_label = None

        try:
            # Crear ambas vistas
            self._create_grid_view()
            self._create_expanded_view()

            # Mostrar grid por defecto
            self.show_grid_view()

            print("✅ Panel de Dashboards Gerenciales inicializado correctamente")

        except Exception as e:
            print(f"❌ Error inicializando panel: {e}")
            import traceback
            traceback.print_exc()

    # ==================== NAVEGACIÓN ENTRE VISTAS ====================

    def show_grid_view(self):
        """Mostrar vista GRID con todas las gráficas"""
        self.current_view = 'grid'
        if self.expanded_view:
            self.expanded_view.pack_forget()
        if self.grid_view:
            self.grid_view.pack(fill='both', expand=True)

    def _animate_expanded_view(self):
        """Animar la entrada de la vista expandida con efecto deslizante"""
        # Configuración de la animación
        duration_ms = 300  # 300ms duración total
        fps = 60  # 60 FPS
        frame_time = 1000 // fps  # ~16ms por frame
        total_frames = duration_ms // frame_time  # ~18 frames

        # Posición inicial y final
        start_offset = -0.08  # Comienza 8% arriba (fuera de vista)
        end_offset = 0.0  # Termina en posición normal

        current_frame = [0]  # Usar lista para poder modificar en función anidada

        def ease_out_cubic(t):
            """Función de easing suave (ease-out cubic)"""
            return 1 - pow(1 - t, 3)

        def animate_frame():
            if current_frame[0] <= total_frames:
                # Calcular progreso (0.0 a 1.0)
                progress = current_frame[0] / total_frames
                eased_progress = ease_out_cubic(progress)

                # Interpolar posición
                current_offset = start_offset + (end_offset - start_offset) * eased_progress

                # Aplicar posición usando place()
                self.expanded_view.place(relx=0, rely=current_offset, relwidth=1, relheight=1)

                # Siguiente frame
                current_frame[0] += 1
                self.after(frame_time, animate_frame)
            else:
                # Animación completa - cambiar a pack() para layout normal
                self.expanded_view.place_forget()
                self.expanded_view.pack(fill='both', expand=True)

        # Iniciar animación
        animate_frame()

    def show_expanded_view(self, chart_id, title, chart_type='barras'):
        """
        Mostrar vista EXPANDIDA con una gráfica en pantalla completa

        Args:
            chart_id: ID de la gráfica
            title: Título de la gráfica
            chart_type: 'barras', 'barras_h', 'dona', 'linea'
        """
        self.current_view = 'expanded'
        self.current_chart_id = chart_id
        self.current_chart_title = title
        self.current_chart_type = chart_type
        self.current_chart_data = self.datos_graficas.get(chart_id, {'labels': [], 'values': []})

        # Ocultar grid y mostrar expandida
        if self.grid_view:
            self.grid_view.pack_forget()

        # Renderizar gráfica expandida
        self._render_expanded_chart()

        if self.expanded_view:
            # Iniciar animación de entrada
            self._animate_expanded_view()

    # ==================== CREAR VISTA GRID ====================

    def _create_grid_view(self):
        """Crear vista GRID con tabs y gráficas miniatura"""
        theme = self.theme_manager.get_current_theme()

        self.grid_view = ctk.CTkFrame(self, fg_color='transparent')

        # Header
        header = ctk.CTkFrame(self.grid_view, fg_color='transparent', height=60)
        header.pack(fill='x', padx=20, pady=(15, 10))
        header.pack_propagate(False)

        # Título
        ctk.CTkLabel(
            header,
            text="📊 Dashboards Gerenciales",
            font=('Montserrat', 24, 'bold'),
            text_color=theme['text']
        ).pack(side='left')

        # Tabs
        self.tab_view = CustomTabView(self.grid_view)
        self.tab_view.pack(fill='both', expand=True, padx=10, pady=10)

        # Tab 1: General
        self.tab_general = self.tab_view.add("General", "📊")
        self._create_general_tab_content()

        # Tab 2: Dashboards
        self.tab_dashboards = self.tab_view.add("Dashboards Gerenciales", "📈")
        self._create_dashboards_tab_content()

    def _create_general_tab_content(self):
        """Crear contenido del tab General"""
        theme = self.theme_manager.get_current_theme()

        container = ctk.CTkScrollableFrame(self.tab_general, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=10, pady=10)

        # ═══ MÉTRICAS ═══
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

        # ═══ GRÁFICAS PRINCIPALES ═══
        charts_frame = ctk.CTkFrame(container, fg_color='transparent')
        charts_frame.pack(fill='both', expand=True, pady=(10, 0))
        charts_frame.columnconfigure((0, 1), weight=1)

        # Gráfica 1: Usuarios por Unidad
        self._create_mini_chart(
            charts_frame,
            "📊 Usuarios por Unidad de Negocio",
            chart_id='usuarios_unidad',
            chart_type='barras_h',
            row=0, column=0
        )

        # Gráfica 2: Progreso General
        self._create_mini_chart(
            charts_frame,
            "🍩 Progreso General por Unidad de Negocio",
            chart_id='progreso_unidades',
            chart_type='dona',
            row=0, column=1
        )

    def _create_dashboards_tab_content(self):
        """Crear contenido del tab Dashboards con grid 2x3"""
        theme = self.theme_manager.get_current_theme()

        container = ctk.CTkScrollableFrame(self.tab_dashboards, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=10, pady=10)

        # Título
        ctk.CTkLabel(
            container,
            text="📊 Dashboards Interactivos - Sistema Gerencial",
            font=('Montserrat', 20, 'bold'),
            text_color=HUTCHISON_COLORS['ports_sea_blue']
        ).pack(anchor='w', padx=20, pady=(10, 20))

        # Grid 2x3
        grid_frame = ctk.CTkFrame(container, fg_color='transparent')
        grid_frame.pack(fill='both', expand=True, padx=10, pady=10)
        grid_frame.columnconfigure((0, 1, 2), weight=1)
        grid_frame.rowconfigure((0, 1), weight=1)

        # FILA 1
        self._create_mini_chart(
            grid_frame,
            "📊 Usuarios por Unidad",
            chart_id='usuarios_unidad',
            chart_type='barras_h',
            row=0, column=0
        )

        self._create_mini_chart(
            grid_frame,
            "🍩 Progreso General por Unidad",
            chart_id='progreso_unidades',
            chart_type='dona',
            row=0, column=1
        )

        self._create_mini_chart(
            grid_frame,
            "📈 Tendencia Semanal",
            chart_id='tendencia_semanal',
            chart_type='linea',
            row=0, column=2
        )

        # FILA 2
        self._create_mini_chart(
            grid_frame,
            "📊 Top 5 Unidades de Mayor Progreso",
            chart_id='top5_unidades',
            chart_type='barras',
            row=1, column=0
        )

        self._create_mini_chart(
            grid_frame,
            "🎯 Cumplimiento de Objetivos",
            chart_id='cumplimiento',
            chart_type='dona',
            row=1, column=1
        )

        self._create_mini_chart(
            grid_frame,
            "📉 Módulos con Menor Avance",
            chart_id='menor_avance',
            chart_type='barras_h',
            row=1, column=2
        )

    def _create_mini_chart(self, parent, title, chart_id, chart_type, row, column):
        """Crear tarjeta de gráfica miniatura con botón expandir"""
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=12,
            border_width=1,
            border_color=theme['border']
        )
        card.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')

        # Header con título y botón expandir
        header = ctk.CTkFrame(card, fg_color='transparent', height=40)
        header.pack(fill='x', padx=15, pady=(10, 5))
        header.pack_propagate(False)

        # Título
        ctk.CTkLabel(
            header,
            text=title,
            font=('Montserrat', 12, 'bold'),
            text_color=theme['text']
        ).pack(side='left')

        # Botón expandir - NAVY BLUE
        expand_btn = ctk.CTkButton(
            header,
            text="⛶ Ver Grande",
            font=('Montserrat', 10, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            hover_color='#003D8F',
            text_color='white',
            corner_radius=8,
            height=26,
            width=100,
            command=lambda: self.show_expanded_view(chart_id, title, chart_type)
        )
        expand_btn.pack(side='right')

        # Preview de la gráfica
        preview_frame = ctk.CTkFrame(
            card,
            fg_color=theme['background'],
            corner_radius=8,
            height=200
        )
        preview_frame.pack(fill='both', expand=True, padx=15, pady=(5, 15))
        preview_frame.pack_propagate(False)

        # Renderizar preview
        self._render_chart_preview(preview_frame, chart_id, chart_type)

    def _render_chart_preview(self, container, chart_id, chart_type):
        """Renderizar preview pequeño de la gráfica"""
        theme = self.theme_manager.get_current_theme()
        data = self.datos_graficas.get(chart_id, {'labels': [], 'values': []})

        if not data.get('values'):
            # Placeholder si no hay datos
            ctk.CTkLabel(
                container,
                text="📊",
                font=('Segoe UI', 36),
                text_color=theme['text_tertiary']
            ).place(relx=0.5, rely=0.5, anchor='center')
            return

        # Crear figura pequeña
        fig = Figure(figsize=(4, 2.5), dpi=80, facecolor=theme['background'])
        ax = fig.add_subplot(111)

        labels = data.get('labels', [])
        values = data.get('values', [])

        # Renderizar según tipo
        if chart_type == 'barras':
            ax.bar(labels, values, color=HUTCHISON_COLORS['ports_sea_blue'], alpha=0.8)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=7)

        elif chart_type == 'barras_h':
            ax.barh(labels, values, color=HUTCHISON_COLORS['ports_sea_blue'], alpha=0.8)
            ax.tick_params(axis='y', labelsize=7)

        elif chart_type == 'dona':
            colors = [HUTCHISON_COLORS['aqua_green'], HUTCHISON_COLORS['ports_sea_blue'],
                     HUTCHISON_COLORS['ports_sky_blue'], '#FFC107', '#FF5722']
            ax.pie(values, labels=None, colors=colors[:len(values)], startangle=90)
            ax.axis('equal')

        elif chart_type == 'linea':
            ax.plot(labels, values, color=HUTCHISON_COLORS['ports_sea_blue'], linewidth=2, marker='o')
            ax.fill_between(range(len(labels)), values, alpha=0.3, color=HUTCHISON_COLORS['ports_sky_blue'])
            plt.setp(ax.xaxis.get_majorticklabels(), fontsize=7)

        # Estilo minimalista
        ax.set_facecolor(theme['background'])
        ax.tick_params(colors=theme['text'], labelsize=7)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color(theme['border'])
        ax.spines['left'].set_color(theme['border'])

        fig.tight_layout()

        # Integrar con tkinter
        canvas = FigureCanvasTkAgg(fig, container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    # ==================== CREAR VISTA EXPANDIDA ====================

    def _create_expanded_view(self):
        """Crear vista EXPANDIDA con gráfica en pantalla completa"""
        theme = self.theme_manager.get_current_theme()

        self.expanded_view = ctk.CTkFrame(self, fg_color=theme['background'])

        # Header con botón volver
        header = ctk.CTkFrame(
            self.expanded_view,
            fg_color=theme['surface'],
            height=70
        )
        header.pack(fill='x')
        header.pack_propagate(False)

        header_content = ctk.CTkFrame(header, fg_color='transparent')
        header_content.pack(fill='both', expand=True, padx=20, pady=15)

        # Botón volver - NAVY BLUE
        volver_btn = ctk.CTkButton(
            header_content,
            text="← Volver",
            font=('Montserrat', 14, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            hover_color='#003D8F',
            text_color='white',
            corner_radius=10,
            height=45,
            width=130,
            command=self.show_grid_view
        )
        volver_btn.pack(side='left')

        # Título de la gráfica
        self.expanded_title_label = ctk.CTkLabel(
            header_content,
            text="",
            font=('Montserrat', 20, 'bold'),
            text_color=theme['text']
        )
        self.expanded_title_label.pack(side='left', padx=25)

        # Info
        ctk.CTkLabel(
            header_content,
            text="🔍 Gráfica interactiva | Rueda del mouse para zoom",
            font=('Montserrat', 11),
            text_color=theme['text_secondary']
        ).pack(side='right')

        # Container para la gráfica gigante
        self.expanded_chart_container = ctk.CTkFrame(
            self.expanded_view,
            fg_color=theme['background']
        )
        self.expanded_chart_container.pack(fill='both', expand=True, padx=20, pady=20)

    def _render_expanded_chart(self):
        """Renderizar gráfica expandida en pantalla completa"""
        # Limpiar container
        for widget in self.expanded_chart_container.winfo_children():
            widget.destroy()

        if not self.current_chart_data:
            return

        # Actualizar título
        self.expanded_title_label.configure(text=self.current_chart_title)

        theme = self.theme_manager.get_current_theme()

        # Crear figura grande
        fig = Figure(figsize=(14, 8), dpi=100, facecolor=theme['background'])
        ax = fig.add_subplot(111)

        # Renderizar según tipo
        labels = self.current_chart_data.get('labels', [])
        values = self.current_chart_data.get('values', [])

        if self.current_chart_type == 'barras':
            bars = ax.bar(labels, values, color=HUTCHISON_COLORS['ports_sea_blue'], alpha=0.8)
            # Etiquetas en barras
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=12, fontweight='bold')
            ax.set_ylabel('Valor', fontsize=14)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=12)

        elif self.current_chart_type == 'barras_h':
            bars = ax.barh(labels, values, color=HUTCHISON_COLORS['ports_sea_blue'], alpha=0.8)
            # Etiquetas en barras
            for bar in bars:
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2.,
                       f' {int(width)}',
                       ha='left', va='center', fontsize=12, fontweight='bold')
            ax.set_xlabel('Cantidad', fontsize=14)
            ax.tick_params(axis='y', labelsize=11)

        elif self.current_chart_type == 'dona':
            colors = [HUTCHISON_COLORS['aqua_green'], HUTCHISON_COLORS['ports_sea_blue'],
                     HUTCHISON_COLORS['ports_sky_blue'], '#FFC107', '#FF5722']
            wedges, texts, autotexts = ax.pie(
                values, labels=labels, autopct='%1.1f%%', startangle=90,
                colors=colors[:len(values)], textprops={'fontsize': 12, 'fontweight': 'bold'}
            )
            for autotext in autotexts:
                autotext.set_color('white')
            ax.axis('equal')

        elif self.current_chart_type == 'linea':
            ax.plot(labels, values, color=HUTCHISON_COLORS['ports_sea_blue'],
                   linewidth=3, marker='o', markersize=10)
            ax.fill_between(range(len(labels)), values, alpha=0.3,
                           color=HUTCHISON_COLORS['ports_sky_blue'])
            # Etiquetas en puntos
            for i, v in enumerate(values):
                ax.text(i, v, str(int(v)), ha='center', va='bottom', fontsize=11, fontweight='bold')
            ax.set_xlabel('Tiempo', fontsize=14)
            ax.set_ylabel('Valor', fontsize=14)
            plt.setp(ax.xaxis.get_majorticklabels(), fontsize=11)

        # Estilo
        ax.set_facecolor(theme['background'])
        ax.tick_params(colors=theme['text'], labelsize=11)
        ax.spines['bottom'].set_color(theme['border'])
        ax.spines['left'].set_color(theme['border'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        fig.tight_layout()

        # Integrar con tkinter
        canvas = FigureCanvasTkAgg(fig, self.expanded_chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # === TOOLTIPS INTERACTIVOS (HOVER) ===
        # Crear anotación que se mostrará al hacer hover
        annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                           bbox=dict(boxstyle="round,pad=0.8", fc=HUTCHISON_COLORS['ports_sea_blue'],
                                    ec='white', lw=2, alpha=0.95),
                           arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3",
                                          color='white', lw=2),
                           fontsize=12, fontweight='bold', color='white',
                           visible=False, zorder=1000)

        def update_annot(bar_or_point, label, value):
            """Actualizar posición y texto del tooltip"""
            if self.current_chart_type in ['barras', 'barras_h']:
                # Para barras
                if self.current_chart_type == 'barras':
                    x = bar_or_point.get_x() + bar_or_point.get_width() / 2
                    y = bar_or_point.get_height()
                    annot.xy = (x, y)
                else:  # barras_h
                    x = bar_or_point.get_width()
                    y = bar_or_point.get_y() + bar_or_point.get_height() / 2
                    annot.xy = (x, y)
            else:
                # Para líneas y puntos
                annot.xy = bar_or_point

            text = f"{label}\n{int(value):,}"
            annot.set_text(text)
            annot.get_bbox_patch().set_alpha(0.95)

        def hover(event):
            """Manejar evento de hover del mouse"""
            vis = annot.get_visible()
            if event.inaxes == ax:
                if self.current_chart_type in ['barras', 'barras_h']:
                    # Detectar hover sobre barras
                    for i, bar in enumerate(bars):
                        cont, ind = bar.contains(event)
                        if cont:
                            update_annot(bar, labels[i], values[i])
                            annot.set_visible(True)
                            fig.canvas.draw_idle()
                            return
                elif self.current_chart_type == 'linea':
                    # Detectar hover sobre puntos de línea
                    for i, (x, y) in enumerate(zip(range(len(labels)), values)):
                        if abs(event.xdata - x) < 0.3 and abs(event.ydata - y) < max(values) * 0.05:
                            update_annot((x, y), labels[i], values[i])
                            annot.set_visible(True)
                            fig.canvas.draw_idle()
                            return

                # Si no está sobre ningún elemento, ocultar tooltip
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

        # Conectar evento de movimiento del mouse
        fig.canvas.mpl_connect("motion_notify_event", hover)

        # Toolbar de navegación
        toolbar_frame = ctk.CTkFrame(self.expanded_chart_container, fg_color=theme['surface'])
        toolbar_frame.pack(fill='x', pady=(10, 0))
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()

    # ==================== COMPONENTES AUXILIARES ====================

    def _create_metric_card(self, parent, icon, title, value, subtitle, color):
        """Crear tarjeta de métrica"""
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

        # Ícono
        ctk.CTkLabel(
            inner,
            text=icon,
            font=('Segoe UI', 42),
            text_color=color
        ).pack(anchor='center', pady=(0, 15))

        # Valor
        ctk.CTkLabel(
            inner,
            text=value,
            font=('Segoe UI', 36, 'bold'),
            text_color=theme['text']
        ).pack(anchor='center', pady=(0, 8))

        # Título
        ctk.CTkLabel(
            inner,
            text=title,
            font=('Segoe UI', 14, 'bold'),
            text_color=theme['text_secondary']
        ).pack(anchor='center', pady=(0, 5))

        # Subtítulo
        ctk.CTkLabel(
            inner,
            text=subtitle,
            font=('Segoe UI', 11),
            text_color=theme['text_tertiary'],
            wraplength=200
        ).pack(anchor='center')

        return card

    def _create_metric_card_modulo(self, parent, icon, title, value, color):
        """Crear tarjeta especial para Módulo Actual"""
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

        # Ícono
        ctk.CTkLabel(
            inner,
            text=icon,
            font=('Segoe UI', 42),
            text_color=color
        ).pack(anchor='center', pady=(0, 10))

        # Título
        ctk.CTkLabel(
            inner,
            text=title,
            font=('Segoe UI', 14, 'bold'),
            text_color=theme['text_secondary']
        ).pack(anchor='center', pady=(0, 15))

        # Valor
        ctk.CTkLabel(
            inner,
            text=value,
            font=('Segoe UI', 16, 'bold'),
            text_color=theme['text'],
            justify='center'
        ).pack(anchor='center')

        return card


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
    root.title("Dashboards Gerenciales - HUTCHISON PORTS")
    root.geometry("1400x900")

    # Crear panel
    panel = DashboardsGerencialesPanel(root)
    panel.pack(fill='both', expand=True)

    root.mainloop()

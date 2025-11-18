"""
Panel de Dashboard Moderno - HUTCHISON PORTS
Sistema completamente renovado con animaciones fluidas y diseño moderno

Features:
- ✅ Animaciones suaves con easing functions
- ✅ Cards con gradientes
- ✅ Progress rings animados
- ✅ Gráficas Plotly interactivas
- ✅ Sparklines en métricas
- ✅ Hover effects everywhere
- ✅ Tema oscuro moderno
- ✅ Tooltips mejorados
"""
import customtkinter as ctk
from smart_reports.ui.components.navigation.boton_pestana import CustomTabView
from smart_reports.ui.components.modern import (
    ModernMetricCard,
    CircularProgress,
    ModernButton,
    GlassCard,
    ModernTooltip
)
from smart_reports.ui.components.animations import AnimationEngine, EasingFunctions
from smart_reports.config.gestor_temas import get_theme_manager
from smart_reports.config.themes import HUTCHISON_COLORS

# Matplotlib para fallback (si Plotly no está disponible)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# ═══════════════════════════════════════════════════════════════════
#  DATOS ESTÁTICOS - DEMO
# ═══════════════════════════════════════════════════════════════════

USUARIOS_POR_UNIDAD_DATA = {
    'labels': ['LCMT', 'HPLM', 'ECV', 'TILH', 'CCI', 'TNG', 'HPMX', 'TIMSA', 'LCT', 'EIT', 'ICAVE'],
    'values': [3, 9, 23, 71, 76, 129, 145, 195, 226, 276, 372]
}

PROGRESO_UNIDADES_DATA = {
    'labels': ['TNG - 100%', 'ICAVE - 82%', 'ECV - 75%', 'Container - 68%', 'HPMX - 62%'],
    'values': [100, 82, 75, 68, 62]
}

TENDENCIA_SEMANAL_DATA = {
    'labels': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
    'values': [65, 72, 78, 85, 92, 88, 95]
}


class PanelDashboardModerno(ctk.CTkFrame):
    """
    Dashboard Moderno con todas las mejoras visuales

    Sistema de navegación:
    - Tab General: Métricas principales + KPIs
    - Tab Analytics: Gráficas detalladas
    - Tab Performance: Indicadores de rendimiento
    """

    def __init__(self, parent, db_connection=None, usuario_actual=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        print("🚀 Inicializando Dashboard Moderno...")

        self.theme_manager = get_theme_manager()
        self.theme = self.theme_manager.get_current_theme()
        self.db_connection = db_connection
        self.usuario_actual = usuario_actual or {"nombre": "Admin"}

        # Referencias
        self.metric_cards = []
        self.progress_rings = []

        try:
            self._create_ui()
            print("✅ Dashboard Moderno inicializado correctamente")

        except Exception as e:
            print(f"❌ Error inicializando dashboard: {e}")
            import traceback
            traceback.print_exc()

    def _create_ui(self):
        """Crear UI principal"""
        # Header con gradiente
        self._create_header()

        # Tabs modernos
        self.tab_view = CustomTabView(self)
        self.tab_view.pack(fill='both', expand=True, padx=15, pady=(10, 15))

        # Tab 1: General (métricas principales)
        self.tab_general = self.tab_view.add("General", "📊")
        self._create_general_tab()

        # Tab 2: Analytics (gráficas detalladas)
        self.tab_analytics = self.tab_view.add("Analytics", "📈")
        self._create_analytics_tab()

        # Tab 3: Performance (rendimiento)
        self.tab_performance = self.tab_view.add("Performance", "🎯")
        self._create_performance_tab()

    def _create_header(self):
        """Crear header con gradiente"""
        header = ctk.CTkFrame(
            self,
            fg_color=self.theme['surface'],
            height=80,
            corner_radius=0
        )
        header.pack(fill='x')
        header.pack_propagate(False)

        content = ctk.CTkFrame(header, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=30, pady=20)

        # Título con icono
        title_frame = ctk.CTkFrame(content, fg_color='transparent')
        title_frame.pack(side='left')

        ctk.CTkLabel(
            title_frame,
            text="📊 Dashboard Moderno",
            font=('Poppins', 28, 'bold'),
            text_color=self.theme['text']
        ).pack(side='left')

        # Badge "NUEVO"
        badge = ctk.CTkFrame(
            title_frame,
            fg_color='#667eea',
            corner_radius=15,
            height=30
        )
        badge.pack(side='left', padx=15)

        ctk.CTkLabel(
            badge,
            text="✨ NUEVO",
            font=('Poppins', 11, 'bold'),
            text_color='white'
        ).pack(padx=15, pady=4)

        # Botones de acción
        actions = ctk.CTkFrame(content, fg_color='transparent')
        actions.pack(side='right')

        ModernButton(
            actions,
            text="Actualizar",
            icon="🔄",
            gradient_colors=('#667eea', '#764ba2'),
            width=150,
            command=self._refresh_data
        ).pack(side='right', padx=5)

        ModernButton(
            actions,
            text="Exportar",
            icon="📥",
            gradient_colors=('#11998e', '#38ef7d'),
            width=140,
            command=self._export_dashboard
        ).pack(side='right', padx=5)

    # ═══════════════════════════════════════════════════════════════════
    # TAB 1: GENERAL
    # ═══════════════════════════════════════════════════════════════════

    def _create_general_tab(self):
        """Crear tab General con métricas principales"""
        container = ctk.CTkScrollableFrame(
            self.tab_general,
            fg_color='transparent'
        )
        container.pack(fill='both', expand=True, padx=15, pady=15)

        # Sección 1: KPIs principales con animación escalonada
        kpis_frame = ctk.CTkFrame(container, fg_color='transparent')
        kpis_frame.pack(fill='x', pady=(0, 25))
        kpis_frame.columnconfigure((0, 1, 2, 3), weight=1)

        # Datos de sparklines para cada métrica
        sparkline_usuarios = [1200, 1250, 1300, 1400, 1450, 1500, 1525]
        sparkline_progreso = [50, 55, 60, 65, 68, 69, 70]
        sparkline_completados = [800, 850, 900, 950, 1000, 1050, 1068]

        # KPI 1: Total Usuarios
        card1 = ModernMetricCard(
            kpis_frame,
            title="Total de Usuarios",
            value="1,525",
            icon="👥",
            gradient_colors=('#667eea', '#764ba2'),
            change_percent=12.5,
            sparkline_data=sparkline_usuarios
        )
        card1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.metric_cards.append(card1)

        # KPI 2: Tasa de Progreso
        card2 = ModernMetricCard(
            kpis_frame,
            title="Tasa de Progreso",
            value="70.0%",
            icon="📈",
            gradient_colors=('#11998e', '#38ef7d'),
            change_percent=5.2,
            sparkline_data=sparkline_progreso
        )
        card2.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        self.metric_cards.append(card2)

        # KPI 3: Completados
        card3 = ModernMetricCard(
            kpis_frame,
            title="Módulos Completados",
            value="1,068",
            icon="✅",
            gradient_colors=('#4facfe', '#00f2fe'),
            change_percent=8.7,
            sparkline_data=sparkline_completados
        )
        card3.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')
        self.metric_cards.append(card3)

        # KPI 4: Módulo Actual
        card4 = ModernMetricCard(
            kpis_frame,
            title="Módulo Actual",
            value="Módulo 8",
            icon="📄",
            gradient_colors=('#f093fb', '#f5576c'),
            change_percent=None
        )
        card4.grid(row=0, column=3, padx=10, pady=10, sticky='nsew')
        self.metric_cards.append(card4)

        # Animar entrada de cards con delay escalonado
        animator = AnimationEngine(self)
        animator.stagger_children(
            self.metric_cards,
            animation_type='scale',
            stagger_delay=100,
            from_scale=0.8,
            to_scale=1.0,
            duration=500,
            easing=EasingFunctions.ease_out_back
        )

        # Sección 2: Progress Rings
        progress_section = ctk.CTkFrame(container, fg_color='transparent')
        progress_section.pack(fill='x', pady=(0, 25))

        # Título de sección
        section_title = ctk.CTkFrame(progress_section, fg_color='transparent', height=40)
        section_title.pack(fill='x', pady=(0, 15))

        ctk.CTkLabel(
            section_title,
            text="📊 Progreso por Unidad de Negocio",
            font=('Poppins', 18, 'bold'),
            text_color=self.theme['text'],
            anchor='w'
        ).pack(side='left', padx=10)

        # Grid de progress rings
        rings_grid = ctk.CTkFrame(progress_section, fg_color='transparent')
        rings_grid.pack(fill='x')
        rings_grid.columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Progress data
        progress_data = [
            ("TNG", 100, '#667eea'),
            ("ICAVE", 82, '#11998e'),
            ("ECV", 75, '#f093fb'),
            ("Container", 68, '#4facfe'),
            ("HPMX", 62, '#ffd43b')
        ]

        for i, (label, percentage, color) in enumerate(progress_data):
            ring = CircularProgress(
                rings_grid,
                percentage=percentage,
                size=140,
                label=label,
                color=color
            )
            ring.grid(row=0, column=i, padx=10, pady=10)
            self.progress_rings.append(ring)

        # Sección 3: Gráficas principales
        charts_section = ctk.CTkFrame(container, fg_color='transparent')
        charts_section.pack(fill='both', expand=True)
        charts_section.columnconfigure((0, 1), weight=1)

        # Gráfica 1: Usuarios por Unidad
        chart1_container = GlassCard(charts_section)
        chart1_container.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self._create_bar_chart(
            chart1_container,
            "Usuarios por Unidad de Negocio",
            USUARIOS_POR_UNIDAD_DATA
        )

        # Gráfica 2: Distribución de Progreso
        chart2_container = GlassCard(charts_section)
        chart2_container.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        self._create_donut_chart(
            chart2_container,
            "Distribución de Progreso",
            PROGRESO_UNIDADES_DATA
        )

    # ═══════════════════════════════════════════════════════════════════
    # TAB 2: ANALYTICS
    # ═══════════════════════════════════════════════════════════════════

    def _create_analytics_tab(self):
        """Crear tab Analytics con gráficas detalladas"""
        container = ctk.CTkScrollableFrame(
            self.tab_analytics,
            fg_color='transparent'
        )
        container.pack(fill='both', expand=True, padx=15, pady=15)

        # Grid de gráficas
        charts_grid = ctk.CTkFrame(container, fg_color='transparent')
        charts_grid.pack(fill='both', expand=True)
        charts_grid.columnconfigure((0, 1), weight=1)
        charts_grid.rowconfigure((0, 1), weight=1)

        # Gráfica 1: Tendencia Semanal (área)
        card1 = GlassCard(charts_grid)
        card1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self._create_area_chart(
            card1,
            "Tendencia Semanal",
            TENDENCIA_SEMANAL_DATA
        )

        # Gráfica 2: Top 5 Unidades
        card2 = GlassCard(charts_grid)
        card2.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        self._create_bar_chart(
            card2,
            "Top 5 Unidades",
            {
                'labels': ['TNG', 'ICAVE', 'ECV', 'Container', 'HPMX'],
                'values': [100, 85, 75, 68, 62]
            }
        )

        # Gráfica 3: Cumplimiento de Objetivos
        card3 = GlassCard(charts_grid)
        card3.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self._create_donut_chart(
            card3,
            "Cumplimiento de Objetivos",
            {
                'labels': ['Completados', 'En Progreso', 'Pendientes', 'Retrasados'],
                'values': [70, 20, 8, 2]
            }
        )

        # Gráfica 4: Módulos con Menor Avance
        card4 = GlassCard(charts_grid)
        card4.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        self._create_bar_chart(
            card4,
            "Módulos con Menor Avance",
            {
                'labels': ['Mod 8', 'Mod 7', 'Mod 6', 'Mod 5', 'Mod 4'],
                'values': [45, 52, 58, 65, 72]
            },
            orientation='h'
        )

    # ═══════════════════════════════════════════════════════════════════
    # TAB 3: PERFORMANCE
    # ═══════════════════════════════════════════════════════════════════

    def _create_performance_tab(self):
        """Crear tab Performance con indicadores"""
        container = ctk.CTkScrollableFrame(
            self.tab_performance,
            fg_color='transparent'
        )
        container.pack(fill='both', expand=True, padx=15, pady=15)

        # Título
        ctk.CTkLabel(
            container,
            text="🎯 Indicadores de Rendimiento",
            font=('Poppins', 22, 'bold'),
            text_color=self.theme['text']
        ).pack(anchor='w', padx=20, pady=(10, 25))

        # Grid de indicadores
        indicators_grid = ctk.CTkFrame(container, fg_color='transparent')
        indicators_grid.pack(fill='both', expand=True)
        indicators_grid.columnconfigure((0, 1, 2), weight=1)

        # Indicador 1: Tasa de Completado
        self._create_performance_card(
            indicators_grid,
            "Tasa de Completado",
            85,
            "Usuarios que completaron todos los módulos",
            '#11998e',
            row=0, col=0
        )

        # Indicador 2: Engagement
        self._create_performance_card(
            indicators_grid,
            "Engagement",
            92,
            "Usuarios activos en los últimos 7 días",
            '#667eea',
            row=0, col=1
        )

        # Indicador 3: Retención
        self._create_performance_card(
            indicators_grid,
            "Retención",
            78,
            "Usuarios que regresan regularmente",
            '#f093fb',
            row=0, col=2
        )

        # Indicador 4: Eficiencia
        self._create_performance_card(
            indicators_grid,
            "Eficiencia",
            88,
            "Módulos completados en tiempo óptimo",
            '#4facfe',
            row=1, col=0
        )

        # Indicador 5: Satisfacción
        self._create_performance_card(
            indicators_grid,
            "Satisfacción",
            94,
            "Calificación promedio del sistema",
            '#ffd43b',
            row=1, col=1
        )

        # Indicador 6: ROI
        self._create_performance_card(
            indicators_grid,
            "ROI Capacitación",
            76,
            "Retorno de inversión en capacitación",
            '#ff6b6b',
            row=1, col=2
        )

    def _create_performance_card(self, parent, title, percentage, description, color, row, col):
        """Crear card de indicador de rendimiento"""
        card = GlassCard(parent)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # Progress ring
        ring = CircularProgress(
            card,
            percentage=percentage,
            size=120,
            label="",
            color=color
        )
        ring.pack(pady=(20, 15))

        # Título
        ctk.CTkLabel(
            card,
            text=title,
            font=('Poppins', 15, 'bold'),
            text_color=self.theme['text']
        ).pack(pady=(0, 5))

        # Descripción
        ctk.CTkLabel(
            card,
            text=description,
            font=('Poppins', 11),
            text_color=self.theme['text_secondary'],
            wraplength=200
        ).pack(pady=(0, 20))

    # ═══════════════════════════════════════════════════════════════════
    # HELPERS - GRÁFICAS
    # ═══════════════════════════════════════════════════════════════════

    def _create_bar_chart(self, parent, title, data, orientation='v'):
        """Crear gráfica de barras"""
        # Header
        header = ctk.CTkFrame(parent, fg_color='transparent', height=50)
        header.pack(fill='x', padx=15, pady=(15, 5))

        ctk.CTkLabel(
            header,
            text=title,
            font=('Poppins', 14, 'bold'),
            text_color=self.theme['text']
        ).pack(side='left')

        # Chart container
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color=self.theme['background'],
            corner_radius=12,
            height=300
        )
        chart_frame.pack(fill='both', expand=True, padx=15, pady=(5, 15))

        # Crear figura
        fig = Figure(figsize=(6, 4), dpi=90, facecolor=self.theme['background'])
        ax = fig.add_subplot(111)

        labels = data['labels']
        values = data['values']

        if orientation == 'v':
            bars = ax.bar(labels, values, color='#667eea', alpha=0.9, edgecolor='white', linewidth=1.5)
            ax.set_ylabel('Valor', fontsize=11, color=self.theme['text'])
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=9)
        else:
            bars = ax.barh(labels, values, color='#667eea', alpha=0.9, edgecolor='white', linewidth=1.5)
            ax.set_xlabel('Valor', fontsize=11, color=self.theme['text'])
            ax.tick_params(axis='y', labelsize=9)

        # Etiquetas en barras
        for bar in bars:
            if orientation == 'v':
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold',
                       color=self.theme['text'])
            else:
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2.,
                       f' {int(width)}',
                       ha='left', va='center', fontsize=10, fontweight='bold',
                       color=self.theme['text'])

        # Estilo
        ax.set_facecolor(self.theme['background'])
        ax.tick_params(colors=self.theme['text'], labelsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color(self.theme['border'])
        ax.spines['left'].set_color(self.theme['border'])

        fig.tight_layout()

        # Mostrar
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def _create_donut_chart(self, parent, title, data):
        """Crear gráfica de dona"""
        # Header
        header = ctk.CTkFrame(parent, fg_color='transparent', height=50)
        header.pack(fill='x', padx=15, pady=(15, 5))

        ctk.CTkLabel(
            header,
            text=title,
            font=('Poppins', 14, 'bold'),
            text_color=self.theme['text']
        ).pack(side='left')

        # Chart
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color=self.theme['background'],
            corner_radius=12,
            height=300
        )
        chart_frame.pack(fill='both', expand=True, padx=15, pady=(5, 15))

        fig = Figure(figsize=(6, 4), dpi=90, facecolor=self.theme['background'])
        ax = fig.add_subplot(111)

        colors = ['#667eea', '#11998e', '#f093fb', '#4facfe', '#ffd43b']
        wedges, texts, autotexts = ax.pie(
            data['values'],
            labels=data['labels'],
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(data['values'])],
            wedgeprops=dict(edgecolor='white', linewidth=2),
            textprops=dict(color=self.theme['text'], fontsize=10)
        )

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.axis('equal')
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def _create_area_chart(self, parent, title, data):
        """Crear gráfica de área"""
        # Header
        header = ctk.CTkFrame(parent, fg_color='transparent', height=50)
        header.pack(fill='x', padx=15, pady=(15, 5))

        ctk.CTkLabel(
            header,
            text=title,
            font=('Poppins', 14, 'bold'),
            text_color=self.theme['text']
        ).pack(side='left')

        # Chart
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color=self.theme['background'],
            corner_radius=12,
            height=300
        )
        chart_frame.pack(fill='both', expand=True, padx=15, pady=(5, 15))

        fig = Figure(figsize=(6, 4), dpi=90, facecolor=self.theme['background'])
        ax = fig.add_subplot(111)

        labels = data['labels']
        values = data['values']

        ax.plot(labels, values, color='#667eea', linewidth=3, marker='o', markersize=8,
               markerfacecolor='white', markeredgecolor='#667eea', markeredgewidth=2)
        ax.fill_between(range(len(labels)), values, alpha=0.3, color='#667eea')

        # Etiquetas
        for i, v in enumerate(values):
            ax.text(i, v, str(int(v)), ha='center', va='bottom',
                   fontsize=10, fontweight='bold', color=self.theme['text'])

        ax.set_ylabel('Valor', fontsize=11, color=self.theme['text'])
        ax.set_facecolor(self.theme['background'])
        ax.tick_params(colors=self.theme['text'], labelsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color(self.theme['border'])
        ax.spines['left'].set_color(self.theme['border'])

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    # ═══════════════════════════════════════════════════════════════════
    # ACCIONES
    # ═══════════════════════════════════════════════════════════════════

    def _refresh_data(self):
        """Refrescar datos del dashboard"""
        print("🔄 Refrescando datos...")

        # Animar métricas
        for card in self.metric_cards:
            # Simular cambio de valor
            current_value = card.value
            card.update_value(current_value, animate=True)

        # Animar progress rings
        for ring in self.progress_rings:
            # Re-animar
            ring.update_percentage(ring.percentage)

    def _export_dashboard(self):
        """Exportar dashboard"""
        print("📥 Exportando dashboard...")
        # TODO: Implementar exportación a PDF/PNG


# ═══════════════════════════════════════════════════════════════════
#  TESTING
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import customtkinter as ctk

    ctk.set_appearance_mode("dark")

    root = ctk.CTk()
    root.title("Dashboard Moderno - HUTCHISON PORTS")
    root.geometry("1400x900")

    panel = PanelDashboardModerno(root)
    panel.pack(fill='both', expand=True)

    root.mainloop()

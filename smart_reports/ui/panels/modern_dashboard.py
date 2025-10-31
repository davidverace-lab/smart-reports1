"""
Panel ModernDashboard - Dashboard optimizado con lazy loading y pestañas
"""
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from smart_reports.ui.components.matplotlib_chart_card import MatplotlibChartCard
from smart_reports.ui.components.metric_card import MetricCard
from smart_reports.ui.panels.matplotlib_interactive_panel import MatplotlibInteractivePanel
from smart_reports.config.settings import HUTCHISON_COLORS, EXECUTIVE_CHART_COLORS
from smart_reports.config.theme_manager import get_theme_manager


# Datos de ejemplo basados en las imágenes proporcionadas
DATOS_TNG = {
    'modulos': ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'],
    'sin_iniciar': [45, 38, 42, 35, 40, 33, 37, 30],
    'en_proceso': [32, 28, 25, 30, 27, 32, 28, 25],
    'completado': [123, 134, 133, 135, 133, 135, 135, 145]
}

DATOS_CONTAINER_CARE = {
    'modulos': ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'],
    'sin_iniciar': [28, 25, 30, 22, 27, 20, 24, 18],
    'en_proceso': [18, 15, 12, 16, 14, 18, 15, 12],
    'completado': [54, 60, 58, 62, 59, 62, 61, 70]
}

DATOS_ECV_EIT = {
    'modulos': ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'],
    'sin_iniciar': [35, 30, 33, 28, 32, 26, 29, 24],
    'en_proceso': [22, 20, 18, 24, 21, 25, 22, 19],
    'completado': [83, 90, 89, 88, 87, 89, 89, 97]
}

DATOS_JERARQUICO = {
    'fases': ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'],
    'puestos': {
        'DIRECTORES': [12, 12, 12, 11, 11, 10, 10, 10],
        'GERENTES GENERALES': [25, 24, 23, 23, 22, 22, 21, 20],
        'GERENTES SENIOR': [45, 44, 43, 42, 42, 41, 40, 39],
        'GERENTES DE AREA': [68, 67, 65, 64, 63, 62, 61, 60],
        'SUBGERENTES': [92, 90, 88, 87, 85, 84, 82, 80],
        'COORDINADORES': [115, 112, 110, 108, 106, 104, 102, 100],
        'SUPERVISORES': [145, 142, 140, 138, 135, 133, 130, 128],
        'JEFES DE TURNO': [180, 176, 173, 170, 167, 164, 161, 158]
    }
}

# Colores Hutchison Ports para UI
PRIMARY_COLORS = {
    'accent_blue': HUTCHISON_COLORS['ports_sky_blue'],
    'accent_green': HUTCHISON_COLORS['success'],
    'accent_orange': HUTCHISON_COLORS['warning'],
    'accent_cyan': HUTCHISON_COLORS['ports_horizon_blue'],
    'accent_yellow': HUTCHISON_COLORS['sunray_yellow'],
    'accent_red': HUTCHISON_COLORS['danger'],
    'accent_purple': HUTCHISON_COLORS['ports_sea_blue']
}


class ModernDashboard(ctk.CTkFrame):
    """Dashboard optimizado con lazy loading y pestañas"""

    def __init__(self, parent, db_connection, **kwargs):
        """
        Args:
            parent: Widget padre
            db_connection: Conexión a la base de datos
        """
        # Obtener tema actual
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(parent, fg_color=theme['background'], **kwargs)
        self.db = db_connection
        self.cursor = db_connection.cursor() if db_connection else None

        # Flags para lazy loading (según especificación)
        self._general_loaded = False
        self._progreso_loaded = False
        self._jerarquico_loaded = False
        self._interactivo_loaded = False

        # Referencias a componentes
        self.progreso_bar_card = None
        self.progreso_donut_card = None
        self.unit_selector = None
        self.current_unit = 'TNG'

        # Configurar grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Crear contenido con pestañas
        self._create_tabbed_content()

        # Cargar pestaña General al inicio (después de crear widgets)
        self.after(50, self.load_general_charts)

    def _create_tabbed_content(self):
        """Crear contenedor con pestañas usando CTkSegmentedButton"""
        # Frame principal con padding
        main_frame = ctk.CTkFrame(self, fg_color='transparent')
        main_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)  # content_frame ocupará el espacio

        # Header con título y botón exportar
        header = ctk.CTkFrame(main_frame, fg_color='transparent', height=60)
        header.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        header.grid_propagate(False)

        theme = self.theme_manager.get_current_theme()

        self.title_label = ctk.CTkLabel(
            header,
            text='📊 Panel de Control',
            font=('Montserrat', 28, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        self.title_label.pack(side='left')

        # Botón Exportar a PDF
        export_pdf_btn = ctk.CTkButton(
            header,
            text='📄 Exportar a PDF',
            font=('Arial', 14, 'bold'),
            fg_color=PRIMARY_COLORS['accent_green'],
            hover_color='#40b656',
            corner_radius=10,
            height=40,
            width=180,
            command=self.export_dashboard_pdf
        )
        export_pdf_btn.pack(side='right', padx=10)

        # Header Frame para el CTkSegmentedButton (pestañas)
        header_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        header_frame.grid(row=1, column=0, sticky='ew', pady=(0, 15))

        # Configurar colores del CTkSegmentedButton según modo
        is_dark = self.theme_manager.is_dark_mode()

        if is_dark:
            seg_fg_color = theme['surface']
            seg_text_color = '#FFFFFF'
            seg_selected_color = PRIMARY_COLORS['accent_blue']
            seg_selected_hover = '#007bb5'
        else:
            seg_fg_color = '#FFFFFF'
            seg_text_color = HUTCHISON_COLORS['ports_sea_blue']
            seg_selected_color = PRIMARY_COLORS['accent_blue']
            seg_selected_hover = '#007bb5'

        # CTkSegmentedButton para pestañas
        self.tab_selector = ctk.CTkSegmentedButton(
            header_frame,
            values=["General", "Progreso por Módulo", "Avance Jerárquico", "Dashboards Interactivos"],
            font=('Montserrat Bold', 14),
            height=40,
            fg_color=seg_fg_color,
            selected_color=seg_selected_color,
            selected_hover_color=seg_selected_hover,
            text_color=seg_text_color,
            text_color_disabled='#888888',
            command=self.on_tab_change
        )
        self.tab_selector.pack(fill='x', padx=15, pady=5)
        self.tab_selector.set("General")  # Seleccionar pestaña inicial

        # Content Frame (contenedor de las pestañas)
        content_frame = ctk.CTkFrame(main_frame, fg_color=theme['surface'], corner_radius=15)
        content_frame.grid(row=2, column=0, sticky='nsew')
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Crear frames para cada pestaña (todos en la misma celda)
        self.general_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
        self.progreso_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
        self.jerarquico_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
        self.interactivo_frame = ctk.CTkFrame(content_frame, fg_color='transparent')

        # Configurar grids de los frames
        self.general_frame.grid_columnconfigure(0, weight=1)
        self.general_frame.grid_rowconfigure((0, 1), weight=1)

        self.progreso_frame.grid_columnconfigure(0, weight=1)
        self.progreso_frame.grid_rowconfigure(1, weight=1)

        self.jerarquico_frame.grid_columnconfigure((0, 1), weight=1)
        self.jerarquico_frame.grid_rowconfigure(0, weight=1)

        self.interactivo_frame.grid_columnconfigure(0, weight=1)
        self.interactivo_frame.grid_rowconfigure(0, weight=1)

        # Colocar todos los frames en la misma posición (solo uno visible a la vez)
        self.general_frame.grid(row=0, column=0, sticky='nsew')
        self.progreso_frame.grid(row=0, column=0, sticky='nsew')
        self.jerarquico_frame.grid(row=0, column=0, sticky='nsew')
        self.interactivo_frame.grid(row=0, column=0, sticky='nsew')

        # Ocultar todos excepto el primero
        self.progreso_frame.grid_remove()
        self.jerarquico_frame.grid_remove()
        self.interactivo_frame.grid_remove()

        # Almacenar referencias a las pestañas (para compatibilidad)
        self.tab_general = self.general_frame
        self.tab_progreso = self.progreso_frame
        self.tab_jerarquico = self.jerarquico_frame
        self.tab_interactivo = self.interactivo_frame

    def on_tab_change(self, value):
        """Callback cuando cambia la pestaña - Lazy loading y cambio de vista"""
        # Ocultar todos los frames
        self.general_frame.grid_remove()
        self.progreso_frame.grid_remove()
        self.jerarquico_frame.grid_remove()
        self.interactivo_frame.grid_remove()

        # Mostrar el frame correspondiente y cargar datos si es necesario
        if value == "General":
            self.general_frame.grid(row=0, column=0, sticky='nsew')
            if not self._general_loaded:
                self.load_general_charts()
                self._general_loaded = True
        elif value == "Progreso por Módulo":
            self.progreso_frame.grid(row=0, column=0, sticky='nsew')
            if not self._progreso_loaded:
                self.load_progreso_charts()
                self._progreso_loaded = True
        elif value == "Avance Jerárquico":
            self.jerarquico_frame.grid(row=0, column=0, sticky='nsew')
            if not self._jerarquico_loaded:
                self.load_jerarquico_charts()
                self._jerarquico_loaded = True
        elif value == "Dashboards Interactivos":
            self.interactivo_frame.grid(row=0, column=0, sticky='nsew')
            if not self._interactivo_loaded:
                self.load_interactivo_charts()
                self._interactivo_loaded = True

    def load_general_charts(self):
        """Cargar pestaña General (lazy loading)"""
        if self._general_loaded:
            return

        self._create_tab_general(self.tab_general)
        self._general_loaded = True

    def load_progreso_charts(self):
        """Cargar pestaña Progreso (lazy loading)"""
        if self._progreso_loaded:
            return

        self._create_tab_progreso_modulo(self.tab_progreso)
        self._progreso_loaded = True

    def load_jerarquico_charts(self):
        """Cargar pestaña Jerárquico (lazy loading)"""
        if self._jerarquico_loaded:
            return

        self._create_tab_comportamiento_jerarquico(self.tab_jerarquico)
        self._jerarquico_loaded = True

    def load_interactivo_charts(self):
        """Cargar pestaña Dashboards Interactivos (lazy loading)"""
        if self._interactivo_loaded:
            return

        # Crear panel de gráficos interactivos con Matplotlib
        interactive_panel = MatplotlibInteractivePanel(
            self.tab_interactivo,
            self.db
        )
        interactive_panel.pack(fill='both', expand=True, padx=5, pady=5)
        self._interactivo_loaded = True

    # ==================== PESTAÑA GENERAL ====================

    def _create_tab_general(self, parent):
        """Crear pestaña General con métricas y gráficos"""
        # Row 1: Métricas (3 cards)
        metrics_frame = ctk.CTkFrame(parent, fg_color='transparent')
        metrics_frame.grid(row=0, column=0, sticky='ew', padx=15, pady=(15, 10))
        metrics_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Obtener datos reales
        total_users = self._get_total_users()
        active_modules = self._get_active_modules()
        completion_rate = self._get_completion_rate()

        # Metric Card 1: Total Usuarios
        metric1 = MetricCard(
            metrics_frame,
            title='Total de Usuarios',
            value=f'{total_users:,}',
            icon='👥',
            color=PRIMARY_COLORS['accent_blue']
        )
        metric1.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

        # Metric Card 2: Módulos Activos
        metric2 = MetricCard(
            metrics_frame,
            title='Módulos Activos',
            value=f'{active_modules}/14',
            icon='📚',
            color=PRIMARY_COLORS['accent_cyan']
        )
        metric2.grid(row=0, column=1, sticky='ew', padx=10, pady=10)

        # Metric Card 3: Tasa de Completado
        metric3 = MetricCard(
            metrics_frame,
            title='Tasa de Completado',
            value=f'{completion_rate:.1f}%',
            icon='✓',
            color=PRIMARY_COLORS['accent_green']
        )
        metric3.grid(row=0, column=2, sticky='ew', padx=10, pady=10)

        # Row 2: Gráficos (2 cards)
        charts_frame = ctk.CTkFrame(parent, fg_color='transparent')
        charts_frame.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 15))
        charts_frame.grid_columnconfigure((0, 1), weight=1)
        charts_frame.grid_rowconfigure(0, weight=1)

        # Chart 1: Usuarios por Unidad (Barras Horizontales)
        chart1 = MatplotlibChartCard(
            charts_frame,
            title='Usuarios por Unidad de Negocio'
        )
        chart1.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        # Chart 2: Distribución Porcentual (Donut)
        chart2 = MatplotlibChartCard(
            charts_frame,
            title='Distribución Porcentual'
        )
        chart2.grid(row=0, column=1, sticky='nsew', padx=(10, 0))

        # Crear gráficos
        self._create_general_charts(chart1, chart2)

    def _create_general_charts(self, chart1, chart2):
        """Crear gráficos para pestaña General"""
        # Obtener datos
        units_data = self._get_users_by_unit()

        if units_data and len(units_data) > 0:
            units = [row[0] for row in units_data]
            counts = [row[1] for row in units_data]

            # Usar paleta ejecutiva Hutchison Ports para gráficos
            colors = EXECUTIVE_CHART_COLORS[:len(units)]

            # Gráfico 1: Barras horizontales
            fig1 = Figure(figsize=(8, 5))
            ax1 = fig1.add_subplot(111)

            bars = ax1.barh(units, counts, color=colors, edgecolor='none')
            ax1.set_xlabel('Número de Usuarios', fontsize=11)
            ax1.set_ylabel('', fontsize=11)
            ax1.tick_params(labelsize=10)
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.grid(axis='x', alpha=0.3)

            # Añadir valores en las barras
            for bar in bars:
                width = bar.get_width()
                ax1.text(width, bar.get_y() + bar.get_height()/2,
                        f'{int(width)}',
                        ha='left', va='center', fontsize=9,
                        fontweight='bold', pad=5)

            fig1.tight_layout()
            chart1.set_figure(fig1)

            # Gráfico 2: Donut
            fig2 = Figure(figsize=(8, 5))
            ax2 = fig2.add_subplot(111)

            theme = self.theme_manager.get_current_theme()
            edge_color = theme['surface']

            wedges, texts, autotexts = ax2.pie(
                counts,
                labels=units,
                colors=colors,
                autopct='%1.1f%%',
                startangle=90,
                pctdistance=0.85,
                wedgeprops=dict(width=0.5, edgecolor=edge_color, linewidth=3)
            )

            # Estilo de textos
            for text in texts:
                text.set_fontsize(10)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(9)
                autotext.set_weight('bold')

            # Leyenda horizontal
            ax2.legend(
                wedges, units,
                loc='upper center',
                bbox_to_anchor=(0.5, -0.05),
                ncol=min(len(units), 3),
                fontsize=9,
                frameon=True
            )

            fig2.tight_layout()
            chart2.set_figure(fig2)

    # ==================== PESTAÑA PROGRESO POR MÓDULO ====================

    def _create_tab_progreso_modulo(self, parent):
        """Crear pestaña de Progreso por Módulo con gráfico dinámico"""
        # Frame para selector con diseño mejorado
        selector_frame = ctk.CTkFrame(parent, fg_color='transparent')
        selector_frame.grid(row=0, column=0, sticky='ew', padx=15, pady=(15, 10))

        theme = self.theme_manager.get_current_theme()

        # Label
        label = ctk.CTkLabel(
            selector_frame,
            text='📍 Seleccionar Unidad de Negocio:',
            font=('Arial', 16, 'bold'),
            text_color=theme['text']
        )
        label.pack(side='left', padx=(10, 20))

        # Obtener unidades de negocio desde la base de datos
        business_units = self._get_business_units_from_db()

        # Si no hay unidades en BD, usar lista por defecto
        if not business_units:
            business_units = [
                'TNG',
                'CONTAINER CARE',
                'ECV-EIT',
                'OPERACIONES PORTUARIAS',
                'LOGÍSTICA',
                'MANTENIMIENTO',
                'ADMINISTRACIÓN',
                'RECURSOS HUMANOS',
                'FINANZAS',
                'SEGURIDAD',
                'TECNOLOGÍA'
            ]

        # Usar OptionMenu más grande y visible
        dropdown_fg = theme['surface_light'] if self.theme_manager.is_dark_mode() else '#FFFFFF'
        dropdown_border = PRIMARY_COLORS['accent_blue']

        self.unit_selector = ctk.CTkOptionMenu(
            selector_frame,
            values=business_units,
            font=('Arial', 14, 'bold'),
            dropdown_font=('Arial', 13),
            width=350,
            height=50,
            corner_radius=12,
            fg_color=dropdown_fg,
            button_color=PRIMARY_COLORS['accent_blue'],
            button_hover_color='#007bb5',
            dropdown_fg_color=dropdown_fg,
            dropdown_hover_color=PRIMARY_COLORS['accent_blue'],
            text_color=theme['text'],
            command=self._on_unit_change
        )
        self.unit_selector.pack(side='left', padx=(0, 10))

        # Establecer primera unidad como seleccionada
        if business_units:
            self.unit_selector.set(business_units[0])
            self.current_unit = business_units[0]

        # Frame para gráficos con layout mejorado
        charts_frame = ctk.CTkFrame(parent, fg_color='transparent')
        charts_frame.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 15))
        charts_frame.grid_columnconfigure(0, weight=2)  # Gráfico de barras más grande
        charts_frame.grid_columnconfigure(1, weight=1)  # Gráfico de dona más pequeño
        charts_frame.grid_rowconfigure(0, weight=1)

        # Card para gráfico de barras agrupadas (izquierda, más grande)
        self.progreso_bar_card = MatplotlibChartCard(
            charts_frame,
            title='Progreso por Módulo - Comparativa'
        )
        self.progreso_bar_card.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        # Card para gráfico de dona ÚNICO Y DINÁMICO (derecha, más pequeño)
        self.progreso_donut_card = MatplotlibChartCard(
            charts_frame,
            title='Estado General TNG'  # Título inicial
        )
        self.progreso_donut_card.grid(row=0, column=1, sticky='nsew', padx=(10, 0))

        # Crear gráficos iniciales
        if business_units:
            self._update_progreso_charts(business_units[0])

    def _get_business_units_from_db(self):
        """Obtener lista de unidades de negocio desde la base de datos"""
        if not self.cursor:
            return []

        try:
            # Intentar obtener de la tabla UnidadDeNegocio
            self.cursor.execute("""
                SELECT DISTINCT NombreUnidad
                FROM UnidadDeNegocio
                WHERE NombreUnidad IS NOT NULL
                ORDER BY NombreUnidad
            """)
            units = [row[0] for row in self.cursor.fetchall()]

            # Si no hay resultados, intentar otras tablas comunes
            if not units:
                self.cursor.execute("""
                    SELECT DISTINCT Unidad
                    FROM Usuarios
                    WHERE Unidad IS NOT NULL AND Unidad != ''
                    ORDER BY Unidad
                """)
                units = [row[0] for row in self.cursor.fetchall()]

            return units if units else []

        except Exception as e:
            print(f"Error obteniendo unidades de negocio: {e}")
            return []

    def _on_unit_change(self, value):
        """Callback cuando cambia la unidad seleccionada"""
        self.current_unit = value
        self._update_progreso_charts(value)

    def _update_progreso_charts(self, unit):
        """Actualizar AMBOS gráficos según unidad (barras + dona dinámico)"""
        # Seleccionar datos
        if unit == 'TNG':
            data = DATOS_TNG
        elif unit == 'CONTAINER CARE':
            data = DATOS_CONTAINER_CARE
        else:  # ECV-EIT
            data = DATOS_ECV_EIT

        # ===== GRÁFICO DE BARRAS AGRUPADAS (izquierda) =====
        fig_bar = Figure(figsize=(10, 6))
        ax_bar = fig_bar.add_subplot(111)

        x = np.arange(len(data['modulos']))
        width = 0.25

        # Barras agrupadas
        bars1 = ax_bar.bar(x - width, data['sin_iniciar'], width,
                          label='Sin Iniciar', color=PRIMARY_COLORS['accent_red'],
                          edgecolor='none')
        bars2 = ax_bar.bar(x, data['en_proceso'], width,
                          label='En Proceso', color=PRIMARY_COLORS['accent_yellow'],
                          edgecolor='none')
        bars3 = ax_bar.bar(x + width, data['completado'], width,
                          label='Completado', color=PRIMARY_COLORS['accent_green'],
                          edgecolor='none')

        ax_bar.set_xlabel('Módulo', fontsize=11)
        ax_bar.set_ylabel('Número de Personas', fontsize=11)
        ax_bar.set_xticks(x)
        ax_bar.set_xticklabels(data['modulos'], fontsize=10)
        ax_bar.tick_params(labelsize=10)
        ax_bar.spines['top'].set_visible(False)
        ax_bar.spines['right'].set_visible(False)
        ax_bar.grid(axis='y', alpha=0.3)

        # Leyenda
        ax_bar.legend(
            loc='upper right',
            fontsize=10,
            frameon=True
        )

        fig_bar.tight_layout()
        self.progreso_bar_card.set_figure(fig_bar)

        # ===== GRÁFICO DE DONA DINÁMICO (derecha) =====
        # Calcular totales
        total_sin_iniciar = sum(data['sin_iniciar'])
        total_en_proceso = sum(data['en_proceso'])
        total_completado = sum(data['completado'])

        fig_donut = Figure(figsize=(7, 6))
        ax_donut = fig_donut.add_subplot(111)

        labels = ['Completado', 'En Proceso', 'Sin Iniciar']
        values = [total_completado, total_en_proceso, total_sin_iniciar]
        colors_donut = [
            PRIMARY_COLORS['accent_green'],
            PRIMARY_COLORS['accent_yellow'],
            PRIMARY_COLORS['accent_red']
        ]

        theme = self.theme_manager.get_current_theme()
        edge_color = theme['surface']

        wedges, texts, autotexts = ax_donut.pie(
            values,
            labels=labels,
            colors=colors_donut,
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.85,
            wedgeprops=dict(width=0.5, edgecolor=edge_color, linewidth=3)
        )

        # Estilo de textos
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_weight('bold')

        # Leyenda horizontal
        ax_donut.legend(
            wedges, labels,
            loc='upper center',
            bbox_to_anchor=(0.5, -0.05),
            ncol=3,
            fontsize=9,
            frameon=True
        )

        fig_donut.tight_layout()

        # Actualizar título dinámicamente
        if hasattr(self.progreso_donut_card, 'title_label'):
            self.progreso_donut_card.title_label.configure(
                text=f'Estado General {unit}'
            )

        self.progreso_donut_card.set_figure(fig_donut)

    # ==================== PESTAÑA COMPORTAMIENTO JERÁRQUICO ====================

    def _create_tab_comportamiento_jerarquico(self, parent):
        """Crear pestaña de Comportamiento Jerárquico"""
        # Card para gráfico de líneas
        jerarquico_line_card = MatplotlibChartCard(
            parent,
            title='Evolución de Población por Puesto'
        )
        jerarquico_line_card.grid(row=0, column=0, sticky='nsew', padx=(15, 10), pady=15)

        # Card para gráfico de barras comparativo
        jerarquico_bar_card = MatplotlibChartCard(
            parent,
            title='Comparativa M1 vs M8 - Retención por Puesto'
        )
        jerarquico_bar_card.grid(row=0, column=1, sticky='nsew', padx=(10, 15), pady=15)

        # Crear gráficos
        self._create_jerarquico_charts(jerarquico_line_card, jerarquico_bar_card)

    def _create_jerarquico_charts(self, line_card, bar_card):
        """Crear gráficos de comportamiento jerárquico"""
        # ===== GRÁFICO DE LÍNEAS =====
        fig_line = Figure(figsize=(10, 6))
        ax_line = fig_line.add_subplot(111)

        # Usar paleta ejecutiva Hutchison Ports para gráficos de líneas
        colors = EXECUTIVE_CHART_COLORS

        for idx, (puesto, poblacion) in enumerate(DATOS_JERARQUICO['puestos'].items()):
            theme = self.theme_manager.get_current_theme()
            edge_color = theme['surface']

            ax_line.plot(
                DATOS_JERARQUICO['fases'],
                poblacion,
                marker='o',
                markersize=6,
                linewidth=2,
                color=colors[idx % len(colors)],
                label=puesto,
                markeredgecolor=edge_color,
                markeredgewidth=1.5
            )

        ax_line.set_xlabel('Fase', fontsize=11)
        ax_line.set_ylabel('Población', fontsize=11)
        ax_line.tick_params(labelsize=10)
        ax_line.spines['top'].set_visible(False)
        ax_line.spines['right'].set_visible(False)
        ax_line.grid(axis='both', alpha=0.3)

        # Leyenda a la derecha
        ax_line.legend(
            loc='center left',
            bbox_to_anchor=(1.02, 0.5),
            fontsize=9,
            frameon=True
        )

        fig_line.tight_layout()
        line_card.set_figure(fig_line)

        # ===== GRÁFICO DE BARRAS COMPARATIVO =====
        puestos = list(DATOS_JERARQUICO['puestos'].keys())
        m1_values = [DATOS_JERARQUICO['puestos'][p][0] for p in puestos]
        m8_values = [DATOS_JERARQUICO['puestos'][p][7] for p in puestos]

        fig_bar = Figure(figsize=(10, 6))
        ax_bar = fig_bar.add_subplot(111)

        x = np.arange(len(puestos))
        width = 0.35

        bars1 = ax_bar.bar(x - width/2, m1_values, width,
                          label='M1 (Inicial)', color=PRIMARY_COLORS['accent_blue'],
                          edgecolor='none')
        bars2 = ax_bar.bar(x + width/2, m8_values, width,
                          label='M8 (Final)', color=PRIMARY_COLORS['accent_green'],
                          edgecolor='none')

        ax_bar.set_xlabel('Puesto', fontsize=11)
        ax_bar.set_ylabel('Población', fontsize=11)
        ax_bar.set_xticks(x)
        ax_bar.set_xticklabels(puestos, rotation=45, ha='right', fontsize=9)
        ax_bar.tick_params(labelsize=10)
        ax_bar.spines['top'].set_visible(False)
        ax_bar.spines['right'].set_visible(False)
        ax_bar.grid(axis='y', alpha=0.3)

        # Leyenda
        ax_bar.legend(
            loc='upper right',
            fontsize=10,
            frameon=True
        )

        fig_bar.tight_layout()
        bar_card.set_figure(fig_bar)

    # ==================== MÉTODOS DE DATOS ====================

    def _get_total_users(self):
        """Obtener total de usuarios"""
        if not self.cursor:
            return 1525  # Datos de ejemplo
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Instituto_Usuario")
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error obteniendo total de usuarios: {e}")
            return 1525

    def _get_active_modules(self):
        """Obtener número de módulos activos"""
        if not self.cursor:
            return 8  # Datos de ejemplo: 8 módulos activos
        try:
            self.cursor.execute("SELECT COUNT(DISTINCT IdModulo) FROM Instituto_ProgresoModulo")
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error obteniendo módulos activos: {e}")
            return 8

    def _get_completion_rate(self):
        """Obtener tasa de completado"""
        if not self.cursor:
            return 72.5  # Datos de ejemplo: 72.5% de completado
        try:
            self.cursor.execute("""
                SELECT
                    CAST(SUM(CASE WHEN EstatusModuloUsuario = 'Terminado' THEN 1 ELSE 0 END) AS FLOAT) * 100 /
                    NULLIF(COUNT(*), 0) as rate
                FROM Instituto_ProgresoModulo
            """)
            result = self.cursor.fetchone()
            return result[0] if result and result[0] else 0.0
        except Exception as e:
            print(f"Error obteniendo tasa de completado: {e}")
            return 72.5

    def _get_users_by_unit(self):
        """Obtener usuarios por unidad de negocio"""
        if not self.cursor:
            return [
                ('Operaciones Portuarias', 487),
                ('Logística y Almacenamiento', 364),
                ('Mantenimiento', 342),
                ('Administración', 231),
                ('Seguridad', 101)
            ]
        try:
            self.cursor.execute("""
                SELECT un.NombreUnidad, COUNT(u.UserId)
                FROM Instituto_Usuario u
                JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                GROUP BY un.IdUnidadDeNegocio, un.NombreUnidad
                ORDER BY COUNT(u.UserId) DESC
            """)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo usuarios por unidad: {e}")
            return [
                ('Operaciones Portuarias', 487),
                ('Logística y Almacenamiento', 364),
                ('Mantenimiento', 342),
                ('Administración', 231),
                ('Seguridad', 101)
            ]

    def refresh_all_data(self):
        """Refrescar todos los datos del dashboard"""
        # Resetear flags
        self._general_loaded = False
        self._progreso_loaded = False
        self._jerarquico_loaded = False
        self._interactivo_loaded = False

        # Recargar pestaña actual
        current_tab = self.tab_selector.get()
        self.on_tab_change(current_tab)

    # ==================== EXPORTAR A PDF ====================

    def export_dashboard_pdf(self):
        """Exportar dashboard actual a PDF"""
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        import tempfile
        import os
        from tkinter import messagebox

        try:
            # Crear carpeta reportes si no existe
            reports_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'reportes')
            os.makedirs(reports_folder, exist_ok=True)

            # Nombre del archivo con fecha
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_filename = os.path.join(reports_folder, f'Dashboard_Report_{timestamp}.pdf')

            # Crear documento PDF
            doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
            story = []

            # Estilos
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor(HUTCHISON_COLORS['ports_sky_blue']),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor(HUTCHISON_COLORS['ports_sky_blue']),
                spaceAfter=12,
                spaceBefore=12
            )

            # Título
            story.append(Paragraph("📊 Reporte Smart Reports", title_style))
            story.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
            story.append(Spacer(1, 0.3 * inch))

            # Obtener datos actuales
            total_users = self._get_total_users()
            active_modules = self._get_active_modules()
            completion_rate = self._get_completion_rate()

            # Métricas
            story.append(Paragraph("Métricas Generales", heading_style))

            metrics_data = [
                ['Métrica', 'Valor'],
                ['Total de Usuarios', f'{total_users:,}'],
                ['Módulos Activos', f'{active_modules}/14'],
                ['Tasa de Completado', f'{completion_rate:.1f}%']
            ]

            metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(HUTCHISON_COLORS['ports_sky_blue'])),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
            ]))

            story.append(metrics_table)
            story.append(Spacer(1, 0.5 * inch))

            # Guardar gráficos como imágenes temporales
            story.append(Paragraph("Gráficos de Análisis", heading_style))

            # Intentar guardar gráficos de matplotlib si están cargados
            temp_images = []

            if hasattr(self, 'progreso_bar_card') and self.progreso_bar_card.current_fig:
                try:
                    temp_img = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                    self.progreso_bar_card.current_fig.savefig(temp_img.name, dpi=150, bbox_inches='tight', facecolor='white')
                    temp_images.append(temp_img.name)

                    story.append(Paragraph("Progreso por Módulo - Comparativa", styles['Heading3']))
                    img = Image(temp_img.name, width=5*inch, height=3*inch)
                    story.append(img)
                    story.append(Spacer(1, 0.3 * inch))
                except Exception as e:
                    print(f"Error guardando gráfico de barras: {e}")

            if hasattr(self, 'progreso_donut_card') and self.progreso_donut_card.current_fig:
                try:
                    temp_img2 = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                    self.progreso_donut_card.current_fig.savefig(temp_img2.name, dpi=150, bbox_inches='tight', facecolor='white')
                    temp_images.append(temp_img2.name)

                    story.append(Paragraph(f"Estado General {self.current_unit}", styles['Heading3']))
                    img2 = Image(temp_img2.name, width=4*inch, height=3*inch)
                    story.append(img2)
                except Exception as e:
                    print(f"Error guardando gráfico de dona: {e}")

            # Construir PDF
            doc.build(story)

            # Limpiar archivos temporales
            for temp_img in temp_images:
                try:
                    os.remove(temp_img)
                except:
                    pass

            messagebox.showinfo(
                "Exportación Exitosa",
                f"El reporte ha sido exportado exitosamente a:\n\n{pdf_filename}"
            )

            # Abrir el PDF
            os.startfile(pdf_filename)

        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar a PDF:\n{str(e)}")
            print(f"Error detallado: {e}")

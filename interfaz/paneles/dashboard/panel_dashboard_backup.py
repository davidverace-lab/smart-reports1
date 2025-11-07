"""
Panel ModernDashboard - Dashboard optimizado con lazy loading y pestañas
"""
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from interfaz.componentes.visualizacion.tarjeta_grafico_matplotlib import MatplotlibChartCard
from interfaz.componentes.visualizacion.tarjeta_metrica import MetricCard
from nucleo.configuracion.ajustes import HUTCHISON_COLORS, EXECUTIVE_CHART_COLORS


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
        super().__init__(parent, fg_color='#1a1d2e', **kwargs)
        self.db = db_connection
        self.cursor = db_connection.cursor() if db_connection else None

        # Flags para lazy loading (según especificación)
        self._general_loaded = False
        self._progreso_loaded = False
        self._jerarquico_loaded = False

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
        """Crear contenedor con pestañas"""
        # Frame principal con padding
        main_frame = ctk.CTkFrame(self, fg_color='transparent')
        main_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(main_frame, fg_color='transparent', height=60)
        header.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        header.grid_propagate(False)

        title = ctk.CTkLabel(
            header,
            text='📊 Panel de Control',
            font=('Montserrat', 28, 'bold'),
            text_color='#ffffff',
            anchor='w'
        )
        title.pack(side='left')

        # Botón Exportar a PDF
        export_pdf_btn = ctk.CTkButton(
            header,
            text='📄 Exportar a PDF',
            font=('Montserrat', 14, 'bold'),
            fg_color=PRIMARY_COLORS['accent_green'],
            hover_color='#40b656',
            corner_radius=10,
            height=40,
            width=180,
            command=self.export_dashboard_pdf
        )
        export_pdf_btn.pack(side='right', padx=10)

        # TabView
        self.tabview = ctk.CTkTabview(
            main_frame,
            fg_color='#2b2d42',
            segmented_button_fg_color='#1a1d2e',
            segmented_button_selected_color=PRIMARY_COLORS['accent_blue'],
            segmented_button_selected_hover_color='#5a52d5',
            segmented_button_unselected_color='#2b2d42',
            segmented_button_unselected_hover_color='#3a3d5c',
            corner_radius=15,
            command=self.on_tab_change
        )
        self.tabview.grid(row=1, column=0, sticky='nsew')

        # Crear pestañas (ORDEN: General, Progreso, Jerárquico)
        self.tab_general = self.tabview.add("📈 General")
        self.tab_progreso = self.tabview.add("📊 Progreso por Módulo")
        self.tab_jerarquico = self.tabview.add("👔 Comportamiento Jerárquico")

        # Configurar grids de las pestañas
        self.tab_general.grid_columnconfigure(0, weight=1)
        self.tab_general.grid_rowconfigure((0, 1), weight=1)

        self.tab_progreso.grid_columnconfigure(0, weight=1)
        self.tab_progreso.grid_rowconfigure(1, weight=1)

        self.tab_jerarquico.grid_columnconfigure((0, 1), weight=1)
        self.tab_jerarquico.grid_rowconfigure(0, weight=1)

    def on_tab_change(self):
        """Callback cuando cambia la pestaña - Lazy loading"""
        current_tab = self.tabview.get()

        if current_tab == "📈 General" and not self._general_loaded:
            self.load_general_charts()
            self._general_loaded = True
        elif current_tab == "📊 Progreso por Módulo" and not self._progreso_loaded:
            self.load_progreso_charts()
            self._progreso_loaded = True
        elif current_tab == "👔 Comportamiento Jerárquico" and not self._jerarquico_loaded:
            self.load_jerarquico_charts()
            self._jerarquico_loaded = True

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
            fig1 = Figure(figsize=(8, 5), facecolor='#1a1d2e')
            ax1 = fig1.add_subplot(111)
            ax1.set_facecolor('#1a1d2e')

            bars = ax1.barh(units, counts, color=colors, edgecolor='none')
            ax1.set_xlabel('Número de Usuarios', fontsize=11, color='#a0a0b0')
            ax1.set_ylabel('', fontsize=11, color='#a0a0b0')
            ax1.tick_params(colors='#a0a0b0', labelsize=10)
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['left'].set_color('#3a3d5c')
            ax1.spines['bottom'].set_color('#3a3d5c')
            ax1.grid(axis='x', alpha=0.3, color='#3a3d5c')

            # Añadir valores en las barras
            for bar in bars:
                width = bar.get_width()
                ax1.text(width, bar.get_y() + bar.get_height()/2,
                        f'{int(width)}',
                        ha='left', va='center', fontsize=9, color='#ffffff',
                        fontweight='bold', pad=5)

            fig1.tight_layout()
            chart1.set_figure(fig1)

            # Gráfico 2: Donut
            fig2 = Figure(figsize=(8, 5), facecolor='#1a1d2e')
            ax2 = fig2.add_subplot(111)
            ax2.set_facecolor('#1a1d2e')

            wedges, texts, autotexts = ax2.pie(
                counts,
                labels=units,
                colors=colors,
                autopct='%1.1f%%',
                startangle=90,
                pctdistance=0.85,
                wedgeprops=dict(width=0.5, edgecolor='#1a1d2e', linewidth=3)
            )

            # Estilo de textos
            for text in texts:
                text.set_color('#a0a0b0')
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
                frameon=True,
                facecolor='#2b2d42',
                edgecolor='#3a3d5c'
            )

            fig2.tight_layout()
            chart2.set_figure(fig2)

    # ==================== PESTAÑA PROGRESO POR MÓDULO ====================

    def _create_tab_progreso_modulo(self, parent):
        """Crear pestaña de Progreso por Módulo con gráfico dinámico"""
        # Frame para selector
        selector_frame = ctk.CTkFrame(parent, fg_color='transparent')
        selector_frame.grid(row=0, column=0, sticky='ew', padx=15, pady=(15, 10))

        label = ctk.CTkLabel(
            selector_frame,
            text='Seleccionar Unidad de Negocio:',
            font=('Montserrat', 14, 'bold'),
            text_color='#ffffff'
        )
        label.pack(side='left', padx=(0, 15))

        # Segmented button para seleccionar unidad
        self.unit_selector = ctk.CTkSegmentedButton(
            selector_frame,
            values=['TNG', 'CONTAINER CARE', 'ECV-EIT'],
            font=('Montserrat', 12, 'bold'),
            fg_color='#3a3d5c',
            selected_color=PRIMARY_COLORS['accent_blue'],
            selected_hover_color='#5a52d5',
            unselected_color='#2b2d42',
            unselected_hover_color='#3a3d5c',
            command=self._on_unit_change
        )
        self.unit_selector.pack(side='left')
        self.unit_selector.set('TNG')
        self.current_unit = 'TNG'

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
        self._update_progreso_charts('TNG')

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
        fig_bar = Figure(figsize=(10, 6), facecolor='#1a1d2e')
        ax_bar = fig_bar.add_subplot(111)
        ax_bar.set_facecolor('#1a1d2e')

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

        ax_bar.set_xlabel('Módulo', fontsize=11, color='#a0a0b0')
        ax_bar.set_ylabel('Número de Personas', fontsize=11, color='#a0a0b0')
        ax_bar.set_xticks(x)
        ax_bar.set_xticklabels(data['modulos'], fontsize=10, color='#a0a0b0')
        ax_bar.tick_params(colors='#a0a0b0', labelsize=10)
        ax_bar.spines['top'].set_visible(False)
        ax_bar.spines['right'].set_visible(False)
        ax_bar.spines['left'].set_color('#3a3d5c')
        ax_bar.spines['bottom'].set_color('#3a3d5c')
        ax_bar.grid(axis='y', alpha=0.3, color='#3a3d5c')

        # Leyenda
        ax_bar.legend(
            loc='upper right',
            fontsize=10,
            frameon=True,
            facecolor='#2b2d42',
            edgecolor='#3a3d5c'
        )

        fig_bar.tight_layout()
        self.progreso_bar_card.set_figure(fig_bar)

        # ===== GRÁFICO DE DONA DINÁMICO (derecha) =====
        # Calcular totales
        total_sin_iniciar = sum(data['sin_iniciar'])
        total_en_proceso = sum(data['en_proceso'])
        total_completado = sum(data['completado'])

        fig_donut = Figure(figsize=(7, 6), facecolor='#1a1d2e')
        ax_donut = fig_donut.add_subplot(111)
        ax_donut.set_facecolor('#1a1d2e')

        labels = ['Completado', 'En Proceso', 'Sin Iniciar']
        values = [total_completado, total_en_proceso, total_sin_iniciar]
        colors_donut = [
            PRIMARY_COLORS['accent_green'],
            PRIMARY_COLORS['accent_yellow'],
            PRIMARY_COLORS['accent_red']
        ]

        wedges, texts, autotexts = ax_donut.pie(
            values,
            labels=labels,
            colors=colors_donut,
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.85,
            wedgeprops=dict(width=0.5, edgecolor='#1a1d2e', linewidth=3)
        )

        # Estilo de textos
        for text in texts:
            text.set_color('#a0a0b0')
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
            frameon=True,
            facecolor='#2b2d42',
            edgecolor='#3a3d5c'
        )

        fig_donut.tight_layout()

        # Actualizar título dinámicamente
        self.progreso_donut_card.winfo_children()[0].winfo_children()[0].configure(
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
        fig_line = Figure(figsize=(10, 6), facecolor='#1a1d2e')
        ax_line = fig_line.add_subplot(111)
        ax_line.set_facecolor('#1a1d2e')

        # Usar paleta ejecutiva Hutchison Ports para gráficos de líneas
        colors = EXECUTIVE_CHART_COLORS

        for idx, (puesto, poblacion) in enumerate(DATOS_JERARQUICO['puestos'].items()):
            ax_line.plot(
                DATOS_JERARQUICO['fases'],
                poblacion,
                marker='o',
                markersize=6,
                linewidth=2,
                color=colors[idx % len(colors)],
                label=puesto,
                markeredgecolor='#1a1d2e',
                markeredgewidth=1.5
            )

        ax_line.set_xlabel('Fase', fontsize=11, color='#a0a0b0')
        ax_line.set_ylabel('Población', fontsize=11, color='#a0a0b0')
        ax_line.tick_params(colors='#a0a0b0', labelsize=10)
        ax_line.spines['top'].set_visible(False)
        ax_line.spines['right'].set_visible(False)
        ax_line.spines['left'].set_color('#3a3d5c')
        ax_line.spines['bottom'].set_color('#3a3d5c')
        ax_line.grid(axis='both', alpha=0.3, color='#3a3d5c')

        # Leyenda a la derecha
        ax_line.legend(
            loc='center left',
            bbox_to_anchor=(1.02, 0.5),
            fontsize=9,
            frameon=True,
            facecolor='#2b2d42',
            edgecolor='#3a3d5c'
        )

        fig_line.tight_layout()
        line_card.set_figure(fig_line)

        # ===== GRÁFICO DE BARRAS COMPARATIVO =====
        puestos = list(DATOS_JERARQUICO['puestos'].keys())
        m1_values = [DATOS_JERARQUICO['puestos'][p][0] for p in puestos]
        m8_values = [DATOS_JERARQUICO['puestos'][p][7] for p in puestos]

        fig_bar = Figure(figsize=(10, 6), facecolor='#1a1d2e')
        ax_bar = fig_bar.add_subplot(111)
        ax_bar.set_facecolor('#1a1d2e')

        x = np.arange(len(puestos))
        width = 0.35

        bars1 = ax_bar.bar(x - width/2, m1_values, width,
                          label='M1 (Inicial)', color=PRIMARY_COLORS['accent_blue'],
                          edgecolor='none')
        bars2 = ax_bar.bar(x + width/2, m8_values, width,
                          label='M8 (Final)', color=PRIMARY_COLORS['accent_green'],
                          edgecolor='none')

        ax_bar.set_xlabel('Puesto', fontsize=11, color='#a0a0b0')
        ax_bar.set_ylabel('Población', fontsize=11, color='#a0a0b0')
        ax_bar.set_xticks(x)
        ax_bar.set_xticklabels(puestos, rotation=45, ha='right', fontsize=9, color='#a0a0b0')
        ax_bar.tick_params(colors='#a0a0b0', labelsize=10)
        ax_bar.spines['top'].set_visible(False)
        ax_bar.spines['right'].set_visible(False)
        ax_bar.spines['left'].set_color('#3a3d5c')
        ax_bar.spines['bottom'].set_color('#3a3d5c')
        ax_bar.grid(axis='y', alpha=0.3, color='#3a3d5c')

        # Leyenda
        ax_bar.legend(
            loc='upper right',
            fontsize=10,
            frameon=True,
            facecolor='#2b2d42',
            edgecolor='#3a3d5c'
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
            return 0  # Datos de ejemplo
        try:
            self.cursor.execute("SELECT COUNT(DISTINCT IdModulo) FROM Instituto_ProgresoModulo")
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error obteniendo módulos activos: {e}")
            return 0

    def _get_completion_rate(self):
        """Obtener tasa de completado"""
        if not self.cursor:
            return 0.0  # Datos de ejemplo
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
            return 0.0

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

        # Recargar pestaña actual
        self.on_tab_change()

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
                textColor=colors.HexColor('#6c63ff'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#6c63ff'),
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
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6c63ff')),
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

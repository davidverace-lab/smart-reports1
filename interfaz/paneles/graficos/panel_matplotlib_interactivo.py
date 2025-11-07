"""
Panel de gráficos interactivos - Matplotlib embebido optimizado
ACTUALIZADO: Gráficos embebidos directamente (sin botones ni ventanas externas)
"""
import customtkinter as ctk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from interfaz.componentes.visualizacion.tarjeta_grafico_optimizado import OptimizedChartCard
from nucleo.configuracion.ajustes import HUTCHISON_COLORS, EXECUTIVE_CHART_COLORS
from nucleo.configuracion.gestor_temas import get_theme_manager


class MatplotlibInteractivePanel(ctk.CTkFrame):
    """Panel con gráficos matplotlib embebidos optimizados"""

    def __init__(self, parent, db_connection, **kwargs):
        """
        Args:
            parent: Widget padre
            db_connection: Conexión a la base de datos
        """
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(parent, fg_color='transparent', **kwargs)
        self.db = db_connection
        self.cursor = db_connection.cursor() if db_connection else None

        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Crear header
        self._create_header()

        # Crear scroll frame para gráficos
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        self.scroll_frame.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 15))

        # Cargar gráficos
        self.after(100, self.create_chart_cards)

    def _create_header(self):
        """Crear header del panel"""
        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent', height=80)
        header.grid(row=0, column=0, sticky='ew', padx=15, pady=(15, 10))
        header.grid_propagate(False)

        title = ctk.CTkLabel(
            header,
            text='📊 Gráficos Interactivos',
            font=('Montserrat', 28, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        title.pack(side='left', pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text='Visualiza datos de forma rápida y clara • Botón 🚀 D3.js para versión interactiva',
            font=('Montserrat', 13),
            text_color=theme['text_secondary'],
            anchor='w'
        )
        subtitle.pack(side='left', padx=(20, 0))

    def create_chart_cards(self):
        """Crear cards con gráficos matplotlib embebidos"""
        # Configurar grid del scroll frame (2 columnas)
        self.scroll_frame.grid_columnconfigure((0, 1), weight=1)

        # === Card 1: Gráfico de Líneas ===
        chart1 = OptimizedChartCard(
            self.scroll_frame,
            title='Tendencias de Progreso por Módulo'
        )
        chart1.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # === Card 2: Barras Apiladas ===
        chart2 = OptimizedChartCard(
            self.scroll_frame,
            title='Distribución por Estado y Módulo'
        )
        chart2.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        # === Card 3: Scatter / Correlación ===
        chart3 = OptimizedChartCard(
            self.scroll_frame,
            title='Análisis de Correlación - Progreso vs Tiempo'
        )
        chart3.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # === Card 4: Barras Comparativas ===
        chart4 = OptimizedChartCard(
            self.scroll_frame,
            title='Comparativa de Unidades de Negocio'
        )
        chart4.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        # Crear los gráficos
        self._create_charts(chart1, chart2, chart3, chart4)

    def _create_charts(self, chart1, chart2, chart3, chart4):
        """Crear gráficos matplotlib"""

        # === GRÁFICO 1: Líneas ===
        modulos = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']
        x = np.arange(len(modulos))

        fig1 = Figure(figsize=(8, 5), dpi=90)
        ax1 = fig1.add_subplot(111)

        # Series de datos
        unidades = ['TNG', 'Container Care', 'ECV-EIT', 'Operaciones']
        datos_series = [
            [100, 98, 95, 93, 90, 88, 85, 82],
            [90, 88, 85, 82, 80, 78, 75, 72],
            [85, 83, 80, 78, 75, 73, 70, 68],
            [80, 78, 75, 72, 70, 68, 65, 62]
        ]

        for i, (unidad, datos) in enumerate(zip(unidades, datos_series)):
            color = EXECUTIVE_CHART_COLORS[i % len(EXECUTIVE_CHART_COLORS)]
            ax1.plot(x, datos, marker='o', label=unidad, color=color,
                   linewidth=2.5, markersize=7, markeredgewidth=1.5,
                   markeredgecolor='white')

        ax1.set_xlabel('Módulo', fontsize=11, fontfamily='Montserrat', fontweight='bold')
        ax1.set_ylabel('Progreso (%)', fontsize=11, fontfamily='Montserrat', fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(modulos)
        ax1.legend(loc='best', fontsize=10, framealpha=0.9)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)

        fig1.tight_layout()

        d3_data1 = {
            'type': 'line',
            'x': modulos,
            'series': [
                {'name': u, 'values': d} for u, d in zip(unidades, datos_series)
            ],
            'subtitulo': 'Evolución del progreso • Clic en 🚀 para D3.js interactivo'
        }
        chart1.set_figure(fig1, d3_data=d3_data1)

        # === GRÁFICO 2: Barras (simula apiladas) ===
        modulos2 = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']
        completado = [120, 135, 140, 138, 142, 145, 148, 150]

        fig2 = Figure(figsize=(8, 5), dpi=90)
        ax2 = fig2.add_subplot(111)

        bars = ax2.bar(modulos2, completado, color=HUTCHISON_COLORS['success'], edgecolor='none', width=0.6)

        ax2.set_xlabel('Módulo', fontsize=11, fontfamily='Montserrat', fontweight='bold')
        ax2.set_ylabel('Usuarios Completados', fontsize=11, fontfamily='Montserrat', fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        # Valores encima de barras
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2, height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9,
                    fontweight='bold')

        fig2.tight_layout()

        d3_data2 = {
            'type': 'bar',
            'labels': modulos2,
            'values': completado,
            'subtitulo': 'Usuarios que completaron cada módulo • Clic en 🚀 para D3.js'
        }
        chart2.set_figure(fig2, d3_data=d3_data2)

        # === GRÁFICO 3: Scatter / Correlación ===
        dias_rangos = ['0-15', '16-30', '31-45', '46-60', '60+']
        usuarios = [45, 78, 92, 65, 35]

        fig3 = Figure(figsize=(8, 5), dpi=90)
        ax3 = fig3.add_subplot(111)

        bars = ax3.bar(dias_rangos, usuarios, color=HUTCHISON_COLORS['ports_horizon_blue'], edgecolor='none', width=0.6)

        ax3.set_xlabel('Días de Progreso', fontsize=11, fontfamily='Montserrat', fontweight='bold')
        ax3.set_ylabel('Número de Usuarios', fontsize=11, fontfamily='Montserrat', fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)

        # Valores encima de barras
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2, height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9,
                    fontweight='bold')

        fig3.tight_layout()

        d3_data3 = {
            'type': 'bar',
            'labels': dias_rangos,
            'values': usuarios,
            'subtitulo': 'Distribución de usuarios por tiempo • Clic en 🚀 para D3.js'
        }
        chart3.set_figure(fig3, d3_data=d3_data3)

        # === GRÁFICO 4: Comparativa de Unidades ===
        unidades_comp = ['TNG', 'Container\nCare', 'ECV-EIT', 'Operaciones', 'Logística']
        progreso_prom = [90, 78, 75, 68, 62]

        fig4 = Figure(figsize=(8, 5), dpi=90)
        ax4 = fig4.add_subplot(111)

        colors4 = [EXECUTIVE_CHART_COLORS[i % len(EXECUTIVE_CHART_COLORS)] for i in range(len(unidades_comp))]
        bars = ax4.barh(unidades_comp, progreso_prom, color=colors4, edgecolor='none')

        ax4.set_xlabel('Progreso Promedio (%)', fontsize=11, fontfamily='Montserrat', fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='x', linestyle='--')
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)

        # Valores al final de barras
        for bar in bars:
            width = bar.get_width()
            ax4.text(width + 1, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}%',
                    ha='left', va='center', fontsize=9,
                    fontweight='bold')

        fig4.tight_layout()

        d3_data4 = {
            'type': 'bar',
            'labels': ['TNG', 'Container Care', 'ECV-EIT', 'Operaciones', 'Logística'],
            'values': progreso_prom,
            'subtitulo': 'Progreso promedio por unidad • Clic en 🚀 para D3.js'
        }
        chart4.set_figure(fig4, d3_data=d3_data4)

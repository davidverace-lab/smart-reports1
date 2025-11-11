"""
Panel de gráficos interactivos D3.js embebidos
ACTUALIZADO: Gráficos D3.js profesionales con múltiples fallbacks
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.charts.tarjeta_d3_profesional import ProfessionalD3ChartCard
from config.themes import HUTCHISON_COLORS, EXECUTIVE_CHART_COLORS
from config.gestor_temas import get_theme_manager


class MatplotlibInteractivePanel(ctk.CTkFrame):
    """Panel con gráficos D3.js embebidos directamente"""

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
            text='📊 Gráficos Interactivos D3.js',
            font=('Montserrat', 28, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        title.pack(side='left', pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text='Gráficos D3.js embebidos directamente en la aplicación • 100% interactivos',
            font=('Montserrat', 13),
            text_color=theme['text_secondary'],
            anchor='w'
        )
        subtitle.pack(side='left', padx=(20, 0))

    def create_chart_cards(self):
        """Crear cards con gráficos D3.js embebidos"""
        # Configurar grid del scroll frame (2 columnas)
        self.scroll_frame.grid_columnconfigure((0, 1), weight=1)

        # === Card 1: Gráfico de Líneas ===
        chart1 = ProfessionalD3ChartCard(
            self.scroll_frame,
            title='📈 Tendencias de Progreso por Módulo'
        )
        chart1.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # === Card 2: Barras ===
        chart2 = ProfessionalD3ChartCard(
            self.scroll_frame,
            title='📊 Distribución por Estado y Módulo'
        )
        chart2.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        # === Card 3: Análisis ===
        chart3 = ProfessionalD3ChartCard(
            self.scroll_frame,
            title='🎯 Análisis de Correlación - Progreso vs Tiempo'
        )
        chart3.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # === Card 4: Donut ===
        chart4 = ProfessionalD3ChartCard(
            self.scroll_frame,
            title='🍩 Comparativa de Unidades de Negocio'
        )
        chart4.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        # Crear los gráficos D3.js
        self._create_d3_charts(chart1, chart2, chart3, chart4)

    def _create_d3_charts(self, chart1, chart2, chart3, chart4):
        """Crear gráficos D3.js embebidos"""

        # === GRÁFICO 1: Líneas ===
        chart1.set_d3_chart(
            chart_type='line',
            datos={
                'x': ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'],
                'series': [
                    {'name': 'TNG', 'values': [100, 98, 95, 93, 90, 88, 85, 82]},
                    {'name': 'Container Care', 'values': [90, 88, 85, 82, 80, 78, 75, 72]},
                    {'name': 'ECV-EIT', 'values': [85, 83, 80, 78, 75, 73, 70, 68]},
                    {'name': 'Operaciones', 'values': [80, 78, 75, 72, 70, 68, 65, 62]}
                ]
            },
            subtitulo='Evolución del progreso por módulo • Múltiples series'
        )

        # === GRÁFICO 2: Barras ===
        chart2.set_d3_chart(
            chart_type='bar',
            datos={
                'labels': ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'],
                'values': [120, 135, 140, 138, 142, 145, 148, 150]
            },
            subtitulo='Usuarios que completaron cada módulo • Estado: Terminado'
        )

        # === GRÁFICO 3: Análisis de Correlación ===
        chart3.set_d3_chart(
            chart_type='bar',
            datos={
                'labels': ['0-15', '16-30', '31-45', '46-60', '60+'],
                'values': [45, 78, 92, 65, 35]
            },
            subtitulo='Distribución de usuarios por tiempo de progreso (días)'
        )

        # === GRÁFICO 4: Donut ===
        chart4.set_d3_chart(
            chart_type='donut',
            datos={
                'labels': ['TNG - 90%', 'Container Care - 78%', 'ECV-EIT - 75%',
                          'Operaciones - 68%', 'Logística - 62%'],
                'values': [90, 78, 75, 68, 62]
            },
            subtitulo='Progreso promedio por unidad de negocio'
        )

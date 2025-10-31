"""
Panel de Ejemplos de Gráficos - Muestra todos los tipos de gráficos disponibles
"""
import customtkinter as ctk
from smart_reports.ui.components.chart_card import ChartCard


class ChartExamplesPanel(ctk.CTkFrame):
    """Panel que muestra ejemplos de todos los tipos de gráficos con datos inventados"""

    def __init__(self, parent, **kwargs):
        """
        Args:
            parent: Widget padre
        """
        super().__init__(parent, fg_color='#1a1d2e', **kwargs)

        # Configurar grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Crear contenido scrollable
        self._create_scrollable_content()

    def _create_scrollable_content(self):
        """Crear contenedor scrollable para los ejemplos"""
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent',
            scrollbar_button_color='#3a3d5c',
            scrollbar_button_hover_color='#4a4d6c'
        )
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        scroll_frame.grid_columnconfigure((0, 1), weight=1)

        # Header
        self._create_header(scroll_frame)

        # Row 1: Bar Charts
        self._create_bar_charts_row(scroll_frame)

        # Row 2: Donut and Line Charts
        self._create_donut_line_row(scroll_frame)

        # Row 3: Area and Stacked Bar Charts
        self._create_area_stacked_row(scroll_frame)

    def _create_header(self, parent):
        """Crear header con título"""
        header = ctk.CTkFrame(parent, fg_color='transparent', height=80)
        header.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        header.grid_propagate(False)

        # Título
        title = ctk.CTkLabel(
            header,
            text='📊 Ejemplos de Gráficos Interactivos',
            font=('Segoe UI', 32, 'bold'),
            text_color='#ffffff',
            anchor='w'
        )
        title.pack(side='left')

        # Descripción
        desc = ctk.CTkLabel(
            header,
            text='Explora los diferentes tipos de gráficos con datos de ejemplo',
            font=('Segoe UI', 14),
            text_color='#a0a0b0',
            anchor='w'
        )
        desc.pack(side='left', padx=20)

    def _create_bar_charts_row(self, parent):
        """Crear fila con gráficos de barras"""
        # Datos de ejemplo: Ventas por mes
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']
        ventas = [45000, 52000, 48000, 61000, 55000, 67000]

        # Card 1: Barras verticales
        chart1 = ChartCard(parent, '📊 Ventas Mensuales (Barras Verticales)', 'bar', height=350)
        chart1.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        chart1.create_chart(ventas, meses)

        # Datos de ejemplo: Productos más vendidos
        productos = ['Laptop Dell', 'iPhone 14', 'Samsung S23', 'iPad Pro', 'AirPods']
        cantidades = [234, 312, 198, 167, 289]

        # Card 2: Barras horizontales
        chart2 = ChartCard(parent, '🏆 Top 5 Productos (Barras Horizontales)', 'horizontal_bar', height=350)
        chart2.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)
        chart2.create_chart(cantidades, productos)

    def _create_donut_line_row(self, parent):
        """Crear fila con donut y líneas"""
        # Datos de ejemplo: Distribución de clientes por región
        regiones = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
        clientes = [450, 320, 280, 190, 260]

        # Card 1: Donut chart
        chart1 = ChartCard(parent, '🍩 Clientes por Región (Donut)', 'donut', height=350)
        chart1.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        chart1.create_chart(clientes, regiones)

        # Datos de ejemplo: Evolución de usuarios activos
        trimestres = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024', 'Q2 2024']
        usuarios = [1200, 1450, 1680, 1920, 2150, 2380]

        # Card 2: Line chart
        chart2 = ChartCard(parent, '📈 Crecimiento de Usuarios (Línea)', 'line', height=350)
        chart2.grid(row=2, column=1, sticky='nsew', padx=10, pady=10)
        chart2.create_chart(usuarios, trimestres)

    def _create_area_stacked_row(self, parent):
        """Crear fila con area y stacked bar"""
        # Datos de ejemplo: Ingresos anuales
        años = ['2019', '2020', '2021', '2022', '2023', '2024']
        ingresos = [850000, 920000, 1050000, 1180000, 1320000, 1450000]

        # Card 1: Area chart
        chart1 = ChartCard(parent, '💰 Evolución de Ingresos (Área)', 'area', height=350)
        chart1.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        chart1.create_chart(ingresos, años)

        # Datos de ejemplo: Estado de proyectos
        proyectos = ['Proyecto A', 'Proyecto B', 'Proyecto C', 'Proyecto D', 'Proyecto E']
        completados = [12, 18, 15, 22, 20]
        en_progreso = [5, 8, 10, 6, 9]
        pendientes = [3, 4, 5, 2, 6]

        # Card 2: Stacked bar chart
        chart2 = ChartCard(parent, '📊 Estado de Proyectos (Barras Apiladas)', 'stacked_bar', height=350)
        chart2.grid(row=3, column=1, sticky='nsew', padx=10, pady=10)
        chart2.create_chart(completados, proyectos, en_progreso, pendientes)

        # Información adicional
        info_frame = ctk.CTkFrame(parent, fg_color='#2b2d42', corner_radius=15, border_width=1, border_color='#3a3d5c')
        info_frame.grid(row=4, column=0, columnspan=2, sticky='ew', padx=10, pady=20)

        info_title = ctk.CTkLabel(
            info_frame,
            text='💡 Características de los Gráficos',
            font=('Segoe UI', 20, 'bold'),
            text_color='#ffffff'
        )
        info_title.pack(padx=20, pady=(15, 10), anchor='w')

        features = [
            '✅ Interactividad completa con zoom y pan',
            '✅ Tooltips informativos al pasar el mouse',
            '✅ Exportación a PNG, JPG, SVG y PDF',
            '✅ Tema oscuro optimizado para la aplicación',
            '✅ Apertura en navegador para análisis detallado',
            '✅ Colores modernos y profesionales'
        ]

        for feature in features:
            feature_label = ctk.CTkLabel(
                info_frame,
                text=feature,
                font=('Segoe UI', 13),
                text_color='#a0a0b0',
                anchor='w'
            )
            feature_label.pack(padx=30, pady=3, anchor='w')

        # Espaciado final
        ctk.CTkLabel(info_frame, text='').pack(pady=10)

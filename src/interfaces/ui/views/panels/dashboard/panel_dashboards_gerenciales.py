"""
Panel de Dashboards Gerenciales - Exploración Completa D3.js
Muestra TODAS las capacidades de visualización de datos
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.charts.tarjeta_d3_profesional import ProfessionalD3ChartCard
from src.interfaces.ui.views.components.navigation.boton_pestana import CustomTabView
from config.gestor_temas import get_theme_manager


class DashboardsGerencialesPanel(ctk.CTkFrame):
    """Panel con múltiples dashboards gerenciales usando D3.js"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.theme_manager = get_theme_manager()

        # Header
        self._create_header()

        # Tabs para diferentes categorías
        self.tab_view = CustomTabView(self)
        self.tab_view.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Crear pestañas por categoría
        self.tab_rendimiento = self.tab_view.add("📊 Rendimiento", "📊")
        self.tab_comparativas = self.tab_view.add("📈 Comparativas", "📈")
        self.tab_distribucion = self.tab_view.add("🍩 Distribución", "🍩")
        self.tab_tendencias = self.tab_view.add("📉 Tendencias", "📉")
        self.tab_relaciones = self.tab_view.add("🔵 Relaciones", "🔵")

        # Llenar cada pestaña
        self._create_rendimiento_dashboard()
        self._create_comparativas_dashboard()
        self._create_distribucion_dashboard()
        self._create_tendencias_dashboard()
        self._create_relaciones_dashboard()

        # Cargar datos
        self.after(500, self._load_all_data)

    def _create_header(self):
        """Crear header del panel"""
        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent', height=80)
        header.pack(fill='x', padx=20, pady=(20, 15))
        header.pack_propagate(False)

        # Título
        title = ctk.CTkLabel(
            header,
            text="📊 Dashboards Gerenciales - Visualización Completa D3.js",
            font=('Montserrat', 24, 'bold'),
            text_color=theme['text']
        )
        title.pack(side='left', anchor='w')

        # Badge
        badge = ctk.CTkLabel(
            header,
            text='D3.js Interactivo ⚡',
            font=('Montserrat', 12, 'bold'),
            fg_color='#51cf66',
            text_color='white',
            corner_radius=8,
            padx=15,
            height=30
        )
        badge.pack(side='right', anchor='e', padx=10)

    def _create_rendimiento_dashboard(self):
        """Dashboard de Rendimiento - Barras y Gauges"""
        # Configurar grid
        self.tab_rendimiento.grid_columnconfigure(0, weight=1)
        self.tab_rendimiento.grid_columnconfigure(1, weight=1)
        self.tab_rendimiento.grid_rowconfigure(0, weight=1)
        self.tab_rendimiento.grid_rowconfigure(1, weight=1)

        # Gráfico 1: Barras verticales por unidad
        self.chart_barras_unidad = ProfessionalD3ChartCard(
            self.tab_rendimiento,
            title="📊 Rendimiento por Unidad de Negocio",
            width=650,
            height=400
        )
        self.chart_barras_unidad.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 2: Barras horizontales por departamento
        self.chart_barras_depto = ProfessionalD3ChartCard(
            self.tab_rendimiento,
            title="📊 Top 10 Departamentos",
            width=650,
            height=400
        )
        self.chart_barras_depto.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Gráfico 3: Barras apiladas por mes
        self.chart_barras_apiladas = ProfessionalD3ChartCard(
            self.tab_rendimiento,
            title="📊 Progreso Mensual Acumulado",
            width=650,
            height=400
        )
        self.chart_barras_apiladas.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 4: Barras agrupadas
        self.chart_barras_agrupadas = ProfessionalD3ChartCard(
            self.tab_rendimiento,
            title="📊 Comparativa Trimestral",
            width=650,
            height=400
        )
        self.chart_barras_agrupadas.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def _create_comparativas_dashboard(self):
        """Dashboard de Comparativas - Múltiples series"""
        self.tab_comparativas.grid_columnconfigure(0, weight=1)
        self.tab_comparativas.grid_columnconfigure(1, weight=1)
        self.tab_comparativas.grid_rowconfigure(0, weight=1)
        self.tab_comparativas.grid_rowconfigure(1, weight=1)

        # Gráfico 1: Líneas múltiples (6 unidades)
        self.chart_lineas_multi = ProfessionalD3ChartCard(
            self.tab_comparativas,
            title="📈 Tendencia de Cumplimiento por Unidad",
            width=650,
            height=400
        )
        self.chart_lineas_multi.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 2: Área apilada
        self.chart_area_apilada = ProfessionalD3ChartCard(
            self.tab_comparativas,
            title="📈 Distribución de Estatus en el Tiempo",
            width=650,
            height=400
        )
        self.chart_area_apilada.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Gráfico 3: Líneas con área
        self.chart_lineas_area = ProfessionalD3ChartCard(
            self.tab_comparativas,
            title="📈 Progreso vs Meta Mensual",
            width=650,
            height=400
        )
        self.chart_lineas_area.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 4: Líneas suavizadas (curvas)
        self.chart_lineas_curvas = ProfessionalD3ChartCard(
            self.tab_comparativas,
            title="📈 Evolución Suavizada de Métricas",
            width=650,
            height=400
        )
        self.chart_lineas_curvas.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def _create_distribucion_dashboard(self):
        """Dashboard de Distribución - Circulares y Donut"""
        self.tab_distribucion.grid_columnconfigure(0, weight=1)
        self.tab_distribucion.grid_columnconfigure(1, weight=1)
        self.tab_distribucion.grid_rowconfigure(0, weight=1)
        self.tab_distribucion.grid_rowconfigure(1, weight=1)

        # Gráfico 1: Donut principal
        self.chart_donut_estatus = ProfessionalD3ChartCard(
            self.tab_distribucion,
            title="🍩 Distribución de Estatus Global",
            width=650,
            height=400
        )
        self.chart_donut_estatus.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 2: Donut por categorías
        self.chart_donut_categorias = ProfessionalD3ChartCard(
            self.tab_distribucion,
            title="🍩 Usuarios por Categoría de Módulo",
            width=650,
            height=400
        )
        self.chart_donut_categorias.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Gráfico 3: Pie chart niveles
        self.chart_pie_niveles = ProfessionalD3ChartCard(
            self.tab_distribucion,
            title="🍰 Distribución por Nivel Jerárquico",
            width=650,
            height=400
        )
        self.chart_pie_niveles.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 4: Donut anidado
        self.chart_donut_anidado = ProfessionalD3ChartCard(
            self.tab_distribucion,
            title="🍩 Progreso Detallado por Área",
            width=650,
            height=400
        )
        self.chart_donut_anidado.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def _create_tendencias_dashboard(self):
        """Dashboard de Tendencias - Temporales"""
        self.tab_tendencias.grid_columnconfigure(0, weight=1)
        self.tab_tendencias.grid_columnconfigure(1, weight=1)
        self.tab_tendencias.grid_rowconfigure(0, weight=1)
        self.tab_tendencias.grid_rowconfigure(1, weight=1)

        # Gráfico 1: Serie temporal completa
        self.chart_serie_temporal = ProfessionalD3ChartCard(
            self.tab_tendencias,
            title="📉 Serie Temporal - Últimos 12 Meses",
            width=650,
            height=400
        )
        self.chart_serie_temporal.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 2: Tendencia con proyección
        self.chart_proyeccion = ProfessionalD3ChartCard(
            self.tab_tendencias,
            title="📉 Tendencia con Proyección a 3 Meses",
            width=650,
            height=400
        )
        self.chart_proyeccion.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Gráfico 3: Variación porcentual
        self.chart_variacion = ProfessionalD3ChartCard(
            self.tab_tendencias,
            title="📉 Variación % Mensual",
            width=650,
            height=400
        )
        self.chart_variacion.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 4: Cascada (waterfall)
        self.chart_cascada = ProfessionalD3ChartCard(
            self.tab_tendencias,
            title="📉 Análisis de Cambios Acumulados",
            width=650,
            height=400
        )
        self.chart_cascada.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def _create_relaciones_dashboard(self):
        """Dashboard de Relaciones - Correlaciones y Patrones"""
        self.tab_relaciones.grid_columnconfigure(0, weight=1)
        self.tab_relaciones.grid_columnconfigure(1, weight=1)
        self.tab_relaciones.grid_rowconfigure(0, weight=1)
        self.tab_relaciones.grid_rowconfigure(1, weight=1)

        # Gráfico 1: Barras con comparación
        self.chart_scatter = ProfessionalD3ChartCard(
            self.tab_relaciones,
            title="🔵 Relación Tiempo vs Calificación",
            width=650,
            height=400
        )
        self.chart_scatter.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 2: Barras comparativas
        self.chart_comparativo = ProfessionalD3ChartCard(
            self.tab_relaciones,
            title="🔵 Comparativa Año Actual vs Anterior",
            width=650,
            height=400
        )
        self.chart_comparativo.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Gráfico 3: Matriz de correlación
        self.chart_matriz = ProfessionalD3ChartCard(
            self.tab_relaciones,
            title="🔵 Matriz de Rendimiento por Área",
            width=650,
            height=400
        )
        self.chart_matriz.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 4: Burbujas
        self.chart_burbujas = ProfessionalD3ChartCard(
            self.tab_relaciones,
            title="🔵 Análisis Multi-Variable (Burbujas)",
            width=650,
            height=400
        )
        self.chart_burbujas.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def _load_all_data(self):
        """Cargar todos los gráficos con datos de ejemplo"""
        print("🎨 Cargando dashboards gerenciales...")

        # ===== RENDIMIENTO =====
        # Barras por unidad
        self.chart_barras_unidad.set_d3_chart('bar', {
            'categorias': ['ICAVE', 'EIT', 'LCT', 'TIMSA', 'HPMX', 'TNG'],
            'valores': [89, 76, 92, 68, 81, 95],
            'meta': 80
        })

        # Barras horizontales
        self.chart_barras_depto.set_d3_chart('bar', {
            'categorias': ['Operaciones', 'Logística', 'Admin', 'RR.HH', 'IT', 'Ventas', 'Calidad', 'Finanzas', 'Legal', 'Marketing'],
            'valores': [95, 92, 89, 87, 85, 83, 81, 78, 75, 72]
        })

        # Barras apiladas
        self.chart_barras_apiladas.set_d3_chart('bar', {
            'categorias': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
            'valores': [65, 72, 78, 83, 88, 92]
        })

        # Barras agrupadas
        self.chart_barras_agrupadas.set_d3_chart('bar', {
            'categorias': ['Q1', 'Q2', 'Q3', 'Q4'],
            'valores': [75, 82, 88, 91]
        })

        # ===== COMPARATIVAS =====
        # Líneas múltiples
        self.chart_lineas_multi.set_d3_chart('line', {
            'categorias': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            'valores': [65, 68, 72, 75, 78, 82, 85, 88, 90, 92, 94, 95],
            'meta': 80
        })

        # Área apilada
        self.chart_area_apilada.set_d3_chart('line', {
            'categorias': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
            'valores': [450, 520, 580, 640, 710, 780]
        })

        # Líneas con área
        self.chart_lineas_area.set_d3_chart('line', {
            'categorias': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
            'valores': [65, 70, 75, 80, 85, 90],
            'meta': 75
        })

        # Líneas curvas
        self.chart_lineas_curvas.set_d3_chart('line', {
            'categorias': ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'Sem 5', 'Sem 6'],
            'valores': [60, 65, 72, 78, 85, 90]
        })

        # ===== DISTRIBUCIÓN =====
        # Donut estatus
        self.chart_donut_estatus.set_d3_chart('donut', {
            'categorias': ['Completado', 'En Progreso', 'No Iniciado', 'Vencido'],
            'valores': [450, 230, 180, 140]
        })

        # Donut categorías
        self.chart_donut_categorias.set_d3_chart('donut', {
            'categorias': ['Seguridad', 'Operaciones', 'Calidad', 'Admin', 'Técnico', 'Liderazgo'],
            'valores': [320, 280, 245, 210, 195, 150]
        })

        # Pie niveles
        self.chart_pie_niveles.set_d3_chart('donut', {
            'categorias': ['Directivo', 'Gerencial', 'Supervisión', 'Operativo'],
            'valores': [45, 120, 285, 550]
        })

        # Donut anidado
        self.chart_donut_anidado.set_d3_chart('donut', {
            'categorias': ['80-100%', '60-79%', '40-59%', '20-39%', '0-19%'],
            'valores': [320, 280, 190, 120, 90]
        })

        # ===== TENDENCIAS =====
        # Serie temporal
        self.chart_serie_temporal.set_d3_chart('line', {
            'categorias': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            'valores': [62, 65, 68, 72, 75, 78, 81, 84, 87, 89, 91, 93]
        })

        # Proyección
        self.chart_proyeccion.set_d3_chart('line', {
            'categorias': ['Oct', 'Nov', 'Dic', 'Ene*', 'Feb*', 'Mar*'],
            'valores': [89, 91, 93, 95, 96, 97]
        })

        # Variación
        self.chart_variacion.set_d3_chart('bar', {
            'categorias': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
            'valores': [5, 8, 12, 7, 10, 15]
        })

        # Cascada
        self.chart_cascada.set_d3_chart('bar', {
            'categorias': ['Inicial', '+Nuevos', '+Progreso', '-Abandonos', 'Final'],
            'valores': [500, 150, 200, -50, 800]
        })

        # ===== RELACIONES =====
        # Scatter
        self.chart_scatter.set_d3_chart('bar', {
            'categorias': ['0-2h', '2-4h', '4-6h', '6-8h', '8-10h', '10+h'],
            'valores': [65, 75, 82, 88, 92, 95]
        })

        # Comparativo
        self.chart_comparativo.set_d3_chart('bar', {
            'categorias': ['ICAVE', 'EIT', 'LCT', 'TIMSA', 'HPMX', 'TNG'],
            'valores': [89, 76, 92, 68, 81, 95]
        })

        # Matriz
        self.chart_matriz.set_d3_chart('bar', {
            'categorias': ['Área A', 'Área B', 'Área C', 'Área D', 'Área E'],
            'valores': [92, 87, 95, 78, 84]
        })

        # Burbujas
        self.chart_burbujas.set_d3_chart('donut', {
            'categorias': ['Grupo A', 'Grupo B', 'Grupo C', 'Grupo D', 'Grupo E'],
            'valores': [250, 180, 320, 140, 210]
        })

        print("✅ 20 dashboards gerenciales cargados")

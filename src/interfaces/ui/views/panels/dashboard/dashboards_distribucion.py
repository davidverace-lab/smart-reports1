"""
Dashboards de Distribución
Gráficos donut/pie para análisis de distribuciones
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.charts.tarjeta_d3_profesional import ProfessionalD3ChartCard


class DashboardsDistribucion(ctk.CTkFrame):
    """Dashboard de Distribución - 4 gráficos donut/pie"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Crear gráficos
        self._create_charts()

    def _create_charts(self):
        """Crear los 4 gráficos de distribución"""

        # Gráfico 1: Distribución de Estatus
        self.chart_donut_estatus = ProfessionalD3ChartCard(
            self,
            title="🍩 Distribución de Estatus Global",
            width=650,
            height=400
        )
        self.chart_donut_estatus.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 2: Usuarios por Categoría
        self.chart_donut_categorias = ProfessionalD3ChartCard(
            self,
            title="🍩 Usuarios por Categoría de Módulo",
            width=650,
            height=400
        )
        self.chart_donut_categorias.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Gráfico 3: Distribución Jerárquica
        self.chart_pie_niveles = ProfessionalD3ChartCard(
            self,
            title="🍩 Distribución por Nivel Jerárquico",
            width=650,
            height=400
        )
        self.chart_pie_niveles.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 4: Progreso Detallado
        self.chart_donut_anidado = ProfessionalD3ChartCard(
            self,
            title="🍩 Progreso Detallado por Área",
            width=650,
            height=400
        )
        self.chart_donut_anidado.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def load_data(self, metricas_service):
        """Cargar datos desde el servicio de métricas"""
        try:
            # Distribución de estatus
            datos_estatus = metricas_service.get_distribucion_estatus()
            self.chart_donut_estatus.set_d3_chart('donut', datos_estatus)

            # Usuarios por categoría
            datos_categoria = metricas_service.get_usuarios_por_categoria()
            self.chart_donut_categorias.set_d3_chart('donut', datos_categoria)

            # Distribución jerárquica
            datos_jerarquia = metricas_service.get_distribucion_jerarquia()
            self.chart_pie_niveles.set_d3_chart('donut', datos_jerarquia)

            # Reusar datos de estatus para donut anidado
            self.chart_donut_anidado.set_d3_chart('donut', datos_estatus)

        except Exception as e:
            print(f"Error cargando datos de distribución: {e}")

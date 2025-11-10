"""
Dashboards de Rendimiento
Gráficos de barras para analizar performance
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.charts.tarjeta_d3_profesional import ProfessionalD3ChartCard


class DashboardsRendimiento(ctk.CTkFrame):
    """Dashboard de Rendimiento - 4 gráficos de barras"""

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
        """Crear los 4 gráficos de rendimiento"""

        # Gráfico 1: Rendimiento por Unidad
        self.chart_barras_unidad = ProfessionalD3ChartCard(
            self,
            title="📊 Rendimiento por Unidad de Negocio",
            width=650,
            height=400
        )
        self.chart_barras_unidad.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 2: Top 10 Departamentos
        self.chart_barras_depto = ProfessionalD3ChartCard(
            self,
            title="📊 Top 10 Departamentos",
            width=650,
            height=400
        )
        self.chart_barras_depto.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Gráfico 3: Progreso Mensual
        self.chart_barras_apiladas = ProfessionalD3ChartCard(
            self,
            title="📊 Progreso Mensual Acumulado",
            width=650,
            height=400
        )
        self.chart_barras_apiladas.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 4: Comparativa Trimestral
        self.chart_barras_agrupadas = ProfessionalD3ChartCard(
            self,
            title="📊 Comparativa Trimestral",
            width=650,
            height=400
        )
        self.chart_barras_agrupadas.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def load_data(self, metricas_service):
        """Cargar datos desde el servicio de métricas"""
        try:
            # Rendimiento por unidad
            datos_unidad = metricas_service.get_rendimiento_por_unidad()
            self.chart_barras_unidad.set_d3_chart('bar', datos_unidad)

            # Top departamentos
            datos_deptos = metricas_service.get_top_departamentos()
            self.chart_barras_depto.set_d3_chart('bar', datos_deptos)

            # Progreso mensual
            datos_progreso = metricas_service.get_progreso_mensual()
            self.chart_barras_apiladas.set_d3_chart('bar', datos_progreso)

            # Comparativa trimestral
            datos_trimestre = metricas_service.get_comparativa_trimestral()
            self.chart_barras_agrupadas.set_d3_chart('bar', datos_trimestre)

        except Exception as e:
            print(f"Error cargando datos de rendimiento: {e}")

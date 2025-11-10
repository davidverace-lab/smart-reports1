"""
Dashboards de Tendencias
Análisis temporal y proyecciones
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.charts.tarjeta_d3_profesional import ProfessionalD3ChartCard


class DashboardsTendencias(ctk.CTkFrame):
    """Dashboard de Tendencias - 4 gráficos temporales"""

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
        """Crear los 4 gráficos de tendencias"""

        # Gráfico 1: Serie Temporal
        self.chart_serie_temporal = ProfessionalD3ChartCard(
            self,
            title="📉 Serie Temporal - Últimos 12 Meses",
            width=650,
            height=400
        )
        self.chart_serie_temporal.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 2: Proyección
        self.chart_proyeccion = ProfessionalD3ChartCard(
            self,
            title="📉 Tendencia con Proyección a 3 Meses",
            width=650,
            height=400
        )
        self.chart_proyeccion.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Gráfico 3: Variación
        self.chart_variacion = ProfessionalD3ChartCard(
            self,
            title="📉 Variación % Mensual",
            width=650,
            height=400
        )
        self.chart_variacion.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 4: Cascada
        self.chart_cascada = ProfessionalD3ChartCard(
            self,
            title="📉 Análisis de Cambios Acumulados",
            width=650,
            height=400
        )
        self.chart_cascada.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def load_data(self, metricas_service):
        """Cargar datos desde el servicio de métricas"""
        try:
            # Serie temporal
            datos_temporal = metricas_service.get_serie_temporal_12_meses()
            self.chart_serie_temporal.set_d3_chart('line', datos_temporal)

            # Proyección (últimos 6 meses)
            datos_progreso_6m = metricas_service.get_progreso_mensual(meses=6)
            self.chart_proyeccion.set_d3_chart('line', datos_progreso_6m)

            # Variación (progreso mensual)
            datos_progreso = metricas_service.get_progreso_mensual()
            self.chart_variacion.set_d3_chart('bar', datos_progreso)

            # Cascada (progreso mensual)
            self.chart_cascada.set_d3_chart('bar', datos_progreso)

        except Exception as e:
            print(f"Error cargando datos de tendencias: {e}")

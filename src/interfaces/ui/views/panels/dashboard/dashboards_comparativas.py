"""
Dashboards de Comparativas
Gráficos de líneas y áreas para análisis temporal
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.charts.tarjeta_d3_profesional import ProfessionalD3ChartCard


class DashboardsComparativas(ctk.CTkFrame):
    """Dashboard de Comparativas - 4 gráficos de líneas/áreas"""

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
        """Crear los 4 gráficos comparativos"""

        # Gráfico 1: Tendencia de Cumplimiento
        self.chart_lineas_multi = ProfessionalD3ChartCard(
            self,
            title="📈 Tendencia de Cumplimiento por Unidad",
            width=650,
            height=400
        )
        self.chart_lineas_multi.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 2: Distribución de Estatus
        self.chart_area_apilada = ProfessionalD3ChartCard(
            self,
            title="📈 Distribución de Estatus en el Tiempo",
            width=650,
            height=400
        )
        self.chart_area_apilada.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Gráfico 3: Progreso vs Meta
        self.chart_lineas_area = ProfessionalD3ChartCard(
            self,
            title="📈 Progreso vs Meta Mensual",
            width=650,
            height=400
        )
        self.chart_lineas_area.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 4: Evolución Suavizada
        self.chart_lineas_curvas = ProfessionalD3ChartCard(
            self,
            title="📈 Evolución Suavizada de Métricas",
            width=650,
            height=400
        )
        self.chart_lineas_curvas.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def load_data(self, metricas_service):
        """Cargar datos desde el servicio de métricas"""
        try:
            # Serie temporal 12 meses
            datos_temporal = metricas_service.get_serie_temporal_12_meses()
            self.chart_lineas_multi.set_d3_chart('line', datos_temporal)

            # Progreso mensual para área apilada
            datos_progreso = metricas_service.get_progreso_mensual()
            self.chart_area_apilada.set_d3_chart('line', datos_progreso)

            # Serie temporal para líneas con área
            self.chart_lineas_area.set_d3_chart('line', datos_temporal)

            # Progreso mensual 6m para líneas curvas
            datos_progreso_6m = metricas_service.get_progreso_mensual(meses=6)
            self.chart_lineas_curvas.set_d3_chart('line', datos_progreso_6m)

        except Exception as e:
            print(f"Error cargando datos comparativos: {e}")

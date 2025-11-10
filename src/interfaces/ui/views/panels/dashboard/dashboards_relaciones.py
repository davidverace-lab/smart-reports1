"""
Dashboards de Relaciones
Correlaciones y análisis multivariable
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.charts.tarjeta_d3_profesional import ProfessionalD3ChartCard


class DashboardsRelaciones(ctk.CTkFrame):
    """Dashboard de Relaciones - 4 gráficos de correlación"""

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
        """Crear los 4 gráficos de relaciones"""

        # Gráfico 1: Tiempo vs Calificación
        self.chart_scatter = ProfessionalD3ChartCard(
            self,
            title="🔵 Relación Tiempo vs Calificación",
            width=650,
            height=400
        )
        self.chart_scatter.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 2: Comparativa Año Actual vs Anterior
        self.chart_comparativo = ProfessionalD3ChartCard(
            self,
            title="🔵 Comparativa Año Actual vs Anterior",
            width=650,
            height=400
        )
        self.chart_comparativo.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Gráfico 3: Matriz de Rendimiento
        self.chart_matriz = ProfessionalD3ChartCard(
            self,
            title="🔵 Matriz de Rendimiento por Área",
            width=650,
            height=400
        )
        self.chart_matriz.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 4: Análisis Multi-Variable
        self.chart_burbujas = ProfessionalD3ChartCard(
            self,
            title="🔵 Análisis Multi-Variable (Burbujas)",
            width=650,
            height=400
        )
        self.chart_burbujas.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def load_data(self, metricas_service):
        """Cargar datos desde el servicio de métricas"""
        try:
            # Relación tiempo-calificación
            datos_tiempo = metricas_service.get_relacion_tiempo_calificacion()
            self.chart_scatter.set_d3_chart('bar', datos_tiempo)

            # Comparativo (rendimiento por unidad)
            datos_unidad = metricas_service.get_rendimiento_por_unidad()
            self.chart_comparativo.set_d3_chart('bar', datos_unidad)

            # Matriz (top departamentos)
            datos_deptos = metricas_service.get_top_departamentos()
            self.chart_matriz.set_d3_chart('bar', datos_deptos)

            # Burbujas (usuarios por categoría)
            datos_categoria = metricas_service.get_usuarios_por_categoria()
            self.chart_burbujas.set_d3_chart('donut', datos_categoria)

        except Exception as e:
            print(f"Error cargando datos de relaciones: {e}")

"""
Panel de Dashboards Gerenciales - Versión Modular
Integra 5 categorías de dashboards en tabs separados
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.navigation.boton_pestana import CustomTabView
from config.gestor_temas import get_theme_manager
from src.application.services.metricas_gerenciales_service import MetricasGerencialesService

# Importar los dashboards modularizados
from .dashboards_rendimiento import DashboardsRendimiento
from .dashboards_comparativas import DashboardsComparativas
from .dashboards_distribucion import DashboardsDistribucion
from .dashboards_tendencias import DashboardsTendencias
from .dashboards_relaciones import DashboardsRelaciones


class DashboardsGerencialesPanel(ctk.CTkFrame):
    """Panel principal con 20 dashboards D3.js organizados en 5 categorías"""

    def __init__(self, parent, db_connection=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection

        # Servicio de métricas gerenciales
        self.metricas_service = MetricasGerencialesService(db_connection)

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

        # Llenar cada pestaña con su dashboard correspondiente
        self._create_dashboards()

        # Cargar datos después de crear la interfaz
        self.after(500, self._load_all_data)

    def _create_header(self):
        """Crear header del panel"""
        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent', height=80)
        header.pack(fill='x', padx=20, pady=(20, 15))
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="📊 Dashboards Gerenciales - Visualización Completa D3.js",
            font=('Montserrat', 24, 'bold'),
            text_color=theme['text']
        )
        title.pack(side='left', anchor='w')

        badge = ctk.CTkLabel(
            header,
            text="D3.js Interactivo ⚡",
            font=('Montserrat', 12, 'bold'),
            fg_color='#51cf66',
            text_color='white',
            corner_radius=8,
            padx=15,
            height=30
        )
        badge.pack(side='right', anchor='e', padx=10)

    def _create_dashboards(self):
        """Crear los 5 dashboards modularizados"""

        # Dashboard 1: Rendimiento (4 gráficos de barras)
        self.dashboard_rendimiento = DashboardsRendimiento(self.tab_rendimiento)
        self.dashboard_rendimiento.pack(fill='both', expand=True)

        # Dashboard 2: Comparativas (4 gráficos de líneas/áreas)
        self.dashboard_comparativas = DashboardsComparativas(self.tab_comparativas)
        self.dashboard_comparativas.pack(fill='both', expand=True)

        # Dashboard 3: Distribución (4 gráficos donut/pie)
        self.dashboard_distribucion = DashboardsDistribucion(self.tab_distribucion)
        self.dashboard_distribucion.pack(fill='both', expand=True)

        # Dashboard 4: Tendencias (4 gráficos temporales)
        self.dashboard_tendencias = DashboardsTendencias(self.tab_tendencias)
        self.dashboard_tendencias.pack(fill='both', expand=True)

        # Dashboard 5: Relaciones (4 gráficos de correlación)
        self.dashboard_relaciones = DashboardsRelaciones(self.tab_relaciones)
        self.dashboard_relaciones.pack(fill='both', expand=True)

    def _load_all_data(self):
        """Cargar datos en todos los dashboards"""
        print("🎨 Cargando dashboards gerenciales con datos reales...")

        try:
            # Cargar datos en cada dashboard
            self.dashboard_rendimiento.load_data(self.metricas_service)
            self.dashboard_comparativas.load_data(self.metricas_service)
            self.dashboard_distribucion.load_data(self.metricas_service)
            self.dashboard_tendencias.load_data(self.metricas_service)
            self.dashboard_relaciones.load_data(self.metricas_service)

            print("✅ Dashboards cargados exitosamente con datos reales")

        except Exception as e:
            print(f"⚠️ Error cargando dashboards: {e}")
            print("📊 Usando datos de ejemplo como fallback...")

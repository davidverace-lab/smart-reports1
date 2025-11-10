"""
Panel de Dashboards - RESTAURADO a versión simple con matplotlib
Dos pestañas: General y Gerencial (estratégicas)
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.navigation.boton_pestana import CustomTabView
from src.interfaces.ui.views.components.charts.tarjeta_matplotlib_simple import SimpleMatplotlibCard
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS


class DashboardsGerencialesPanel(ctk.CTkFrame):
    """Panel simple con 2 pestañas: General y Gerencial"""

    def __init__(self, parent, db_connection=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection

        # Header
        self._create_header()

        # Tabs: General y Gerencial
        self.tab_view = CustomTabView(self)
        self.tab_view.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Crear pestañas
        self.tab_general = self.tab_view.add("📊 General", "📊")
        self.tab_gerencial = self.tab_view.add("📈 Dashboards Gerenciales", "📈")

        # Crear contenido de cada pestaña
        self._create_general_tab()
        self._create_gerencial_tab()

        # Cargar datos después de crear la interfaz
        self.after(500, self._load_data)

    def _create_header(self):
        """Crear header del panel"""
        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent', height=80)
        header.pack(fill='x', padx=20, pady=(20, 15))
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="📊 Dashboards",
            font=('Montserrat', 24, 'bold'),
            text_color=theme['text']
        )
        title.pack(side='left', anchor='w')

        badge = ctk.CTkLabel(
            header,
            text="📊 Matplotlib",
            font=('Montserrat', 12, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            text_color='white',
            corner_radius=8,
            padx=15,
            height=30
        )
        badge.pack(side='right', anchor='e', padx=10)

    def _create_general_tab(self):
        """Crear pestaña General con métricas y 2 dashboards"""
        theme = self.theme_manager.get_current_theme()

        # Container principal con scroll
        container = ctk.CTkScrollableFrame(
            self.tab_general,
            fg_color='transparent'
        )
        container.pack(fill='both', expand=True, padx=10, pady=10)

        # === SECCIÓN DE MÉTRICAS ===
        metrics_frame = ctk.CTkFrame(container, fg_color='transparent')
        metrics_frame.pack(fill='x', pady=(0, 20))

        # Grid para 3 métricas
        metrics_frame.columnconfigure((0, 1, 2), weight=1)

        # Métrica 1: Cantidad de Usuarios
        self.metric_usuarios = self._create_metric_card(
            metrics_frame,
            title="Total de Usuarios",
            value="0",
            subtitle="Usuarios activos",
            icon="👥",
            color=HUTCHISON_COLORS['ports_sky_blue']
        )
        self.metric_usuarios.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # Métrica 2: Módulo Actual
        self.metric_modulo = self._create_metric_card(
            metrics_frame,
            title="Módulo Actual",
            value="Dashboards",
            subtitle="Vista actual",
            icon="📊",
            color=HUTCHISON_COLORS['ports_horizon_blue']
        )
        self.metric_modulo.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # Métrica 3: Porcentaje de Avance
        self.metric_avance = self._create_metric_card(
            metrics_frame,
            title="Avance del Sistema",
            value="0%",
            subtitle="Implementación",
            icon="📈",
            color=HUTCHISON_COLORS['success']
        )
        self.metric_avance.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

        # === SECCIÓN DE DASHBOARDS GENERALES ===
        dashboards_frame = ctk.CTkFrame(container, fg_color='transparent')
        dashboards_frame.pack(fill='both', expand=True, pady=(10, 0))

        # Grid para 2 dashboards
        dashboards_frame.columnconfigure((0, 1), weight=1)

        # Dashboard 1: Usuarios por Módulo
        self.chart_usuarios_modulo = SimpleMatplotlibCard(
            dashboards_frame,
            title="Usuarios por Módulo",
            width=500,
            height=400
        )
        self.chart_usuarios_modulo.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 2: Reportes Generados
        self.chart_reportes = SimpleMatplotlibCard(
            dashboards_frame,
            title="Reportes Generados",
            width=500,
            height=400
        )
        self.chart_reportes.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        dashboards_frame.rowconfigure(0, weight=1)

    def _create_gerencial_tab(self):
        """Crear pestaña Gerencial con dashboards estratégicos"""
        theme = self.theme_manager.get_current_theme()

        # Container principal con scroll
        container = ctk.CTkScrollableFrame(
            self.tab_gerencial,
            fg_color='transparent'
        )
        container.pack(fill='both', expand=True, padx=10, pady=10)

        # Título de sección
        section_title = ctk.CTkLabel(
            container,
            text="Dashboards Estratégicos para Toma de Decisiones",
            font=('Montserrat', 18, 'bold'),
            text_color=theme['text']
        )
        section_title.pack(anchor='w', padx=10, pady=(10, 20))

        # === FILA 1: Unidades de Negocio y Distribución ===
        row1 = ctk.CTkFrame(container, fg_color='transparent')
        row1.pack(fill='x', pady=(0, 20))
        row1.columnconfigure((0, 1), weight=1)

        # Dashboard 1: Usuarios por Unidad de Negocio
        self.chart_unidades_negocio = SimpleMatplotlibCard(
            row1,
            title="Usuarios por Unidad de Negocio",
            width=500,
            height=400
        )
        self.chart_unidades_negocio.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 2: Distribución por Áreas
        self.chart_distribucion_areas = SimpleMatplotlibCard(
            row1,
            title="Distribución por Áreas",
            width=500,
            height=400
        )
        self.chart_distribucion_areas.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        row1.rowconfigure(0, weight=1)

        # === FILA 2: Tendencias y Actividad ===
        row2 = ctk.CTkFrame(container, fg_color='transparent')
        row2.pack(fill='x', pady=(0, 20))
        row2.columnconfigure((0, 1), weight=1)

        # Dashboard 3: Tendencia Mensual
        self.chart_tendencia_mensual = SimpleMatplotlibCard(
            row2,
            title="Tendencia de Uso Mensual",
            width=500,
            height=400
        )
        self.chart_tendencia_mensual.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 4: Actividad por Tipo de Reporte
        self.chart_tipo_reporte = SimpleMatplotlibCard(
            row2,
            title="Actividad por Tipo de Reporte",
            width=500,
            height=400
        )
        self.chart_tipo_reporte.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        row2.rowconfigure(0, weight=1)

    def _create_metric_card(self, parent, title, value, subtitle, icon, color):
        """Crear tarjeta de métrica"""
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )

        # Container interno
        inner = ctk.CTkFrame(card, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=20, pady=15)

        # Icono
        icon_label = ctk.CTkLabel(
            inner,
            text=icon,
            font=('Montserrat', 32),
            text_color=color
        )
        icon_label.pack(anchor='w', pady=(0, 5))

        # Valor principal
        value_label = ctk.CTkLabel(
            inner,
            text=value,
            font=('Montserrat', 28, 'bold'),
            text_color=theme['text']
        )
        value_label.pack(anchor='w', pady=(0, 2))

        # Título
        title_label = ctk.CTkLabel(
            inner,
            text=title,
            font=('Montserrat', 12, 'bold'),
            text_color=theme['text_secondary']
        )
        title_label.pack(anchor='w', pady=(0, 2))

        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            inner,
            text=subtitle,
            font=('Montserrat', 10),
            text_color=theme['text_tertiary']
        )
        subtitle_label.pack(anchor='w')

        # Guardar referencia al value_label para actualizar después
        card.value_label = value_label

        return card

    def _load_data(self):
        """Cargar datos en los dashboards"""
        print("📊 Cargando datos en dashboards...")

        try:
            # === CARGAR MÉTRICAS ===
            total_usuarios = self._get_total_usuarios()
            self.metric_usuarios.value_label.configure(text=str(total_usuarios))

            # Calcular porcentaje de avance (ejemplo: basado en usuarios)
            porcentaje = min(100, int((total_usuarios / 1000) * 100))  # Objetivo: 1000 usuarios
            self.metric_avance.value_label.configure(text=f"{porcentaje}%")

            # === CARGAR DASHBOARDS GENERALES ===
            # Dashboard 1: Usuarios por Módulo
            datos_modulos = {
                'labels': ['Reportes', 'Dashboards', 'Configuración', 'Usuarios', 'Soporte'],
                'values': [245, 198, 87, 156, 92]
            }
            self.chart_usuarios_modulo.set_chart('bar', datos_modulos)

            # Dashboard 2: Reportes Generados
            datos_reportes = {
                'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                'values': [450, 520, 480, 650, 720, 680]
            }
            self.chart_reportes.set_chart('line', datos_reportes)

            # === CARGAR DASHBOARDS GERENCIALES ===
            # Dashboard 1: Unidades de Negocio
            datos_unidades = self._get_datos_unidades_negocio()
            self.chart_unidades_negocio.set_chart('bar', datos_unidades)

            # Dashboard 2: Distribución por Áreas
            datos_areas = {
                'labels': ['Operaciones', 'Logística', 'Comercial', 'Administración', 'TI'],
                'values': [320, 280, 250, 180, 150]
            }
            self.chart_distribucion_areas.set_chart('donut', datos_areas)

            # Dashboard 3: Tendencia Mensual
            datos_tendencia = {
                'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                'values': [850, 920, 880, 1050, 1120, 1080, 1200, 1350, 1280, 1400, 1450, 1520]
            }
            self.chart_tendencia_mensual.set_chart('line', datos_tendencia)

            # Dashboard 4: Tipo de Reporte
            datos_tipos = {
                'labels': ['Financiero', 'Operativo', 'Estratégico', 'Táctico', 'Ejecutivo'],
                'values': [420, 380, 290, 250, 180]
            }
            self.chart_tipo_reporte.set_chart('bar', datos_tipos)

            print("✅ Dashboards cargados exitosamente")

        except Exception as e:
            print(f"❌ Error cargando dashboards: {e}")
            import traceback
            traceback.print_exc()

    def _get_total_usuarios(self):
        """Obtener total de usuarios desde la base de datos"""
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                # Intentar contar usuarios
                try:
                    cursor.execute("SELECT COUNT(*) FROM Instituto_Usuario WHERE Activo = 1")
                    result = cursor.fetchone()
                    if result:
                        return result[0]
                except:
                    # Si falla, usar dato de ejemplo
                    pass
        except:
            pass

        # Dato de ejemplo
        return 778

    def _get_datos_unidades_negocio(self):
        """Obtener datos de Unidades de Negocio"""
        # Datos de ejemplo de Unidades de Negocio Hutchison Ports
        return {
            'labels': [
                'TNG - Terminal\nContenedores',
                'Container\nCare',
                'ECV/EIT\nEquipos',
                'ICAVE\nLogística',
                'HPMX\nHutchison',
                'HIT\nTerminal',
                'TIMSA\nInfraestructura',
                'SITT\nServicios',
                'Hutchison\nLogistics',
                'Servicios\nCompartidos'
            ],
            'values': [523, 412, 387, 295, 268, 234, 198, 167, 145, 123]
        }

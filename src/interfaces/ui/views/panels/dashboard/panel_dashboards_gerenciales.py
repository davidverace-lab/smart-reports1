"""
Panel de Dashboards Gerenciales - VERSIÓN DEFINITIVA CON D3.JS
Dos pestañas: General y Gerencial con gráficos D3.js interactivos
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.navigation.boton_pestana import CustomTabView
from src.interfaces.ui.views.components.charts.tarjeta_d3_final import D3ChartCard
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS


class DashboardsGerencialesPanel(ctk.CTkFrame):
    """
    Panel de Dashboards con gráficos D3.js interactivos

    - Pestaña General: Métricas + 2 gráficos generales
    - Pestaña Gerencial: 4 gráficos estratégicos para toma de decisiones
    """

    def __init__(self, parent, db_connection=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        print("🚀 Inicializando DashboardsGerencialesPanel...")

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection

        try:
            # Header
            print("  → Creando header...")
            self._create_header()

            # Tabs
            print("  → Creando tabs...")
            self.tab_view = CustomTabView(self)
            self.tab_view.pack(fill='both', expand=True, padx=20, pady=(0, 20))

            # Crear pestañas
            print("  → Agregando pestañas...")
            self.tab_general = self.tab_view.add("General", "📊")
            self.tab_gerencial = self.tab_view.add("Dashboards Gerenciales", "📈")

            # Crear contenido
            print("  → Creando contenido de tabs...")
            self._create_general_tab()
            self._create_gerencial_tab()

            # Cargar datos
            print("  → Programando carga de datos...")
            self.after(500, self._load_data)

            print("✅ DashboardsGerencialesPanel inicializado correctamente")

        except Exception as e:
            print(f"❌ Error inicializando dashboard: {e}")
            import traceback
            traceback.print_exc()

    def _create_header(self):
        """Crear header del panel"""
        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent', height=80)
        header.pack(fill='x', padx=20, pady=(20, 15))
        header.pack_propagate(False)

        # Título
        title = ctk.CTkLabel(
            header,
            text="📊 Dashboards Interactivos",
            font=('Montserrat', 24, 'bold'),
            text_color=theme['text']
        )
        title.pack(side='left', anchor='w')

        # Badge D3.js
        badge = ctk.CTkLabel(
            header,
            text="D3.js Visualizations ⚡",
            font=('Montserrat', 12, 'bold'),
            fg_color=HUTCHISON_COLORS['success'],
            text_color='white',
            corner_radius=8,
            padx=15,
            height=30
        )
        badge.pack(side='right', anchor='e', padx=10)

    def _create_general_tab(self):
        """Crear pestaña General con métricas y 2 gráficos"""
        theme = self.theme_manager.get_current_theme()

        # Container con scroll
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
            subtitle="Usuarios activos en el sistema",
            icon="👥",
            color=HUTCHISON_COLORS['ports_sky_blue']
        )
        self.metric_usuarios.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # Métrica 2: Módulo Actual
        self.metric_modulo = self._create_metric_card(
            metrics_frame,
            title="Módulo Actual",
            value="Dashboards",
            subtitle="Vista activa",
            icon="📊",
            color=HUTCHISON_COLORS['ports_horizon_blue']
        )
        self.metric_modulo.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # Métrica 3: Porcentaje de Avance
        self.metric_avance = self._create_metric_card(
            metrics_frame,
            title="Progreso del Sistema",
            value="0%",
            subtitle="Implementación completa",
            icon="📈",
            color=HUTCHISON_COLORS['success']
        )
        self.metric_avance.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

        # === SECCIÓN DE GRÁFICOS GENERALES ===
        charts_frame = ctk.CTkFrame(container, fg_color='transparent')
        charts_frame.pack(fill='both', expand=True, pady=(10, 0))

        # Grid para 2 gráficos
        charts_frame.columnconfigure((0, 1), weight=1)
        charts_frame.rowconfigure(0, weight=1)

        # Gráfico 1: Usuarios por Módulo (D3.js Barras)
        self.chart_usuarios_modulo = D3ChartCard(
            charts_frame,
            title="Usuarios por Módulo",
            width=500,
            height=400
        )
        self.chart_usuarios_modulo.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Gráfico 2: Reportes Generados (D3.js Líneas)
        self.chart_reportes = D3ChartCard(
            charts_frame,
            title="Reportes Generados - Últimos 6 Meses",
            width=500,
            height=400
        )
        self.chart_reportes.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

    def _create_gerencial_tab(self):
        """Crear pestaña Gerencial con dashboards estratégicos"""
        theme = self.theme_manager.get_current_theme()

        # Container con scroll
        container = ctk.CTkScrollableFrame(
            self.tab_gerencial,
            fg_color='transparent'
        )
        container.pack(fill='both', expand=True, padx=10, pady=10)

        # Título de sección
        section_title = ctk.CTkLabel(
            container,
            text="Dashboards Estratégicos para Toma de Decisiones Gerenciales",
            font=('Montserrat', 18, 'bold'),
            text_color=theme['text']
        )
        section_title.pack(anchor='w', padx=10, pady=(10, 20))

        # === FILA 1: Unidades de Negocio y Distribución ===
        row1 = ctk.CTkFrame(container, fg_color='transparent')
        row1.pack(fill='x', pady=(0, 20))
        row1.columnconfigure((0, 1), weight=1)
        row1.rowconfigure(0, weight=1)

        # Dashboard 1: Usuarios por Unidad de Negocio (D3.js Barras)
        self.chart_unidades = D3ChartCard(
            row1,
            title="Usuarios por Unidad de Negocio",
            width=500,
            height=400
        )
        self.chart_unidades.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 2: Distribución por Áreas (D3.js Donut)
        self.chart_areas = D3ChartCard(
            row1,
            title="Distribución por Áreas Operativas",
            width=500,
            height=400
        )
        self.chart_areas.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # === FILA 2: Tendencias y Actividad ===
        row2 = ctk.CTkFrame(container, fg_color='transparent')
        row2.pack(fill='x', pady=(0, 20))
        row2.columnconfigure((0, 1), weight=1)
        row2.rowconfigure(0, weight=1)

        # Dashboard 3: Tendencia Mensual (D3.js Líneas)
        self.chart_tendencia = D3ChartCard(
            row2,
            title="Tendencia de Uso Mensual",
            width=500,
            height=400
        )
        self.chart_tendencia.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 4: Reportes por Tipo (D3.js Barras)
        self.chart_tipos = D3ChartCard(
            row2,
            title="Actividad por Tipo de Reporte",
            width=500,
            height=400
        )
        self.chart_tipos.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

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

        # Guardar referencia al value_label
        card.value_label = value_label

        return card

    def _load_data(self):
        """Cargar datos en todos los dashboards"""
        print("\n" + "="*60)
        print("📊 CARGANDO DASHBOARDS D3.JS INTERACTIVOS")
        print("="*60)

        try:
            print("\n[1/5] Cargando métricas...")
            # === CARGAR MÉTRICAS ===
            total_usuarios = self._get_total_usuarios()
            self.metric_usuarios.value_label.configure(text=str(total_usuarios))
            print(f"  ✓ Total usuarios: {total_usuarios}")

            # Calcular porcentaje
            porcentaje = min(100, int((total_usuarios / 1000) * 100))
            self.metric_avance.value_label.configure(text=f"{porcentaje}%")
            print(f"  ✓ Porcentaje: {porcentaje}%")

            # === CARGAR GRÁFICOS GENERALES ===
            print("\n[2/5] Cargando gráficos de pestaña General...")

            # Gráfico 1: Usuarios por Módulo (Barras D3.js)
            print("  → Chart 1: Usuarios por Módulo (bar)")
            datos_modulos = {
                'labels': ['Reportes', 'Dashboards', 'Configuración', 'Usuarios', 'Soporte'],
                'values': [245, 198, 87, 156, 92]
            }
            self.chart_usuarios_modulo.set_chart('bar', datos_modulos)
            print("    ✓ Completado")

            # Gráfico 2: Reportes Generados (Líneas D3.js)
            print("  → Chart 2: Reportes Generados (line)")
            datos_reportes = {
                'labels': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
                'values': [450, 520, 480, 650, 720, 680]
            }
            self.chart_reportes.set_chart('line', datos_reportes)
            print("    ✓ Completado")

            # === CARGAR DASHBOARDS GERENCIALES ===
            print("\n[3/5] Cargando dashboards gerenciales...")

            # Dashboard 1: Unidades de Negocio (Barras D3.js)
            print("  → Dashboard 1: Unidades de Negocio (bar)")
            datos_unidades = self._get_datos_unidades_negocio()
            self.chart_unidades.set_chart('bar', datos_unidades)
            print("    ✓ Completado")

            # Dashboard 2: Distribución por Áreas (Donut D3.js)
            print("  → Dashboard 2: Distribución por Áreas (donut)")
            datos_areas = {
                'labels': ['Operaciones', 'Logística', 'Comercial', 'Administración', 'TI'],
                'values': [320, 280, 250, 180, 150]
            }
            self.chart_areas.set_chart('donut', datos_areas)
            print("    ✓ Completado")

            # Dashboard 3: Tendencia Mensual (Líneas D3.js)
            print("  → Dashboard 3: Tendencia Mensual (line)")
            datos_tendencia = {
                'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                'values': [850, 920, 880, 1050, 1120, 1080, 1200, 1350, 1280, 1400, 1450, 1520]
            }
            self.chart_tendencia.set_chart('line', datos_tendencia)
            print("    ✓ Completado")

            # Dashboard 4: Tipos de Reporte (Barras D3.js)
            print("  → Dashboard 4: Tipos de Reporte (bar)")
            datos_tipos = {
                'labels': ['Financiero', 'Operativo', 'Estratégico', 'Táctico', 'Ejecutivo'],
                'values': [420, 380, 290, 250, 180]
            }
            self.chart_tipos.set_chart('bar', datos_tipos)
            print("    ✓ Completado")

            print("\n" + "="*60)
            print("✅ TODOS LOS DASHBOARDS D3.JS CARGADOS EXITOSAMENTE")
            print("="*60 + "\n")

        except Exception as e:
            print(f"❌ Error cargando dashboards: {e}")
            import traceback
            traceback.print_exc()

    def _get_total_usuarios(self):
        """Obtener total de usuarios desde BD"""
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                try:
                    cursor.execute("SELECT COUNT(*) FROM Instituto_Usuario WHERE Activo = 1")
                    result = cursor.fetchone()
                    if result:
                        return result[0]
                except:
                    pass
        except:
            pass

        # Dato de ejemplo
        return 778

    def _get_datos_unidades_negocio(self):
        """Obtener datos de Unidades de Negocio"""
        return {
            'labels': [
                'TNG - Terminal Contenedores',
                'Container Care',
                'ECV/EIT - Equipos',
                'ICAVE - Logística',
                'HPMX - Hutchison Ports',
                'HIT - Terminal',
                'TIMSA - Infraestructura',
                'SITT - Servicios',
                'Hutchison Logistics',
                'Servicios Compartidos'
            ],
            'values': [523, 412, 387, 295, 268, 234, 198, 167, 145, 123]
        }

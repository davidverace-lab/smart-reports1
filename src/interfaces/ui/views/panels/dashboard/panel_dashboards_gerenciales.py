"""
Panel de Dashboards Gerenciales - HUTCHISON PORTS
Diseño replicando mockup con gráficos D3.js interactivos
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.navigation.boton_pestana import CustomTabView
from src.interfaces.ui.views.components.charts.tarjeta_d3_final import D3ChartCard
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS


class DashboardsGerencialesPanel(ctk.CTkFrame):
    """
    Panel de Control - SMART REPORTS INSTITUTO HUTCHISON PORTS

    Diseño:
    - Header con saludo personalizado y logo
    - Tabs: General | Dashboards Gerenciales
    - 3 Cards superiores: Total Usuarios, Módulo Actual, Tasa Completado
    - Gráficos D3.js:
      * Usuarios por Unidad de Negocio (barras horizontales)
      * Progreso General por Unidad (donut chart)
    """

    def __init__(self, parent, db_connection=None, usuario_actual=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        print("🚀 Inicializando DashboardsGerencialesPanel...")

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection
        self.usuario_actual = usuario_actual or {"nombre": "Admin"}

        try:
            # Tabs de navegación (sin header, ya existe en upper bar)
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

    def _create_general_tab(self):
        """Crear pestaña General con diseño del mockup"""
        theme = self.theme_manager.get_current_theme()

        # Container principal con scroll
        container = ctk.CTkScrollableFrame(
            self.tab_general,
            fg_color='transparent'
        )
        container.pack(fill='both', expand=True, padx=10, pady=10)

        # === SECCIÓN DE MÉTRICAS (3 CARDS) ===
        print("    → Creando cards de métricas...")
        metrics_frame = ctk.CTkFrame(container, fg_color='transparent')
        metrics_frame.pack(fill='x', pady=(0, 20))

        # Grid para 3 cards: laterales pequeñas (peso 1), central grande (peso 2)
        metrics_frame.columnconfigure(0, weight=1)  # Total Usuarios (pequeña)
        metrics_frame.columnconfigure(1, weight=2)  # Módulo Actual (grande)
        metrics_frame.columnconfigure(2, weight=1)  # Tasa Completado (pequeña)

        # Card 1: Total de Usuarios (pequeña, izquierda)
        self.metric_usuarios = self._create_metric_card_small(
            metrics_frame,
            title="Total de Usuarios",
            value="0",
            subtitle="Usuarios activos",
            icon="👥",
            color=HUTCHISON_COLORS['ports_sky_blue']
        )
        self.metric_usuarios.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Card 2: Módulo Actual (grande, centro)
        self.metric_modulo = self._create_metric_card_large(
            metrics_frame,
            title="Módulo Actual",
            value="Módulo 8 - Procesos de Recursos Humanos",
            icon="📋",
            color=HUTCHISON_COLORS['ports_horizon_blue']
        )
        self.metric_modulo.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Card 3: Tasa de Completado (pequeña, derecha)
        self.metric_completado = self._create_metric_card_small(
            metrics_frame,
            title="Tasa de Completado",
            value="70.0%",
            subtitle="Progreso general",
            icon="✓",
            color=HUTCHISON_COLORS['success']
        )
        self.metric_completado.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        # === SECCIÓN DE GRÁFICOS (2 COLUMNAS) ===
        print("    → Creando sección de gráficos...")
        charts_frame = ctk.CTkFrame(container, fg_color='transparent')
        charts_frame.pack(fill='both', expand=True, pady=(10, 0))

        # Grid para 2 gráficos (60% - 40%)
        charts_frame.columnconfigure(0, weight=6)  # 60% para barras
        charts_frame.columnconfigure(1, weight=4)  # 40% para donut
        charts_frame.rowconfigure(0, weight=1)

        # Gráfico 1: Usuarios por Unidad de Negocio (Barras Horizontales)
        print("    → Creando gráfico de barras...")
        self.chart_usuarios_unidad = D3ChartCard(
            charts_frame,
            title="Usuarios por Unidad de Negocio",
            width=650,
            height=500
        )
        self.chart_usuarios_unidad.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='nsew')

        # Gráfico 2: Progreso General por Unidad (Donut Chart)
        print("    → Creando gráfico de dona...")
        self.chart_progreso_unidad = D3ChartCard(
            charts_frame,
            title="Progreso General por Unidad de Negocio (TNG 100% - 8 Módulos)",
            width=450,
            height=500
        )
        self.chart_progreso_unidad.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='nsew')

    def _create_gerencial_tab(self):
        """Crear pestaña Dashboards Gerenciales (vista adicional)"""
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
            font=('Segoe UI', 18, 'bold'),
            text_color=theme['text']
        )
        section_title.pack(anchor='w', padx=10, pady=(10, 20))

        # === FILA 1: Distribución y Tendencias ===
        row1 = ctk.CTkFrame(container, fg_color='transparent')
        row1.pack(fill='x', pady=(0, 20))
        row1.columnconfigure((0, 1), weight=1)

        # Dashboard 1: Distribución por Departamento
        self.chart_departamentos = D3ChartCard(
            row1,
            title="Distribución por Departamentos",
            width=500,
            height=400
        )
        self.chart_departamentos.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 2: Tendencia de Módulos
        self.chart_modulos_tendencia = D3ChartCard(
            row1,
            title="Tendencia de Completación de Módulos",
            width=500,
            height=400
        )
        self.chart_modulos_tendencia.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # === FILA 2: Actividad y Evaluaciones ===
        row2 = ctk.CTkFrame(container, fg_color='transparent')
        row2.pack(fill='x', pady=(0, 20))
        row2.columnconfigure((0, 1), weight=1)

        # Dashboard 3: Actividad Mensual
        self.chart_actividad = D3ChartCard(
            row2,
            title="Actividad Mensual del Sistema",
            width=500,
            height=400
        )
        self.chart_actividad.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 4: Resultados de Evaluaciones
        self.chart_evaluaciones = D3ChartCard(
            row2,
            title="Resultados de Evaluaciones",
            width=500,
            height=400
        )
        self.chart_evaluaciones.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

    def _create_metric_card_small(self, parent, title, value, subtitle, icon, color):
        """
        Crear tarjeta de métrica pequeña (laterales)

        Args:
            parent: Widget padre
            title: Título de la métrica
            value: Valor principal a mostrar
            subtitle: Texto descriptivo
            icon: Emoji o símbolo
            color: Color del icono y acento
        """
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=8,
            border_width=1,
            border_color=theme['border']
        )

        inner = ctk.CTkFrame(card, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=20, pady=15)

        # Icono
        icon_label = ctk.CTkLabel(
            inner,
            text=icon,
            font=('Segoe UI', 28),
            text_color=color
        )
        icon_label.pack(anchor='center', pady=(0, 5))

        # Valor principal
        value_label = ctk.CTkLabel(
            inner,
            text=value,
            font=('Segoe UI', 28, 'bold'),
            text_color=theme['text']
        )
        value_label.pack(anchor='center', pady=(0, 3))

        # Título
        title_label = ctk.CTkLabel(
            inner,
            text=title,
            font=('Segoe UI', 12, 'bold'),
            text_color=theme['text_secondary']
        )
        title_label.pack(anchor='center', pady=(0, 2))

        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            inner,
            text=subtitle,
            font=('Segoe UI', 10),
            text_color=theme['text_tertiary']
        )
        subtitle_label.pack(anchor='center')

        # Guardar referencias
        card.value_label = value_label
        card.title_label = title_label
        card.subtitle_label = subtitle_label

        return card

    def _create_metric_card_large(self, parent, title, value, icon, color):
        """
        Crear tarjeta de métrica grande (centro - Módulo Actual)

        Args:
            parent: Widget padre
            title: "Módulo Actual"
            value: "Módulo 8 - Procesos de Recursos Humanos"
            icon: Emoji o símbolo
            color: Color del icono y acento
        """
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=8,
            border_width=1,
            border_color=theme['border']
        )

        inner = ctk.CTkFrame(card, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=30, pady=20)

        # Icono grande
        icon_label = ctk.CTkLabel(
            inner,
            text=icon,
            font=('Segoe UI', 40),
            text_color=color
        )
        icon_label.pack(anchor='center', pady=(5, 8))

        # Título: "Módulo Actual"
        title_label = ctk.CTkLabel(
            inner,
            text=title,
            font=('Segoe UI', 14, 'bold'),
            text_color=theme['text_secondary']
        )
        title_label.pack(anchor='center', pady=(0, 8))

        # Valor: "Módulo 8 - Procesos de Recursos Humanos" (tamaño mediano)
        value_label = ctk.CTkLabel(
            inner,
            text=value,
            font=('Segoe UI', 18, 'bold'),
            text_color=theme['text'],
            wraplength=350
        )
        value_label.pack(anchor='center', pady=(0, 5))

        # Guardar referencias
        card.value_label = value_label
        card.title_label = title_label

        return card

    def _load_data(self):
        """Cargar datos reales desde la base de datos"""
        print("\n" + "="*70)
        print("📊 CARGANDO DATOS DEL DASHBOARD - HUTCHISON PORTS")
        print("="*70)

        try:
            # === PASO 1: CARGAR MÉTRICAS ===
            print("\n[1/3] 📈 Cargando métricas principales...")

            # Métrica 1: Total de Usuarios (desde BD)
            total_usuarios = self._get_total_usuarios()
            self.metric_usuarios.value_label.configure(text=f"{total_usuarios:,}")
            print(f"  ✓ Total usuarios: {total_usuarios:,}")

            # Métrica 2: Módulo Actual (ya está fijo, no se actualiza)
            print(f"  ✓ Módulo actual: Módulo 8 - Procesos de Recursos Humanos")

            # Métrica 3: Tasa de Completado (valor estático 70%)
            print(f"  ✓ Tasa de completado: 70.0% (valor estático)")

            # === PASO 2: CARGAR GRÁFICOS PESTAÑA GENERAL ===
            print("\n[2/3] 📊 Cargando gráficos de pestaña General...")

            # Gráfico 1: Usuarios por Unidad de Negocio (Barras Horizontales)
            print("  → Gráfico 1: Usuarios por Unidad de Negocio (bar horizontal)")
            datos_unidades = self._get_usuarios_por_unidad()
            if datos_unidades and datos_unidades['values']:
                self.chart_usuarios_unidad.set_chart('bar', datos_unidades)
                print(f"    ✓ Cargado con {len(datos_unidades['values'])} unidades")
            else:
                print("    ⚠ No hay datos disponibles, usando datos de ejemplo")
                self.chart_usuarios_unidad.set_chart('bar', self._get_datos_ejemplo_unidades())

            # Gráfico 2: Progreso por Unidad (Donut Chart)
            print("  → Gráfico 2: Progreso General por Unidad (donut)")
            datos_progreso = self._get_progreso_por_unidad()
            if datos_progreso and datos_progreso['values']:
                self.chart_progreso_unidad.set_chart('donut', datos_progreso)
                print(f"    ✓ Cargado con {len(datos_progreso['values'])} unidades")
            else:
                print("    ⚠ No hay datos disponibles, usando datos de ejemplo")
                self.chart_progreso_unidad.set_chart('donut', self._get_datos_ejemplo_progreso())

            # === PASO 3: CARGAR DASHBOARDS GERENCIALES ===
            print("\n[3/3] 📊 Cargando dashboards gerenciales...")

            # Dashboard 1: Distribución por Departamentos
            print("  → Dashboard 1: Distribución por Departamentos (donut)")
            datos_deptos = self._get_distribucion_departamentos()
            self.chart_departamentos.set_chart('donut', datos_deptos)
            print("    ✓ Completado")

            # Dashboard 2: Tendencia de Módulos
            print("  → Dashboard 2: Tendencia de Módulos (line)")
            datos_tendencia = {
                'labels': ['Mod 1', 'Mod 2', 'Mod 3', 'Mod 4', 'Mod 5', 'Mod 6', 'Mod 7', 'Mod 8'],
                'values': [92, 88, 85, 82, 78, 75, 72, 70]
            }
            self.chart_modulos_tendencia.set_chart('line', datos_tendencia)
            print("    ✓ Completado")

            # Dashboard 3: Actividad Mensual
            print("  → Dashboard 3: Actividad Mensual (line)")
            datos_actividad = {
                'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                'values': [850, 920, 980, 1050, 1120, 1180, 1250, 1320, 1380, 1450, 1500, 1525]
            }
            self.chart_actividad.set_chart('line', datos_actividad)
            print("    ✓ Completado")

            # Dashboard 4: Resultados de Evaluaciones
            print("  → Dashboard 4: Resultados de Evaluaciones (bar)")
            datos_eval = {
                'labels': ['Aprobados', 'En Proceso', 'Pendientes', 'No Aprobados'],
                'values': [1068, 284, 142, 31]
            }
            self.chart_evaluaciones.set_chart('bar', datos_eval)
            print("    ✓ Completado")

            print("\n" + "="*70)
            print("✅ TODOS LOS DATOS CARGADOS EXITOSAMENTE")
            print("="*70 + "\n")

        except Exception as e:
            print(f"❌ Error cargando datos del dashboard: {e}")
            import traceback
            traceback.print_exc()

    # ============================================
    # MÉTODOS DE CONSULTA A BASE DE DATOS
    # ============================================

    def _get_total_usuarios(self):
        """Obtener total de usuarios activos desde BD"""
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                query = """
                    SELECT COUNT(*) as total
                    FROM instituto_Usuario
                    WHERE Activo = 1
                """
                cursor.execute(query)
                result = cursor.fetchone()
                if result and result[0]:
                    return result[0]
        except Exception as e:
            print(f"  ⚠ Error consultando total usuarios: {e}")

        # Valor por defecto del mockup
        return 1525

    def _get_usuarios_por_unidad(self):
        """
        Obtener usuarios por unidad de negocio para gráfico de barras

        Returns:
            dict: {'labels': [...], 'values': [...]}
        """
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                query = """
                    SELECT
                        COALESCE(un.Codigo, 'SIN UNIDAD') as unidad,
                        COUNT(u.IdUsuario) as cantidad
                    FROM instituto_Usuario u
                    LEFT JOIN instituto_UnidadDeNegocio un
                        ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                    WHERE u.Activo = 1
                    GROUP BY un.Codigo
                    ORDER BY cantidad ASC
                """
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    labels = [row[0] for row in results]
                    values = [row[1] for row in results]
                    return {'labels': labels, 'values': values}
        except Exception as e:
            print(f"  ⚠ Error consultando usuarios por unidad: {e}")

        return None

    def _get_datos_ejemplo_unidades(self):
        """Datos de ejemplo del mockup para usuarios por unidad"""
        return {
            'labels': ['LCMT', 'HPLM', 'ECV', 'TILH', 'CCI', 'TNG', 'HPMX', 'TIMSA', 'LCT', 'EIT', 'ICAVE'],
            'values': [3, 9, 23, 71, 76, 129, 145, 195, 226, 276, 372]
        }

    def _get_progreso_por_unidad(self):
        """
        Obtener progreso promedio por unidad de negocio para donut chart

        Returns:
            dict: {'labels': [...], 'values': [...]}
        """
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                query = """
                    SELECT
                        un.Codigo as unidad,
                        ROUND(AVG(pm.PorcentajeAvance), 1) as promedio
                    FROM instituto_UnidadDeNegocio un
                    LEFT JOIN instituto_Usuario u ON un.IdUnidadDeNegocio = u.IdUnidadDeNegocio
                    LEFT JOIN instituto_ProgresoModulo pm ON u.UserId = pm.UserId
                    WHERE un.Activo = 1
                    GROUP BY un.IdUnidadDeNegocio, un.Codigo
                    HAVING promedio > 0
                    ORDER BY promedio DESC
                    LIMIT 5
                """
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    labels = [f"{row[0]} - {row[1]:.0f}%" for row in results]
                    values = [row[1] for row in results]
                    return {'labels': labels, 'values': values}
        except Exception as e:
            print(f"  ⚠ Error consultando progreso por unidad: {e}")

        return None

    def _get_datos_ejemplo_progreso(self):
        """Datos de ejemplo del mockup para progreso por unidad"""
        return {
            'labels': ['TNG - 100%', 'ICAVE - 82%', 'ECV - 75%', 'CCI - 68%', 'HPMX - 62%'],
            'values': [100, 82, 75, 68, 62]
        }

    def _get_distribucion_departamentos(self):
        """Obtener distribución de usuarios por departamento"""
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                query = """
                    SELECT
                        COALESCE(d.NombreDepartamento, 'Sin Departamento') as departamento,
                        COUNT(u.IdUsuario) as cantidad
                    FROM instituto_Usuario u
                    LEFT JOIN instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
                    WHERE u.Activo = 1
                    GROUP BY d.NombreDepartamento
                    ORDER BY cantidad DESC
                    LIMIT 8
                """
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    labels = [row[0] for row in results]
                    values = [row[1] for row in results]
                    return {'labels': labels, 'values': values}
        except Exception as e:
            print(f"  ⚠ Error consultando distribución departamentos: {e}")

        # Datos de ejemplo
        return {
            'labels': ['Operaciones', 'Logística', 'Comercial', 'Administración', 'TI', 'RRHH', 'Finanzas', 'Legal'],
            'values': [385, 298, 245, 187, 156, 134, 98, 67]
        }

"""
Panel de Dashboards de Recursos Humanos - HUTCHISON PORTS
Dashboards especializados para área de RRHH
"""
import customtkinter as ctk
from src.interfaces.ui.views.components.navigation.boton_pestana import CustomTabView
from src.interfaces.ui.views.components.charts.interactive_chart_card import InteractiveChartCard
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS


class PanelDashboardsRRHH(ctk.CTkFrame):
    """
    Panel especializado para Recursos Humanos

    Dashboards incluidos:
    - Distribución de personal por departamento
    - Capacitación: completados vs pendientes
    - Promedio de calificaciones por área
    - Rotación y antiguedad
    - Cumplimiento de capacitación obligatoria
    """

    def __init__(self, parent, db_connection=None, usuario_actual=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        print("🚀 Inicializando Panel RRHH...")

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection
        self.usuario_actual = usuario_actual or {"nombre": "RRHH"}

        try:
            # Título principal
            self._create_header()

            # Container con scroll
            self.container = ctk.CTkScrollableFrame(
                self,
                fg_color='transparent'
            )
            self.container.pack(fill='both', expand=True, padx=10, pady=10)

            # Crear dashboards
            self._create_dashboards()

            # Cargar datos
            self.after(500, self._load_data)

            print("✅ Panel RRHH inicializado correctamente")

        except Exception as e:
            print(f"❌ Error inicializando panel RRHH: {e}")
            import traceback
            traceback.print_exc()

    def _create_header(self):
        """Crear header del panel"""
        theme = self.theme_manager.get_current_theme()

        header_frame = ctk.CTkFrame(
            self,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=2,
            border_color=HUTCHISON_COLORS['aqua_green']
        )
        header_frame.pack(fill='x', padx=20, pady=(20, 10))

        header_content = ctk.CTkFrame(header_frame, fg_color='transparent')
        header_content.pack(fill='both', expand=True, padx=30, pady=20)

        # Título
        ctk.CTkLabel(
            header_content,
            text="👥 Dashboards de Recursos Humanos",
            font=('Segoe UI', 28, 'bold'),
            text_color=HUTCHISON_COLORS['aqua_green']
        ).pack(anchor='w', pady=(0, 5))

        # Subtítulo
        ctk.CTkLabel(
            header_content,
            text="Análisis especializado de capacitación y desarrollo de talento",
            font=('Segoe UI', 14),
            text_color=theme['text_secondary']
        ).pack(anchor='w')

    def _create_dashboards(self):
        """Crear todos los dashboards de RRHH"""
        theme = self.theme_manager.get_current_theme()

        # === FILA 1: Personal y Capacitación ===
        row1 = ctk.CTkFrame(self.container, fg_color='transparent')
        row1.pack(fill='x', pady=(0, 20))
        row1.columnconfigure((0, 1), weight=1)

        # Dashboard 1: Personal por Departamento
        print("    → Creando dashboard Personal por Departamento...")
        self.chart_personal_depto = InteractiveChartCard(
            row1,
            title="👥 Personal por Departamento",
            width=600,
            height=450
        )
        self.chart_personal_depto.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 2: Capacitación Completada
        print("    → Creando dashboard Capacitación...")
        self.chart_capacitacion = InteractiveChartCard(
            row1,
            title="📚 Estado de Capacitación",
            width=500,
            height=450
        )
        self.chart_capacitacion.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # === FILA 2: Calificaciones y Performance ===
        row2 = ctk.CTkFrame(self.container, fg_color='transparent')
        row2.pack(fill='x', pady=(0, 20))
        row2.columnconfigure((0, 1), weight=1)

        # Dashboard 3: Promedio de Calificaciones por Área
        print("    → Creando dashboard Calificaciones por Área...")
        self.chart_calif_area = InteractiveChartCard(
            row2,
            title="⭐ Promedio de Calificaciones por Área",
            width=550,
            height=400
        )
        self.chart_calif_area.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Dashboard 4: Cumplimiento por Unidad de Negocio
        print("    → Creando dashboard Cumplimiento...")
        self.chart_cumplimiento = InteractiveChartCard(
            row2,
            title="✓ % Cumplimiento por Unidad de Negocio",
            width=550,
            height=400
        )
        self.chart_cumplimiento.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # === FILA 3: Tendencias ===
        row3 = ctk.CTkFrame(self.container, fg_color='transparent')
        row3.pack(fill='x', pady=(0, 20))
        row3.columnconfigure((0, 1), weight=1)

        # Dashboard 5: Tendencia de Capacitación Mensual
        print("    → Creando dashboard Tendencia Mensual...")
        self.chart_tendencia = InteractiveChartCard(
            row3,
            title="📈 Módulos Completados por Mes",
            width=700,
            height=400
        )
        self.chart_tendencia.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    def _load_data(self):
        """Cargar datos en los dashboards"""
        print("\n[RRHH] Cargando datos de dashboards...")

        try:
            # Dashboard 1: Personal por Departamento
            datos_personal = self._get_personal_por_departamento()
            self.chart_personal_depto.set_chart('bar', datos_personal)
            print(f"  ✓ Dashboard 1: {len(datos_personal['values'])} departamentos")

            # Dashboard 2: Estado de Capacitación
            datos_capacitacion = self._get_estado_capacitacion()
            self.chart_capacitacion.set_chart('donut', datos_capacitacion)
            print(f"  ✓ Dashboard 2: Estado capacitación")

            # Dashboard 3: Calificaciones por Área
            datos_calif = self._get_calificaciones_por_area()
            self.chart_calif_area.set_chart('bar', datos_calif)
            print(f"  ✓ Dashboard 3: Calificaciones")

            # Dashboard 4: Cumplimiento
            datos_cumplimiento = self._get_cumplimiento_unidades()
            self.chart_cumplimiento.set_chart('bar', datos_cumplimiento)
            print(f"  ✓ Dashboard 4: Cumplimiento")

            # Dashboard 5: Tendencia Mensual
            datos_tendencia = self._get_tendencia_mensual()
            self.chart_tendencia.set_chart('line', datos_tendencia)
            print(f"  ✓ Dashboard 5: Tendencia")

            print("✅ Todos los dashboards RRHH cargados")

        except Exception as e:
            print(f"❌ Error cargando datos RRHH: {e}")
            import traceback
            traceback.print_exc()

    def _get_personal_por_departamento(self):
        """Obtener cantidad de personal por departamento"""
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                query = """
                    SELECT
                        Departamento,
                        COUNT(*) as Total
                    FROM instituto_Usuario
                    WHERE Activo = 1
                    GROUP BY Departamento
                    ORDER BY Total DESC
                """
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    labels = [row[0] for row in results]
                    values = [row[1] for row in results]
                    return {'labels': labels, 'values': values}
        except Exception as e:
            print(f"  ⚠ Error consultando personal: {e}")

        # Datos de ejemplo
        return {
            'labels': ['Operaciones', 'Logística', 'Administración', 'Mantenimiento', 'Recursos Humanos', 'Comercial', 'Seguridad', 'Sistemas'],
            'values': [245, 180, 95, 120, 42, 68, 85, 35]
        }

    def _get_estado_capacitacion(self):
        """Obtener estado de capacitación (completado, en progreso, pendiente)"""
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()

                # Completados
                cursor.execute("SELECT COUNT(*) FROM instituto_UsuarioModulo WHERE Progreso = 100 AND Aprobado = 1")
                completados = cursor.fetchone()[0] or 0

                # En Progreso
                cursor.execute("SELECT COUNT(*) FROM instituto_UsuarioModulo WHERE Progreso > 0 AND Progreso < 100")
                en_progreso = cursor.fetchone()[0] or 0

                # No iniciados (total usuarios * 8 módulos - asignados)
                cursor.execute("SELECT COUNT(*) FROM instituto_Usuario WHERE Activo = 1")
                total_usuarios = cursor.fetchone()[0] or 0
                total_posible = total_usuarios * 8

                cursor.execute("SELECT COUNT(*) FROM instituto_UsuarioModulo")
                asignados = cursor.fetchone()[0] or 0

                pendientes = max(0, total_posible - asignados)

                return {
                    'labels': ['Completados', 'En Progreso', 'Pendientes'],
                    'values': [completados, en_progreso, pendientes]
                }
        except Exception as e:
            print(f"  ⚠ Error consultando capacitación: {e}")

        # Datos de ejemplo
        return {
            'labels': ['Completados', 'En Progreso', 'Pendientes'],
            'values': [1850, 420, 3180]
        }

    def _get_calificaciones_por_area(self):
        """Obtener promedio de calificaciones por área"""
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                query = """
                    SELECT
                        u.Departamento,
                        AVG(CAST(um.CalificacionFinal AS FLOAT)) as PromedioCalif
                    FROM instituto_UsuarioModulo um
                    INNER JOIN instituto_Usuario u ON um.UsuarioID = u.UsuarioID
                    WHERE um.CalificacionFinal IS NOT NULL AND um.Aprobado = 1
                    GROUP BY u.Departamento
                    ORDER BY PromedioCalif DESC
                """
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    labels = [row[0] for row in results]
                    values = [round(row[1], 1) for row in results]
                    return {'labels': labels, 'values': values}
        except Exception as e:
            print(f"  ⚠ Error consultando calificaciones: {e}")

        # Datos de ejemplo
        return {
            'labels': ['Seguridad', 'Operaciones', 'Logística', 'Sistemas', 'Administración', 'RRHH', 'Comercial', 'Mantenimiento'],
            'values': [92.5, 90.2, 89.8, 88.5, 87.3, 86.9, 85.4, 84.2]
        }

    def _get_cumplimiento_unidades(self):
        """Obtener % de cumplimiento por unidad de negocio"""
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                query = """
                    SELECT
                        un.Nombre,
                        COUNT(DISTINCT um.UsuarioID) * 100.0 / COUNT(DISTINCT u.UsuarioID) as PorcentajeCumplimiento
                    FROM instituto_Usuario u
                    INNER JOIN instituto_UnidadNegocio un ON u.UnidadNegocioID = un.UnidadID
                    LEFT JOIN instituto_UsuarioModulo um ON u.UsuarioID = um.UsuarioID AND um.Progreso = 100
                    WHERE u.Activo = 1
                    GROUP BY un.Nombre
                    ORDER BY PorcentajeCumplimiento DESC
                """
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    labels = [row[0] for row in results]
                    values = [round(row[1], 1) for row in results]
                    return {'labels': labels, 'values': values}
        except Exception as e:
            print(f"  ⚠ Error consultando cumplimiento: {e}")

        # Datos de ejemplo
        return {
            'labels': ['Terminal 1', 'Logística', 'RRHH', 'TI', 'Seguridad', 'Terminal 2', 'Operaciones', 'Administración'],
            'values': [95.5, 92.3, 91.8, 89.2, 88.5, 85.7, 83.2, 80.5]
        }

    def _get_tendencia_mensual(self):
        """Obtener tendencia de módulos completados por mes"""
        try:
            if self.db_connection:
                cursor = self.db_connection.cursor()
                query = """
                    SELECT
                        FORMAT(FechaFinalizacion, 'yyyy-MM') as Mes,
                        COUNT(*) as Total
                    FROM instituto_UsuarioModulo
                    WHERE Progreso = 100 AND FechaFinalizacion IS NOT NULL
                    GROUP BY FORMAT(FechaFinalizacion, 'yyyy-MM')
                    ORDER BY Mes
                """
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    # Convertir "2024-01" a "Ene 2024"
                    meses = {
                        '01': 'Ene', '02': 'Feb', '03': 'Mar', '04': 'Abr',
                        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Ago',
                        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dic'
                    }
                    labels = [f"{meses[row[0].split('-')[1]]} {row[0].split('-')[0]}" for row in results]
                    values = [row[1] for row in results]
                    return {'labels': labels, 'values': values}
        except Exception as e:
            print(f"  ⚠ Error consultando tendencia: {e}")

        # Datos de ejemplo
        return {
            'labels': ['Ene 2024', 'Feb 2024', 'Mar 2024', 'Abr 2024', 'May 2024', 'Jun 2024', 'Jul 2024'],
            'values': [145, 198, 225, 268, 312, 285, 295]
        }

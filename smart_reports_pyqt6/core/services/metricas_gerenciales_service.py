"""
Servicio de Métricas Gerenciales
Proporciona datos agregados para dashboards ejecutivos
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


class MetricasGerencialesService:
    """Servicio para obtener métricas gerenciales agregadas"""

    def __init__(self, db_connection):
        """
        Args:
            db_connection: Conexión a base de datos MySQL
        """
        self.conn = db_connection
        self.cursor = db_connection.cursor() if db_connection else None

    # ==================== RENDIMIENTO ====================

    def get_rendimiento_por_unidad(self) -> Dict[str, Any]:
        """Obtener rendimiento por unidad de negocio"""
        if not self.cursor:
            return self._get_mock_rendimiento_unidad()

        try:
            query = """
            SELECT
                u.unidad_negocio,
                COUNT(DISTINCT a.usuario_id) as total_usuarios,
                SUM(CASE WHEN a.estatus = 'Completado' THEN 1 ELSE 0 END) as completados,
                ROUND(AVG(CASE WHEN a.estatus = 'Completado' THEN a.calificacion ELSE NULL END), 1) as promedio_calif
            FROM instituto_asignaciones a
            JOIN instituto_usuarios u ON a.usuario_id = u.id
            WHERE a.estatus IS NOT NULL
            GROUP BY u.unidad_negocio
            ORDER BY completados DESC
            LIMIT 10
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                return self._get_mock_rendimiento_unidad()

            categorias = [row[0] for row in results]
            valores = [float(row[3]) if row[3] else 0 for row in results]

            return {
                'categorias': categorias,
                'valores': valores
            }
        except Exception as e:
            print(f"Error en get_rendimiento_por_unidad: {e}")
            return self._get_mock_rendimiento_unidad()

    def get_top_departamentos(self) -> Dict[str, Any]:
        """Top 10 departamentos por rendimiento"""
        if not self.cursor:
            return self._get_mock_top_departamentos()

        try:
            query = """
            SELECT
                u.departamento,
                COUNT(DISTINCT a.id) as total_asignaciones,
                SUM(CASE WHEN a.estatus = 'Completado' THEN 1 ELSE 0 END) as completados,
                ROUND(100.0 * SUM(CASE WHEN a.estatus = 'Completado' THEN 1 ELSE 0 END) / COUNT(*), 1) as porcentaje
            FROM instituto_asignaciones a
            JOIN instituto_usuarios u ON a.usuario_id = u.id
            WHERE a.estatus IS NOT NULL AND u.departamento IS NOT NULL
            GROUP BY u.departamento
            ORDER BY porcentaje DESC
            LIMIT 10
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                return self._get_mock_top_departamentos()

            categorias = [row[0] for row in results]
            valores = [float(row[3]) for row in results]

            return {
                'categorias': categorias,
                'valores': valores
            }
        except Exception as e:
            print(f"Error en get_top_departamentos: {e}")
            return self._get_mock_top_departamentos()

    def get_progreso_mensual(self, meses: int = 6) -> Dict[str, Any]:
        """Progreso mensual acumulado"""
        if not self.cursor:
            return self._get_mock_progreso_mensual()

        try:
            query = """
            SELECT
                DATE_FORMAT(c.fecha_finalizacion, '%b %Y') as mes,
                COUNT(*) as completados
            FROM instituto_completados c
            WHERE c.fecha_finalizacion >= DATE_SUB(NOW(), INTERVAL %s MONTH)
            GROUP BY DATE_FORMAT(c.fecha_finalizacion, '%Y-%m')
            ORDER BY c.fecha_finalizacion
            """
            self.cursor.execute(query, (meses,))
            results = self.cursor.fetchall()

            if not results:
                return self._get_mock_progreso_mensual()

            categorias = [row[0] for row in results]
            valores = [int(row[1]) for row in results]

            return {
                'categorias': categorias,
                'valores': valores
            }
        except Exception as e:
            print(f"Error en get_progreso_mensual: {e}")
            return self._get_mock_progreso_mensual()

    def get_comparativa_trimestral(self) -> Dict[str, Any]:
        """Comparativa trimestral"""
        if not self.cursor:
            return self._get_mock_comparativa_trimestral()

        try:
            query = """
            SELECT
                CONCAT('Q', QUARTER(c.fecha_finalizacion)) as trimestre,
                COUNT(*) as total,
                ROUND(AVG(a.calificacion), 1) as promedio
            FROM instituto_completados c
            JOIN instituto_asignaciones a ON c.asignacion_id = a.id
            WHERE YEAR(c.fecha_finalizacion) = YEAR(NOW())
            GROUP BY QUARTER(c.fecha_finalizacion)
            ORDER BY QUARTER(c.fecha_finalizacion)
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                return self._get_mock_comparativa_trimestral()

            categorias = [row[0] for row in results]
            valores = [float(row[2]) if row[2] else 0 for row in results]

            return {
                'categorias': categorias,
                'valores': valores
            }
        except Exception as e:
            print(f"Error en get_comparativa_trimestral: {e}")
            return self._get_mock_comparativa_trimestral()

    # ==================== DISTRIBUCIÓN ====================

    def get_distribucion_estatus(self) -> Dict[str, Any]:
        """Distribución de estatus global"""
        if not self.cursor:
            return self._get_mock_distribucion_estatus()

        try:
            query = """
            SELECT
                COALESCE(a.estatus, 'Sin Estatus') as estatus,
                COUNT(*) as total
            FROM instituto_asignaciones a
            GROUP BY a.estatus
            ORDER BY total DESC
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                return self._get_mock_distribucion_estatus()

            categorias = [row[0] for row in results]
            valores = [int(row[1]) for row in results]

            return {
                'categorias': categorias,
                'valores': valores
            }
        except Exception as e:
            print(f"Error en get_distribucion_estatus: {e}")
            return self._get_mock_distribucion_estatus()

    def get_usuarios_por_categoria(self) -> Dict[str, Any]:
        """Usuarios por categoría de módulo"""
        if not self.cursor:
            return self._get_mock_usuarios_categoria()

        try:
            query = """
            SELECT
                SUBSTRING_INDEX(a.curso, ' ', 1) as categoria,
                COUNT(DISTINCT a.usuario_id) as usuarios
            FROM instituto_asignaciones a
            WHERE a.curso IS NOT NULL
            GROUP BY categoria
            ORDER BY usuarios DESC
            LIMIT 8
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                return self._get_mock_usuarios_categoria()

            categorias = [row[0] for row in results]
            valores = [int(row[1]) for row in results]

            return {
                'categorias': categorias,
                'valores': valores
            }
        except Exception as e:
            print(f"Error en get_usuarios_por_categoria: {e}")
            return self._get_mock_usuarios_categoria()

    def get_distribucion_jerarquia(self) -> Dict[str, Any]:
        """Distribución por nivel jerárquico"""
        if not self.cursor:
            return self._get_mock_distribucion_jerarquia()

        try:
            query = """
            SELECT
                u.nivel_puesto,
                COUNT(DISTINCT u.id) as total_usuarios,
                SUM(CASE WHEN a.estatus = 'Completado' THEN 1 ELSE 0 END) as completados
            FROM instituto_usuarios u
            LEFT JOIN instituto_asignaciones a ON u.id = a.usuario_id
            WHERE u.nivel_puesto IS NOT NULL
            GROUP BY u.nivel_puesto
            ORDER BY total_usuarios DESC
            LIMIT 8
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                return self._get_mock_distribucion_jerarquia()

            categorias = [row[0] for row in results]
            valores = [int(row[1]) for row in results]

            return {
                'categorias': categorias,
                'valores': valores
            }
        except Exception as e:
            print(f"Error en get_distribucion_jerarquia: {e}")
            return self._get_mock_distribucion_jerarquia()

    # ==================== TENDENCIAS ====================

    def get_serie_temporal_12_meses(self) -> Dict[str, Any]:
        """Serie temporal últimos 12 meses"""
        if not self.cursor:
            return self._get_mock_serie_temporal()

        try:
            query = """
            SELECT
                DATE_FORMAT(c.fecha_finalizacion, '%b %y') as mes,
                COUNT(*) as total,
                ROUND(AVG(a.calificacion), 1) as promedio_calif
            FROM instituto_completados c
            JOIN instituto_asignaciones a ON c.asignacion_id = a.id
            WHERE c.fecha_finalizacion >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
            GROUP BY DATE_FORMAT(c.fecha_finalizacion, '%Y-%m')
            ORDER BY c.fecha_finalizacion
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                return self._get_mock_serie_temporal()

            categorias = [row[0] for row in results]
            valores = [float(row[2]) if row[2] else 0 for row in results]

            return {
                'categorias': categorias,
                'valores': valores,
                'meta': 80
            }
        except Exception as e:
            print(f"Error en get_serie_temporal_12_meses: {e}")
            return self._get_mock_serie_temporal()

    # ==================== RELACIONES ====================

    def get_relacion_tiempo_calificacion(self) -> Dict[str, Any]:
        """Relación entre tiempo dedicado y calificación"""
        if not self.cursor:
            return self._get_mock_relacion_tiempo()

        try:
            query = """
            SELECT
                a.tiempo_dedicado,
                a.calificacion
            FROM instituto_asignaciones a
            WHERE a.estatus = 'Completado'
                AND a.tiempo_dedicado IS NOT NULL
                AND a.calificacion IS NOT NULL
                AND a.tiempo_dedicado > 0
            LIMIT 100
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                return self._get_mock_relacion_tiempo()

            # Agrupar en rangos para visualización de barras
            rangos = {'0-30min': [], '30-60min': [], '1-2h': [], '2-4h': [], '4h+': []}
            for tiempo, calif in results:
                minutos = tiempo  # Asumiendo que tiempo_dedicado está en minutos
                if minutos <= 30:
                    rangos['0-30min'].append(calif)
                elif minutos <= 60:
                    rangos['30-60min'].append(calif)
                elif minutos <= 120:
                    rangos['1-2h'].append(calif)
                elif minutos <= 240:
                    rangos['2-4h'].append(calif)
                else:
                    rangos['4h+'].append(calif)

            categorias = []
            valores = []
            for rango, califs in rangos.items():
                if califs:
                    categorias.append(rango)
                    valores.append(round(sum(califs) / len(califs), 1))

            return {
                'categorias': categorias,
                'valores': valores
            }
        except Exception as e:
            print(f"Error en get_relacion_tiempo_calificacion: {e}")
            return self._get_mock_relacion_tiempo()

    # ==================== DATOS MOCK (FALLBACK) ====================

    def _get_mock_rendimiento_unidad(self):
        return {
            'categorias': ['TNG', 'Container Care', 'ECV/EIT', 'Logística', 'Puerto'],
            'valores': [92, 88, 85, 82, 78]
        }

    def _get_mock_top_departamentos(self):
        return {
            'categorias': ['Operaciones', 'Logística', 'Admin', 'RR.HH', 'IT', 'Ventas', 'Calidad', 'Finanzas', 'Legal', 'Marketing'],
            'valores': [95, 92, 89, 87, 85, 83, 81, 78, 75, 72]
        }

    def _get_mock_progreso_mensual(self):
        return {
            'categorias': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
            'valores': [65, 72, 78, 83, 88, 92]
        }

    def _get_mock_comparativa_trimestral(self):
        return {
            'categorias': ['Q1', 'Q2', 'Q3', 'Q4'],
            'valores': [75, 82, 88, 91]
        }

    def _get_mock_distribucion_estatus(self):
        return {
            'categorias': ['Completado', 'En Progreso', 'No Iniciado', 'Vencido'],
            'valores': [1250, 380, 215, 155]
        }

    def _get_mock_usuarios_categoria(self):
        return {
            'categorias': ['Seguridad', 'Operaciones', 'Calidad', 'Liderazgo', 'Técnico', 'Compliance', 'Soft Skills', 'Ventas'],
            'valores': [450, 380, 320, 280, 245, 210, 185, 160]
        }

    def _get_mock_distribucion_jerarquia(self):
        return {
            'categorias': ['Directores', 'Gerentes', 'Supervisores', 'Coordinadores', 'Analistas', 'Operadores', 'Técnicos', 'Admin'],
            'valores': [45, 120, 280, 350, 420, 580, 320, 185]
        }

    def _get_mock_serie_temporal(self):
        return {
            'categorias': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            'valores': [65, 68, 72, 75, 78, 82, 85, 88, 90, 92, 94, 95],
            'meta': 80
        }

    def _get_mock_relacion_tiempo(self):
        return {
            'categorias': ['0-30min', '30-60min', '1-2h', '2-4h', '4h+'],
            'valores': [72, 78, 85, 92, 88]
        }

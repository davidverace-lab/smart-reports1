"""
DatabaseQueryController - LÓGICA de consultas a base de datos
Separa la lógica de BD de la interfaz (patrón Android: Controller = Java)
"""


class DatabaseQueryController:
    """Controller para manejar todas las consultas a base de datos"""

    def __init__(self, db_connection, cursor):
        """
        Args:
            db_connection: Conexión a la base de datos
            cursor: Cursor para ejecutar consultas
        """
        self.conn = db_connection
        self.cursor = cursor

    def verify_database_tables(self):
        """Verificar que las tablas necesarias existan"""
        tables_needed = ['instituto_UnidadDeNegocio', 'instituto_Usuario',
                        'instituto_Modulo', 'instituto_ProgresoModulo']
        placeholders = ','.join(['?' for _ in tables_needed])

        try:
            self.cursor.execute(f"""
                SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
                AND TABLE_NAME IN ({placeholders})
            """, tables_needed)

            existing_tables = [t[0] for t in self.cursor.fetchall()]

            if len(existing_tables) < len(tables_needed):
                missing = set(tables_needed) - set(existing_tables)
                return False, f"Faltan tablas: {', '.join(missing)}"

            return True, "Todas las tablas existen"

        except Exception as e:
            return False, f"Error verificando tablas: {e}"

    def load_business_units(self):
        """
        Cargar unidades de negocio desde BD

        Returns:
            list: Lista de nombres de unidades de negocio
        """
        try:
            query = """
                SELECT DISTINCT NombreUnidad
                FROM instituto_UnidadDeNegocio
                WHERE Activo = 1
                ORDER BY NombreUnidad
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return [row[0] for row in results]

        except Exception as e:
            print(f"Error cargando unidades de negocio: {e}")
            return []

    def search_user_by_id(self, user_id):
        """
        Buscar usuario por ID

        Args:
            user_id: ID del usuario a buscar

        Returns:
            dict: Datos del usuario o None si no existe
        """
        try:
            query = """
                SELECT
                    u.IdUsuario,
                    u.NombreCompleto,
                    u.Email,
                    u.UserStatus,
                    un.NombreUnidad,
                    u.Division
                FROM instituto_Usuario u
                LEFT JOIN instituto_UnidadDeNegocio un
                    ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                WHERE u.IdUsuario = ?
            """
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()

            if result:
                return {
                    'id': result[0],
                    'nombre': result[1],
                    'email': result[2],
                    'status': result[3],
                    'unidad': result[4] or 'Sin Unidad',
                    'division': result[5] or 'Sin División'
                }

            return None

        except Exception as e:
            print(f"Error buscando usuario: {e}")
            return None

    def query_business_unit(self, unit_name):
        """
        Consultar usuarios de una unidad de negocio

        Args:
            unit_name: Nombre de la unidad de negocio

        Returns:
            tuple: (columnas, resultados)
        """
        try:
            query = """
                SELECT
                    u.IdUsuario,
                    u.NombreCompleto,
                    u.Email,
                    un.NombreUnidad,
                    u.UserStatus,
                    COUNT(DISTINCT pm.IdModulo) as ModulosAsignados,
                    SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as ModulosCompletados
                FROM instituto_Usuario u
                LEFT JOIN instituto_UnidadDeNegocio un
                    ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                LEFT JOIN instituto_ProgresoModulo pm
                    ON u.UserId = pm.UserId
                WHERE un.NombreUnidad = ?
                GROUP BY u.IdUsuario, u.NombreCompleto, u.Email, un.NombreUnidad, u.UserStatus
                ORDER BY u.NombreCompleto
            """
            self.cursor.execute(query, (unit_name,))
            results = self.cursor.fetchall()

            columns = ['ID', 'Nombre', 'Email', 'Unidad', 'Estado',
                      'Módulos Asignados', 'Módulos Completados']

            return columns, results

        except Exception as e:
            print(f"Error consultando unidad: {e}")
            return [], []

    def query_new_users(self, days=30):
        """
        Consultar usuarios nuevos en los últimos N días

        Args:
            days: Número de días hacia atrás

        Returns:
            tuple: (columnas, resultados)
        """
        try:
            query = """
                SELECT
                    u.IdUsuario,
                    u.NombreCompleto,
                    u.Email,
                    un.NombreUnidad,
                    u.FechaCreacion,
                    u.UserStatus
                FROM instituto_Usuario u
                LEFT JOIN instituto_UnidadDeNegocio un
                    ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                WHERE u.FechaCreacion >= DATEADD(day, -?, GETDATE())
                ORDER BY u.FechaCreacion DESC
            """
            self.cursor.execute(query, (days,))
            results = self.cursor.fetchall()

            columns = ['ID', 'Nombre', 'Email', 'Unidad', 'Fecha Creación', 'Estado']

            return columns, results

        except Exception as e:
            print(f"Error consultando usuarios nuevos: {e}")
            return [], []

    def get_progress_statistics(self):
        """
        Obtener estadísticas globales de progreso

        Returns:
            dict: Estadísticas de progreso
        """
        try:
            # Total usuarios
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM instituto_Usuario
                WHERE UserStatus = 'Active'
            """)
            total_users = self.cursor.fetchone()[0] or 0

            # Total módulos
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM instituto_Modulo
                WHERE Activo = 1
            """)
            total_modules = self.cursor.fetchone()[0] or 0

            # Módulos completados
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM instituto_ProgresoModulo
                WHERE EstatusModulo = 'Completado'
            """)
            completed = self.cursor.fetchone()[0] or 0

            # Módulos en progreso
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM instituto_ProgresoModulo
                WHERE EstatusModulo = 'En Progreso'
            """)
            in_progress = self.cursor.fetchone()[0] or 0

            return {
                'total_users': total_users,
                'total_modules': total_modules,
                'completed': completed,
                'in_progress': in_progress,
                'completion_rate': (completed / (total_users * total_modules * 1.0)) * 100 if total_users > 0 and total_modules > 0 else 0
            }

        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {
                'total_users': 0,
                'total_modules': 0,
                'completed': 0,
                'in_progress': 0,
                'completion_rate': 0
            }

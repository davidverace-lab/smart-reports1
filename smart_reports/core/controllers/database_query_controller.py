"""
Database Query Controller
Controlador para consultas a la base de datos (stub temporal)
"""


class DatabaseQueryController:
    """Controlador temporal para consultas de base de datos"""

    def __init__(self, connection=None, cursor=None):
        self.connection = connection
        self.cursor = cursor

    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL"""
        if not self.cursor:
            return []

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error ejecutando query: {e}")
            return []

    def fetch_one(self, query, params=None):
        """Obtiene un solo resultado"""
        results = self.execute_query(query, params)
        return results[0] if results else None

    def commit(self):
        """Hace commit de la transacción"""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """Hace rollback de la transacción"""
        if self.connection:
            self.connection.rollback()

    def verify_database_tables(self):
        """
        Verifica que las tablas necesarias existan en la base de datos

        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.connection or not self.cursor:
            return (False, "No hay conexión a la base de datos")

        try:
            # Verificar tablas principales
            required_tables = ['empleados', 'modulos', 'progreso_modulos']

            self.cursor.execute("SHOW TABLES")
            existing_tables = [table[0].lower() for table in self.cursor.fetchall()]

            missing_tables = [table for table in required_tables if table.lower() not in existing_tables]

            if missing_tables:
                return (False, f"Faltan las siguientes tablas: {', '.join(missing_tables)}")

            return (True, "Todas las tablas necesarias están presentes")

        except Exception as e:
            return (False, f"Error verificando tablas: {str(e)}")

"""
Detector de Tablas - Encuentra automáticamente las tablas correctas en la BD
"""

class TableDetector:
    """Detecta automáticamente el esquema y nombres de tablas"""

    def __init__(self, cursor):
        """
        Args:
            cursor: Cursor de la base de datos
        """
        self.cursor = cursor
        self.schema_prefix = ""
        self.table_mapping = {}
        self._detect_tables()

    def _detect_tables(self):
        """Detecta qué tablas existen y con qué prefijo"""
        # Nombres de tablas que buscamos (sin prefijo)
        base_tables = [
            'Usuario', 'Modulo', 'ProgresoModulo', 'Departamento',
            'UnidadDeNegocio', 'ResultadoEvaluacion', 'Evaluacion'
        ]

        # Prefijos posibles
        prefixes = ['Instituto.', 'Instituto_', 'dbo.', '']

        for table in base_tables:
            for prefix in prefixes:
                full_name = f"{prefix}{table}"
                if self._table_exists(full_name):
                    self.table_mapping[table] = full_name
                    break

            # Si no se encontró, usar nombre sin prefijo
            if table not in self.table_mapping:
                self.table_mapping[table] = table

    def _table_exists(self, table_name):
        """Verifica si una tabla existe"""
        try:
            self.cursor.execute(f"SELECT TOP 1 1 FROM {table_name}")
            return True
        except:
            return False

    def get_table_name(self, base_name):
        """
        Obtiene el nombre completo de la tabla

        Args:
            base_name: Nombre base (ej: 'Usuario')

        Returns:
            Nombre completo (ej: 'Instituto.Usuario' o 'Instituto_Usuario' o 'Usuario')
        """
        return self.table_mapping.get(base_name, base_name)

    def format_query(self, query):
        """
        Formatea una query reemplazando nombres de tablas

        Args:
            query: Query con nombres base (ej: FROM Usuario)

        Returns:
            Query con nombres correctos
        """
        formatted = query
        for base_name, full_name in self.table_mapping.items():
            # Reemplazar Instituto.NombreTabla con el nombre correcto
            formatted = formatted.replace(f"Instituto.{base_name}", full_name)
            formatted = formatted.replace(f"Instituto_{base_name}", full_name)

        return formatted

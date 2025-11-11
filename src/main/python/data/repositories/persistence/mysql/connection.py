"""
Gestión de conexión a Base de Datos (SQL Server y MySQL)
"""
from typing import Optional

# SQL Server support
try:
    import pyodbc
    SQLSERVER_AVAILABLE = True
except ImportError:
    pyodbc = None
    SQLSERVER_AVAILABLE = False

# MySQL support
try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
    MYSQL_AVAILABLE = True
except ImportError:
    mysql = None
    MySQLError = Exception
    MYSQL_AVAILABLE = False

from src.main.res.config.database import DB_TYPE, SQLSERVER_CONFIG, MYSQL_CONFIG


class DatabaseConnection:
    """Singleton para gestionar la conexión a la base de datos"""

    _instance = None
    _connection = None
    _cursor = None
    _db_type = DB_TYPE

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def connect(self):
        """Establece conexión con la base de datos según el tipo configurado"""
        if self._connection is not None:
            return self._connection

        try:
            if self._db_type == 'sqlserver':
                self._connection = self._connect_sqlserver()
            elif self._db_type == 'mysql':
                self._connection = self._connect_mysql()
            else:
                raise ValueError(f"Tipo de BD no soportado: {self._db_type}")

            self._cursor = self._connection.cursor()
            return self._connection

        except Exception as e:
            raise Exception(f"Error de conexión a BD ({self._db_type}): {str(e)}")

    def _connect_sqlserver(self):
        """Conexión a SQL Server usando pyodbc"""
        if not SQLSERVER_AVAILABLE:
            raise ImportError(
                "pyodbc no está instalado. Para SQL Server ejecuta:\n"
                "pip install pyodbc\n"
                "También necesitas ODBC Driver 17 for SQL Server instalado."
            )

        # Construir connection string
        server = SQLSERVER_CONFIG['server']
        port = SQLSERVER_CONFIG.get('port', 1433)

        # Si el puerto no es el default, agregarlo al servidor
        if port != 1433:
            server = f"{server},{port}"

        connection_string = (
            f"DRIVER={SQLSERVER_CONFIG['driver']};"
            f"SERVER={server};"
            f"DATABASE={SQLSERVER_CONFIG['database']};"
            f"UID={SQLSERVER_CONFIG['username']};"
            f"PWD={SQLSERVER_CONFIG['password']};"
            f"TrustServerCertificate=yes;"
        )

        return pyodbc.connect(connection_string)

    def _connect_mysql(self):
        """Conexión a MySQL usando mysql-connector-python"""
        if not MYSQL_AVAILABLE:
            raise ImportError(
                "mysql-connector-python no está instalado. Para MySQL ejecuta:\n"
                "pip install mysql-connector-python"
            )

        return mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            database=MYSQL_CONFIG['database'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            charset=MYSQL_CONFIG.get('charset', 'utf8mb4')
        )

    def get_cursor(self):
        """Retorna el cursor de la conexión"""
        if self._cursor is None:
            self.connect()
        return self._cursor

    def get_placeholder(self) -> str:
        """Retorna el placeholder de parámetros según el tipo de BD"""
        return '?' if self._db_type == 'sqlserver' else '%s'

    def commit(self):
        """Commit de transacción"""
        if self._connection:
            self._connection.commit()

    def rollback(self):
        """Rollback de transacción"""
        if self._connection:
            self._connection.rollback()

    def close(self):
        """Cierra la conexión"""
        if self._connection:
            self._connection.close()
            self._connection = None
            self._cursor = None

    def execute(self, query: str, params: Optional[tuple] = None):
        """Ejecuta una query y retorna resultados"""
        cursor = self.get_cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()

    def execute_one(self, query: str, params: Optional[tuple] = None):
        """Ejecuta query y retorna un solo resultado"""
        cursor = self.get_cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchone()

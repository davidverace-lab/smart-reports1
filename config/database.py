"""
Configuración de base de datos
"""
import os

# Configuración MySQL
MYSQL_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'tngcore'),
    'charset': 'utf8mb4',
    'autocommit': False
}

# Prefijo de tablas
TABLE_PREFIX = 'instituto_'

# Pool de conexiones
CONNECTION_POOL = {
    'pool_size': 5,
    'pool_name': 'smart_reports_pool',
    'pool_reset_session': True
}

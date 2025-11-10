"""
Configuración de base de datos - SOPORTE MULTI-DB
Soporta: SQL Server (trabajo) y MySQL (casa)
"""
import os

# ============================================================
# ⚙️ CONFIGURACIÓN PRINCIPAL - CAMBIA AQUÍ EL TIPO DE BD
# ============================================================
# Opciones: 'sqlserver' o 'mysql'
DB_TYPE = os.getenv('DB_TYPE', 'mysql')  # 👈 CAMBIA AQUÍ: 'sqlserver' o 'mysql'

# ============================================================
# 📊 CONFIGURACIÓN SQL SERVER (TRABAJO)
# ============================================================
SQLSERVER_CONFIG = {
    'server': '10.133.18.111',
    'port': 1433,
    'database': 'TNGCORE',
    'username': 'tngdatauser',
    'password': 'Password1',
    'driver': 'ODBC Driver 17 for SQL Server',
    'trusted_connection': 'no',
    'encrypt': 'yes',
    'trust_server_certificate': 'yes'
}

# ============================================================
# 🏠 CONFIGURACIÓN MYSQL (CASA)
# ============================================================
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'tngcore',
    'user': 'root',
    'password': 'Xbox360xd',
    'charset': 'utf8mb4',
    'autocommit': False
}

# ============================================================
# 🔧 CONFIGURACIÓN ACTIVA (AUTOMÁTICA)
# ============================================================
# Esta se selecciona automáticamente según DB_TYPE
ACTIVE_CONFIG = SQLSERVER_CONFIG if DB_TYPE == 'sqlserver' else MYSQL_CONFIG

# Prefijo de tablas (igual para ambas)
TABLE_PREFIX = 'instituto_'

# Pool de conexiones
CONNECTION_POOL = {
    'pool_size': 5,
    'pool_name': 'smart_reports_pool',
    'pool_reset_session': True
}

# ============================================================
# 📝 INSTRUCCIONES RÁPIDAS
# ============================================================
# OPCIÓN 1: Cambiar directamente en este archivo
#   - Cambia DB_TYPE = 'sqlserver' o 'mysql' arriba
#
# OPCIÓN 2: Usar variables de entorno (.env)
#   - DB_TYPE=sqlserver
#   - DB_HOST=tu_servidor
#   - DB_PORT=1433
#   - DB_NAME=tngcore
#   - DB_USER=tu_usuario
#   - DB_PASSWORD=tu_password
# ============================================================

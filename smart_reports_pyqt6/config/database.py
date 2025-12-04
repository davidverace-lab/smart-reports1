"""
Configuración de Base de Datos - Smart Reports
===============================================

Aquí configuras el tipo de base de datos y sus credenciales.

CAMBIAR TIPO DE BASE DE DATOS:
------------------------------
Edita la variable DB_TYPE abajo:
- DB_TYPE = 'mysql'      # Para MySQL
- DB_TYPE = 'sqlserver'  # Para SQL Server
"""
import os
from pathlib import Path

# Intentar cargar variables de entorno desde .env (si existe y python-dotenv instalado)
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    # python-dotenv no instalado, usar solo variables de entorno del sistema
    pass


# ============================================================================
# TIPO DE BASE DE DATOS
# ============================================================================
# 🔧 CAMBIA AQUÍ EL TIPO DE BD (mysql o sqlserver)
DB_TYPE = os.getenv('DB_TYPE', 'mysql')  # 👈 Cambiar aquí o en .env (ahora por defecto MySQL)


# ============================================================================
# CONFIGURACIÓN SQL SERVER (Trabajo/Producción)
# ============================================================================
SQLSERVER_CONFIG = {
    'driver': os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}'),
    'server': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '1433')),
    'database': os.getenv('DB_NAME', 'InstitutoHutchison'),
    'username': os.getenv('DB_USER', 'sa'),
    'password': os.getenv('DB_PASSWORD', ''),
    'trusted_connection': os.getenv('DB_TRUSTED', 'no').lower() == 'yes'
}


# ============================================================================
# CONFIGURACIÓN MYSQL (Casa/Desarrollo)
# ============================================================================
MYSQL_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'database': os.getenv('DB_NAME', 'InstitutoHutchison'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Xbox360xd'),  # Contraseña por defecto
    'charset': 'utf8mb4'
}


# ============================================================================
# VALIDACIÓN
# ============================================================================
def validar_configuracion():
    """Valida que la configuración de BD sea correcta"""
    if DB_TYPE not in ['mysql', 'sqlserver']:
        raise ValueError(
            f"❌ DB_TYPE inválido: '{DB_TYPE}'\n"
            f"✅ Opciones válidas: 'mysql' o 'sqlserver'\n"
            f"📝 Edita: smart_reports/config/database.py línea 21"
        )

    return True


# Validar al importar
validar_configuracion()


# ============================================================================
# AYUDA RÁPIDA
# ============================================================================
"""
🔧 CÓMO CAMBIAR LA BASE DE DATOS:
---------------------------------

OPCIÓN 1 - Editar directamente este archivo (database.py):
    Línea 21: DB_TYPE = 'sqlserver'  # Cambiar a 'mysql' o 'sqlserver'

OPCIÓN 2 - Usar archivo .env (recomendado para producción):
    1. Copia .env.example a .env
    2. Edita .env y configura:
       DB_TYPE=sqlserver
       DB_HOST=tu_servidor
       DB_NAME=tu_base_datos
       DB_USER=tu_usuario
       DB_PASSWORD=tu_password

OPCIÓN 3 - Variables de entorno del sistema:
    set DB_TYPE=sqlserver
    set DB_HOST=mi_servidor
    set DB_NAME=InstitutoHutchison


📋 EJEMPLOS:
-----------

Para SQL Server local:
    DB_TYPE = 'sqlserver'
    SQLSERVER_CONFIG = {
        'server': 'localhost',
        'database': 'InstitutoHutchison',
        'username': 'sa',
        'password': 'MiPassword123'
    }

Para MySQL local:
    DB_TYPE = 'mysql'
    MYSQL_CONFIG = {
        'host': 'localhost',
        'database': 'tngcore',
        'user': 'root',
        'password': 'mipassword'
    }
"""

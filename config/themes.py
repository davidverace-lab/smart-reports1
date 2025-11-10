"""
Configuración global del sistema Smart Reports
"""

# ============================================
# CONFIGURACIÓN DE BASE DE DATOS
# ============================================

# Tipo de base de datos: 'sqlserver' o 'mysql'
DB_TYPE = 'mysql'  # Cambiar a 'sqlserver' para usar base de datos del trabajo

# Configuración SQL Server (Trabajo)
SQLSERVER_CONFIG = {
    'server': '10.133.18.111',
    'database': 'TNGCORE',
    'username': 'tngdatauser',
    'password': 'Password1',
    'driver': 'ODBC Driver 17 for SQL Server'
}

# Configuración MySQL (Casa)
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'tngcore',
    'user': 'root',
    'password': 'Xbox360xd'
}

# Configuración activa (se establece según DB_TYPE)
DATABASE_CONFIG = SQLSERVER_CONFIG if DB_TYPE == 'sqlserver' else MYSQL_CONFIG

# ============================================
# PALETAS DE COLORES - HUTCHISON PORTS BRANDING
# ============================================

# Colores Corporativos Hutchison Ports (Brand Guidelines)
HUTCHISON_COLORS = {
    # Colores Principales
    'ports_sky_blue': '#009BDE',      # Color principal de acción/botones
    'ports_sea_blue': '#002E6D',      # Azul marino corporativo
    'ports_horizon_blue': '#9ACAEB',  # Azul claro/suave

    # Colores Secundarios (usar con moderación)
    'aqua_green': '#00B5AD',          # Verde agua
    'sunray_yellow': '#FFD700',       # Amarillo énfasis
    'sunset_orange': '#FF6B35',       # Naranja cálido

    # Colores de Estado
    'success': '#00B5AD',             # Verde agua (éxito)
    'warning': '#FFD700',             # Amarillo (advertencia)
    'danger': '#FF6B35',              # Naranja (peligro)
}

# Paleta Oscura (Tema por defecto) - Adaptada a Hutchison Ports
DARK_THEME = {
    'background': '#1a1d2e',
    'surface': '#2b2d42',
    'surface_light': '#3a3d5a',
    'surface_dark': '#1a1d2e',        # Para contraste en modo oscuro
    'primary': '#009BDE',             # Ports Sky Blue
    'secondary': '#002E6D',           # Ports Sea Blue
    'accent': '#9ACAEB',              # Ports Horizon Blue
    'success': '#00B5AD',             # Aqua Green
    'warning': '#FFD700',             # Sunray Yellow
    'danger': '#FF6B35',              # Sunset Orange
    'text': '#ffffff',
    'text_secondary': '#a0a0a0',
    'text_tertiary': '#808080',       # Texto terciario (más tenue)
    'text_light': '#808080',          # Texto más claro
    'border': '#444654',
    'border_light': '#555570',        # Bordes claros
    'edited': '#FFF59D',
    'card_bg': '#2b2d42',             # Fondo de cards
    'hover': '#3a3d5a'                # Color hover
}

# Paleta Clara - Adaptada a Hutchison Ports
LIGHT_THEME = {
    'background': '#f0f2f5',          # Gris muy claro para fondo principal
    'surface': '#ffffff',             # Blanco para cards/paneles
    'surface_light': '#e8f4f8',       # Azul muy claro Hutchison
    'surface_dark': '#d0d0d0',        # Para contraste en modo claro
    'primary': '#009BDE',             # Ports Sky Blue
    'secondary': '#002E6D',           # Ports Sea Blue
    'accent': '#9ACAEB',              # Ports Horizon Blue
    'success': '#00B5AD',             # Aqua Green
    'warning': '#FFD700',             # Sunray Yellow
    'danger': '#FF6B35',              # Sunset Orange
    'text': '#002E6D',                # Texto principal - Ports Sea Blue
    'text_secondary': '#555555',      # Texto secundario
    'text_tertiary': '#777777',       # Texto terciario (más tenue)
    'text_light': '#777777',          # Texto más claro
    'border': '#d0d0d0',              # Bordes
    'border_light': '#e8e8e8',        # Bordes claros
    'edited': '#FFF59D',
    'card_bg': '#ffffff',             # Fondo de cards
    'hover': '#e8f4f8'                # Color hover
}

# Paleta Ejecutiva para Gráficos (Priorizar azules corporativos)
EXECUTIVE_CHART_COLORS = [
    '#009BDE',  # Ports Sky Blue
    '#002E6D',  # Ports Sea Blue
    '#9ACAEB',  # Ports Horizon Blue
    '#00B5AD',  # Aqua Green (para destacar)
    '#FFD700',  # Sunray Yellow (para énfasis)
    '#FF6B35',  # Sunset Orange (para alertas)
]

# Colores corporativos (Compatibilidad con código existente)
COLORS = {
    'primary': '#009BDE',      # Ports Sky Blue
    'secondary': '#002E6D',    # Ports Sea Blue
    'accent': '#9ACAEB',       # Ports Horizon Blue
    'success': '#00B5AD',      # Aqua Green
    'warning': '#FFD700',      # Sunray Yellow
    'danger': '#FF6B35',       # Sunset Orange
    'dark': '#1a1d2e',         # Fondo oscuro
    'light': '#F7F7F7',        # Gris claro
    'edited': '#FFF59D'        # Amarillo para celdas editadas
}

# Configuración de la aplicación
APP_CONFIG = {
    'title': 'SMART REPORTS - INSTITUTO HP',
    'version': '2.0',
    'geometry': '1400x800',
    'theme': 'darkly',
    'company': 'Instituto Hutchison Ports'
}

# Rutas de archivos
PATHS = {
    'logo': 'assets/logo.png',
    'reports': 'reports/',
    'logs': 'logs/',
    'backups': 'backups/'
}

# Estados de módulos
MODULE_STATUSES = ['Completado', 'En proceso', 'Registrado', 'No iniciado']

# Configuración de PDFs
PDF_CONFIG = {
    'page_size': 'letter',
    'title_font_size': 24,
    'subtitle_font_size': 16,
    'normal_font_size': 10,
    'logo_width': 2,  # inches
    'logo_height': 0.8  # inches
}

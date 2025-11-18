"""
Temas y Colores Corporativos - Hutchison Ports
===============================================

Define los colores y temas de la aplicación según el branding de Hutchison Ports.
"""

# ============================================================================
# COLORES CORPORATIVOS HUTCHISON PORTS
# ============================================================================

HUTCHISON_COLORS = {
    # Colores principales
    'primary': '#003087',        # Azul corporativo Hutchison
    'secondary': '#00A651',      # Verde corporativo
    'accent': '#FFB81C',         # Amarillo/Naranja de acento

    # Colores de fondo
    'bg_dark': '#1a1a1a',        # Fondo oscuro principal
    'bg_medium': '#2b2b2b',      # Fondo oscuro secundario
    'bg_light': '#f5f5f5',       # Fondo claro
    'bg_card_dark': '#2d2d2d',   # Fondo de tarjetas modo oscuro
    'bg_card_light': '#ffffff',  # Fondo de tarjetas modo claro

    # Colores de texto
    'text_primary': '#ffffff',   # Texto principal (modo oscuro)
    'text_secondary': '#b0b0b0', # Texto secundario (modo oscuro)
    'text_dark': '#1a1a1a',      # Texto para modo claro
    'text_muted': '#666666',     # Texto apagado

    # Colores de estado
    'success': '#00A651',        # Verde éxito
    'warning': '#FFB81C',        # Amarillo advertencia
    'error': '#D32F2F',          # Rojo error
    'info': '#2196F3',           # Azul información

    # Colores de gráficos
    'chart_1': '#003087',        # Azul
    'chart_2': '#00A651',        # Verde
    'chart_3': '#FFB81C',        # Amarillo
    'chart_4': '#D32F2F',        # Rojo
    'chart_5': '#9C27B0',        # Púrpura
    'chart_6': '#FF9800',        # Naranja

    # Bordes y divisores
    'border_dark': '#404040',    # Bordes modo oscuro
    'border_light': '#e0e0e0',   # Bordes modo claro
    'divider': '#333333',        # Divisores

    # Hover y estados interactivos
    'hover_dark': '#383838',     # Hover modo oscuro
    'hover_light': '#f0f0f0',    # Hover modo claro
    'selected': '#004099',       # Elemento seleccionado
    'disabled': '#555555',       # Elementos deshabilitados
}


# ============================================================================
# TEMA OSCURO (DARK MODE)
# ============================================================================

DARK_THEME = {
    'name': 'dark',
    'colors': {
        # Fondos
        'background': HUTCHISON_COLORS['bg_dark'],
        'background_secondary': HUTCHISON_COLORS['bg_medium'],
        'card_background': HUTCHISON_COLORS['bg_card_dark'],

        # Textos
        'text': HUTCHISON_COLORS['text_primary'],
        'text_secondary': HUTCHISON_COLORS['text_secondary'],
        'text_muted': HUTCHISON_COLORS['text_muted'],

        # Elementos UI
        'primary': HUTCHISON_COLORS['primary'],
        'secondary': HUTCHISON_COLORS['secondary'],
        'accent': HUTCHISON_COLORS['accent'],

        # Bordes y divisores
        'border': HUTCHISON_COLORS['border_dark'],
        'divider': HUTCHISON_COLORS['divider'],

        # Estados
        'hover': HUTCHISON_COLORS['hover_dark'],
        'selected': HUTCHISON_COLORS['selected'],
        'disabled': HUTCHISON_COLORS['disabled'],

        # Estados de información
        'success': HUTCHISON_COLORS['success'],
        'warning': HUTCHISON_COLORS['warning'],
        'error': HUTCHISON_COLORS['error'],
        'info': HUTCHISON_COLORS['info'],
    }
}


# ============================================================================
# TEMA CLARO (LIGHT MODE)
# ============================================================================

LIGHT_THEME = {
    'name': 'light',
    'colors': {
        # Fondos
        'background': HUTCHISON_COLORS['bg_light'],
        'background_secondary': '#e8e8e8',
        'card_background': HUTCHISON_COLORS['bg_card_light'],

        # Textos
        'text': HUTCHISON_COLORS['text_dark'],
        'text_secondary': '#4a4a4a',
        'text_muted': HUTCHISON_COLORS['text_muted'],

        # Elementos UI
        'primary': HUTCHISON_COLORS['primary'],
        'secondary': HUTCHISON_COLORS['secondary'],
        'accent': HUTCHISON_COLORS['accent'],

        # Bordes y divisores
        'border': HUTCHISON_COLORS['border_light'],
        'divider': '#d0d0d0',

        # Estados
        'hover': HUTCHISON_COLORS['hover_light'],
        'selected': '#e3f2fd',
        'disabled': '#bdbdbd',

        # Estados de información
        'success': HUTCHISON_COLORS['success'],
        'warning': '#F57C00',
        'error': HUTCHISON_COLORS['error'],
        'info': HUTCHISON_COLORS['info'],
    }
}


# ============================================================================
# PALETA DE COLORES PARA GRÁFICOS
# ============================================================================

CHART_COLORS = [
    HUTCHISON_COLORS['chart_1'],  # Azul
    HUTCHISON_COLORS['chart_2'],  # Verde
    HUTCHISON_COLORS['chart_3'],  # Amarillo
    HUTCHISON_COLORS['chart_4'],  # Rojo
    HUTCHISON_COLORS['chart_5'],  # Púrpura
    HUTCHISON_COLORS['chart_6'],  # Naranja
]


# ============================================================================
# GRADIENTES CORPORATIVOS
# ============================================================================

GRADIENTS = {
    'primary': ['#003087', '#0055cc'],      # Azul corporativo
    'success': ['#00A651', '#00d668'],      # Verde éxito
    'warning': ['#FFB81C', '#ffd54f'],      # Amarillo advertencia
    'danger': ['#D32F2F', '#f44336'],       # Rojo peligro
}


# ============================================================================
# FUNCIÓN AUXILIAR PARA OBTENER TEMA
# ============================================================================

def get_theme(mode='dark'):
    """
    Obtiene el tema según el modo especificado.

    Args:
        mode (str): 'dark' o 'light'

    Returns:
        dict: Diccionario con los colores del tema
    """
    if mode.lower() == 'dark':
        return DARK_THEME
    elif mode.lower() == 'light':
        return LIGHT_THEME
    else:
        # Por defecto retornar tema oscuro
        return DARK_THEME


def get_color(color_name, theme_mode='dark'):
    """
    Obtiene un color específico del tema.

    Args:
        color_name (str): Nombre del color
        theme_mode (str): 'dark' o 'light'

    Returns:
        str: Código hexadecimal del color
    """
    theme = get_theme(theme_mode)
    return theme['colors'].get(color_name, HUTCHISON_COLORS['primary'])

"""
Sistema de Temas para PyQt6 usando QSS (Qt StyleSheets)
Instituto Hutchison Ports - Smart Reports
Reemplaza el sistema de temas de CustomTkinter
"""

# Colores Hutchison Ports
HUTCHISON_COLORS = {
    # Colores primarios
    'primary': '#002E6D',          # Navy
    'primary_hover': '#001a3d',    # Navy oscuro
    'secondary': '#0066CC',        # Royal blue
    'accent': '#00D4AA',           # Aqua green
    'aqua_green': '#00D4AA',       # Aqua green

    # Estados
    'success': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#f44336',
    'info': '#2196F3',

    # Escala de azules
    'navy': '#002E6D',
    'navy_blue': '#003D82',
    'royal_blue_dark': '#004C97',
    'royal_blue': '#0066CC',
    'azure_blue': '#0080FF',
    'sky_blue': '#009BDE',
    'horizon_blue': '#00B5E2',
    'light_blue': '#33C7F0',
    'lighter_blue': '#66D4F5',
    'very_light_blue': '#99E1FA',
}

# Tema Oscuro (Dark Mode)
DARK_THEME_QSS = f"""
/* ==================== TEMA OSCURO ==================== */

/* Ventana Principal */
QMainWindow {{
    background-color: #1a1a1a;
    color: #ffffff;
}}

/* Widgets generales */
QWidget {{
    background-color: #1a1a1a;
    color: #ffffff;
    font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
}}

/* Frames y paneles */
QFrame {{
    background-color: #1a1a1a;
    border-radius: 0px;
    border: 1px solid #1a1a1a;
}}

/* Labels */
QLabel {{
    background-color: transparent;
    color: #ffffff;
}}

/* Botones */
QPushButton {{
    background-color: {HUTCHISON_COLORS['primary']};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    min-height: 35px;
}}

QPushButton:hover {{
    background-color: {HUTCHISON_COLORS['primary_hover']};
}}

QPushButton:pressed {{
    background-color: #000f26;
}}

QPushButton:disabled {{
    background-color: #555555;
    color: #888888;
}}

/* Botones secundarios */
QPushButton[class="secondary"] {{
    background-color: #383838;
    color: white;
}}

QPushButton[class="secondary"]:hover {{
    background-color: #4a4a4a;
}}

/* Botones de peligro */
QPushButton[class="danger"] {{
    background-color: {HUTCHISON_COLORS['danger']};
}}

QPushButton[class="danger"]:hover {{
    background-color: #d32f2f;
}}

/* Line Edit (campos de texto) */
QLineEdit {{
    background-color: #2d2d2d;
    color: #ffffff;
    border: 2px solid #383838;
    border-radius: 0px;
    padding: 10px;
    min-height: 35px;
}}

QLineEdit:focus {{
    border: 2px solid {HUTCHISON_COLORS['primary']};
}}

/* Text Edit */
QTextEdit {{
    background-color: #2d2d2d;
    color: #ffffff;
    border: 2px solid #383838;
    border-radius: 0px;
    padding: 8px;
}}

QTextEdit:focus {{
    border: 2px solid {HUTCHISON_COLORS['primary']};
}}

/* Combo Box */
QComboBox {{
    background-color: #2d2d2d;
    color: #ffffff;
    border: 2px solid #383838;
    border-radius: 0px;
    padding: 10px;
    min-height: 35px;
}}

QComboBox:hover {{
    border: 2px solid {HUTCHISON_COLORS['primary']};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: url(none);
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #ffffff;
    margin-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: #2d2d2d;
    color: #ffffff;
    selection-background-color: {HUTCHISON_COLORS['primary']};
    border: 1px solid #383838;
}}

/* List Widget */
QListWidget {{
    background-color: #2d2d2d;
    color: #ffffff;
    border: 2px solid #383838;
    border-radius: 0px;
}}

QListWidget::item {{
    padding: 10px;
    border-bottom: 1px solid #383838;
}}

QListWidget::item:selected {{
    background-color: {HUTCHISON_COLORS['primary']};
    color: white;
}}

QListWidget::item:hover {{
    background-color: #383838;
}}

/* Table Widget */
QTableWidget {{
    background-color: #2d2d2d;
    color: #ffffff;
    gridline-color: #383838;
    border: 1px solid #383838;
}}

QTableWidget::item {{
    padding: 8px;
}}

QTableWidget::item:selected {{
    background-color: {HUTCHISON_COLORS['primary']};
    color: white;
}}

QHeaderView::section {{
    background-color: #1a1a1a;
    color: #ffffff;
    padding: 10px;
    border: 1px solid #383838;
    font-weight: bold;
}}

/* Scroll Bar */
QScrollBar:vertical {{
    background-color: #2d2d2d;
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: #555555;
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {HUTCHISON_COLORS['primary']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: #2d2d2d;
    height: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal {{
    background-color: #555555;
    border-radius: 6px;
    min-width: 20px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {HUTCHISON_COLORS['primary']};
}}

/* Menu Bar */
QMenuBar {{
    background-color: #1a1a1a;
    color: #ffffff;
    padding: 5px;
}}

QMenuBar::item:selected {{
    background-color: {HUTCHISON_COLORS['primary']};
}}

QMenu {{
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #383838;
}}

QMenu::item:selected {{
    background-color: {HUTCHISON_COLORS['primary']};
}}

/* Status Bar */
QStatusBar {{
    background-color: #1a1a1a;
    color: #b0b0b0;
}}

/* Progress Bar */
QProgressBar {{
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #383838;
    border-radius: 8px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {HUTCHISON_COLORS['primary']};
    border-radius: 7px;
}}

/* Tab Widget */
QTabWidget::pane {{
    background-color: #2d2d2d;
    border: 1px solid #383838;
    border-radius: 0px;
}}

QTabBar::tab {{
    background-color: #383838;
    color: #ffffff;
    padding: 10px 20px;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: {HUTCHISON_COLORS['primary']};
}}

QTabBar::tab:hover {{
    background-color: #4a4a4a;
}}

/* CheckBox */
QCheckBox {{
    color: #ffffff;
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border: 2px solid #383838;
    border-radius: 0px;
    background-color: #2d2d2d;
}}

QCheckBox::indicator:checked {{
    background-color: {HUTCHISON_COLORS['primary']};
    border-color: {HUTCHISON_COLORS['primary']};
}}

/* Radio Button */
QRadioButton {{
    color: #ffffff;
    spacing: 8px;
}}

QRadioButton::indicator {{
    width: 20px;
    height: 20px;
    border: 2px solid #383838;
    border-radius: 10px;
    background-color: #2d2d2d;
}}

QRadioButton::indicator:checked {{
    background-color: {HUTCHISON_COLORS['primary']};
    border-color: {HUTCHISON_COLORS['primary']};
}}

/* Tooltips */
QToolTip {{
    background-color: {HUTCHISON_COLORS['primary']};
    color: white;
    border: 1px solid {HUTCHISON_COLORS['primary_hover']};
    padding: 5px;
    border-radius: 4px;
}}
"""

# Tema Claro (Light Mode)
LIGHT_THEME_QSS = f"""
/* ==================== TEMA CLARO ==================== */

/* Ventana Principal */
QMainWindow {{
    background-color: #f5f5f5;
    color: #003087;
}}

/* Widgets generales */
QWidget {{
    background-color: #f5f5f5;
    color: #003087;
    font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
}}

/* Frames y paneles */
QFrame {{
    background-color: #f5f5f5;
    border-radius: 0px;
    border: 1px solid #f5f5f5;
}}

/* Labels */
QLabel {{
    background-color: transparent;
    color: #003087;
}}

/* Botones */
QPushButton {{
    background-color: {HUTCHISON_COLORS['primary']};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    min-height: 35px;
}}

QPushButton:hover {{
    background-color: {HUTCHISON_COLORS['primary_hover']};
}}

QPushButton:pressed {{
    background-color: #000f26;
}}

QPushButton:disabled {{
    background-color: #cccccc;
    color: #888888;
}}

/* Botones secundarios */
QPushButton[class="secondary"] {{
    background-color: #e0e0e0;
    color: #003087;
}}

QPushButton[class="secondary"]:hover {{
    background-color: #d0d0d0;
}}

/* Botones de peligro */
QPushButton[class="danger"] {{
    background-color: {HUTCHISON_COLORS['danger']};
    color: white;
}}

QPushButton[class="danger"]:hover {{
    background-color: #d32f2f;
}}

/* Line Edit (campos de texto) */
QLineEdit {{
    background-color: #ffffff;
    color: #003087;
    border: 2px solid #e0e0e0;
    border-radius: 0px;
    padding: 10px;
    min-height: 35px;
}}

QLineEdit:focus {{
    border: 2px solid {HUTCHISON_COLORS['primary']};
}}

/* Text Edit */
QTextEdit {{
    background-color: #ffffff;
    color: #003087;
    border: 2px solid #e0e0e0;
    border-radius: 0px;
    padding: 8px;
}}

QTextEdit:focus {{
    border: 2px solid {HUTCHISON_COLORS['primary']};
}}

/* Combo Box */
QComboBox {{
    background-color: #ffffff;
    color: #003087;
    border: 2px solid #e0e0e0;
    border-radius: 0px;
    padding: 10px;
    min-height: 35px;
}}

QComboBox:hover {{
    border: 2px solid {HUTCHISON_COLORS['primary']};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: url(none);
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #003087;
    margin-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: #ffffff;
    color: #003087;
    selection-background-color: {HUTCHISON_COLORS['primary']};
    border: 1px solid #e0e0e0;
}}

/* List Widget */
QListWidget {{
    background-color: #ffffff;
    color: #003087;
    border: 2px solid #e0e0e0;
    border-radius: 0px;
}}

QListWidget::item {{
    padding: 10px;
    border-bottom: 1px solid #e0e0e0;
}}

QListWidget::item:selected {{
    background-color: {HUTCHISON_COLORS['primary']};
    color: white;
}}

QListWidget::item:hover {{
    background-color: #f0f0f0;
}}

/* Table Widget */
QTableWidget {{
    background-color: #ffffff;
    color: #003087;
    gridline-color: #e0e0e0;
    border: 1px solid #e0e0e0;
}}

QTableWidget::item {{
    padding: 8px;
}}

QTableWidget::item:selected {{
    background-color: {HUTCHISON_COLORS['primary']};
    color: white;
}}

QHeaderView::section {{
    background-color: #f5f5f5;
    color: #003087;
    padding: 10px;
    border: 1px solid #e0e0e0;
    font-weight: bold;
}}

/* Scroll Bar */
QScrollBar:vertical {{
    background-color: #f5f5f5;
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: #cccccc;
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {HUTCHISON_COLORS['primary']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: #f5f5f5;
    height: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal {{
    background-color: #cccccc;
    border-radius: 6px;
    min-width: 20px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {HUTCHISON_COLORS['primary']};
}}

/* Menu Bar */
QMenuBar {{
    background-color: #ffffff;
    color: #003087;
    padding: 5px;
    border-bottom: 1px solid #e0e0e0;
}}

QMenuBar::item:selected {{
    background-color: {HUTCHISON_COLORS['primary']};
    color: white;
}}

QMenu {{
    background-color: #ffffff;
    color: #003087;
    border: 1px solid #e0e0e0;
}}

QMenu::item:selected {{
    background-color: {HUTCHISON_COLORS['primary']};
    color: white;
}}

/* Status Bar */
QStatusBar {{
    background-color: #ffffff;
    color: #4a5c8a;
    border-top: 1px solid #e0e0e0;
}}

/* Progress Bar */
QProgressBar {{
    background-color: #f5f5f5;
    color: #003087;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {HUTCHISON_COLORS['primary']};
    border-radius: 7px;
}}

/* Tab Widget */
QTabWidget::pane {{
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 0px;
}}

QTabBar::tab {{
    background-color: #e0e0e0;
    color: #003087;
    padding: 10px 20px;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: {HUTCHISON_COLORS['primary']};
    color: white;
}}

QTabBar::tab:hover {{
    background-color: #d0d0d0;
}}

/* CheckBox */
QCheckBox {{
    color: #003087;
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border: 2px solid #e0e0e0;
    border-radius: 0px;
    background-color: #ffffff;
}}

QCheckBox::indicator:checked {{
    background-color: {HUTCHISON_COLORS['primary']};
    border-color: {HUTCHISON_COLORS['primary']};
}}

/* Radio Button */
QRadioButton {{
    color: #003087;
    spacing: 8px;
}}

QRadioButton::indicator {{
    width: 20px;
    height: 20px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    background-color: #ffffff;
}}

QRadioButton::indicator:checked {{
    background-color: {HUTCHISON_COLORS['primary']};
    border-color: {HUTCHISON_COLORS['primary']};
}}

/* Tooltips */
QToolTip {{
    background-color: {HUTCHISON_COLORS['primary']};
    color: white;
    border: 1px solid {HUTCHISON_COLORS['primary_hover']};
    padding: 5px;
    border-radius: 4px;
}}
"""


from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication


class ThemeManager(QObject):
    """Gestor de temas para PyQt6"""

    # Signal emitido cuando cambia el tema
    theme_changed = pyqtSignal(str)  # Emite el nuevo tema ('dark' o 'light')

    def __init__(self):
        super().__init__()
        self.current_theme = 'dark'  # 'dark' o 'light'

    def get_stylesheet(self, theme: str = None) -> str:
        """Obtener stylesheet QSS del tema"""
        if theme is None:
            theme = self.current_theme

        if theme == 'dark':
            return DARK_THEME_QSS
        else:
            return LIGHT_THEME_QSS

    def set_theme(self, app, theme: str):
        """Aplicar tema a la aplicación"""
        self.current_theme = theme

        # Aplicar stylesheet global
        if isinstance(app, QApplication):
            app.setStyleSheet(self.get_stylesheet(theme))
        else:
            # Si es una ventana, obtener la aplicación
            QApplication.instance().setStyleSheet(self.get_stylesheet(theme))

        # Emitir signal de cambio de tema
        self.theme_changed.emit(theme)

        # Forzar actualización de todos los widgets
        if isinstance(app, QApplication):
            for widget in app.allWidgets():
                widget.update()
        else:
            app.update()

    def toggle_theme(self, app):
        """Alternar entre tema oscuro y claro"""
        new_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.set_theme(app, new_theme)
        return new_theme

    def is_dark_mode(self) -> bool:
        """Verificar si está en modo oscuro"""
        return self.current_theme == 'dark'

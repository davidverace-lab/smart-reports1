"""
ModernSidebar - PyQt6
Barra lateral moderna con navegación y botón hamburguesa para colapsar/expandir
"""

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QFont


class ModernSidebar(QFrame):
    """Sidebar moderna con logo, navegación y footer - COLAPSABLE"""

    # Signals
    navigation_clicked = pyqtSignal(str)
    logout_clicked = pyqtSignal()

    def __init__(self, parent=None, navigation_callbacks=None, theme_manager=None):
        """
        Args:
            parent: Widget padre
            navigation_callbacks: Dict con {nombre: callback_function}
            theme_manager: Gestor de temas
        """
        super().__init__(parent)

        self.navigation_callbacks = navigation_callbacks or {}
        self.theme_manager = theme_manager
        self.nav_buttons = {}
        self.active_button = None

        # Estado de colapso
        self.is_collapsed = False
        self.expanded_width = 240
        self.collapsed_width = 70

        # Configurar sidebar
        self.setFixedWidth(self.expanded_width)
        self.setObjectName("modernSidebar")

        # Crear UI
        self._create_ui()

        # Aplicar tema inicial
        self._update_theme()

    def _create_ui(self):
        """Crear interfaz completa"""

        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 15, 10, 20)
        self.main_layout.setSpacing(10)

        # Header con botón hamburguesa
        self._create_header()

        self.main_layout.addSpacing(20)

        # Navegación
        self._create_navigation()

        # Spacer para empujar elementos al fondo
        self.main_layout.addStretch()

        # Toggle de tema
        self._create_theme_toggle()

        # Footer
        self._create_footer()

    def _create_header(self):
        """Crear header con botón hamburguesa y logo"""

        # Container del header
        header_container = QWidget()
        header_container.setObjectName("headerContainer")
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)

        # Botón hamburguesa
        self.collapse_btn = QPushButton("☰")
        self.collapse_btn.setFont(QFont("Montserrat", 24, QFont.Weight.Bold))
        self.collapse_btn.setFixedSize(50, 40)
        self.collapse_btn.setObjectName("hamburgerBtn")
        self.collapse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.collapse_btn.clicked.connect(self._toggle_collapse)
        header_layout.addWidget(self.collapse_btn, alignment=Qt.AlignmentFlag.AlignTop)

        # Frame del logo (colapsable)
        self.logo_frame = QWidget()
        self.logo_frame.setObjectName("logoFrame")
        logo_layout = QVBoxLayout(self.logo_frame)
        logo_layout.setContentsMargins(10, 10, 10, 10)
        logo_layout.setSpacing(2)

        # Título principal
        self.logo_label = QLabel("SMART\nREPORTS")
        self.logo_label.setFont(QFont("Montserrat", 26, QFont.Weight.Bold))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setWordWrap(True)
        logo_layout.addWidget(self.logo_label)

        # Subtítulo
        self.subtitle = QLabel("Instituto Hutchison Ports")
        self.subtitle.setFont(QFont("Montserrat", 10))
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setWordWrap(True)
        logo_layout.addWidget(self.subtitle)

        header_layout.addWidget(self.logo_frame)

        # Línea separadora
        self.header_separator = QFrame()
        self.header_separator.setFrameShape(QFrame.Shape.HLine)
        self.header_separator.setFixedHeight(1)
        self.header_separator.setObjectName("separator")
        header_layout.addWidget(self.header_separator)

        self.main_layout.addWidget(header_container)

    def _create_navigation(self):
        """Crear botones de navegación"""

        nav_items = [
            ('Dashboards', 'dashboard'),
            ('Consulta de Empleados', 'consultas'),
            ('Importación de Datos', 'importacion'),
            ('Generar Reportes', 'reportes'),
            ('Configuración', 'configuracion'),
        ]

        for text, key in nav_items:
            btn = QPushButton(text)
            btn.setFont(QFont("Montserrat", 13, QFont.Weight.Bold))
            btn.setFixedHeight(50)
            btn.setObjectName("navButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, k=key: self._on_nav_click(k))

            # Guardar referencia al texto completo
            btn.setProperty("fullText", text)
            btn.setProperty("shortText", text[:3].upper())
            btn.setProperty("navKey", key)

            self.nav_buttons[key] = btn
            self.main_layout.addWidget(btn)

    def _create_theme_toggle(self):
        """Crear toggle para modo claro/oscuro"""

        # Frame para el toggle
        self.toggle_frame = QWidget()
        self.toggle_frame.setObjectName("toggleFrame")
        toggle_layout = QVBoxLayout(self.toggle_frame)
        toggle_layout.setContentsMargins(5, 15, 5, 5)
        toggle_layout.setSpacing(10)

        # Línea separadora superior
        self.theme_separator_top = QFrame()
        self.theme_separator_top.setFrameShape(QFrame.Shape.HLine)
        self.theme_separator_top.setFixedHeight(1)
        self.theme_separator_top.setObjectName("separator")
        toggle_layout.addWidget(self.theme_separator_top)

        # Container horizontal
        toggle_container = QWidget()
        toggle_container_layout = QHBoxLayout(toggle_container)
        toggle_container_layout.setContentsMargins(10, 0, 10, 0)

        # Label (sin icono)
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else True
        self.theme_label = QLabel('Modo Oscuro' if is_dark else 'Modo Claro')
        self.theme_label.setFont(QFont("Montserrat", 12, QFont.Weight.Bold))
        toggle_container_layout.addWidget(self.theme_label)

        toggle_container_layout.addStretch()

        # Botón de toggle (switch simulado)
        self.theme_btn = QPushButton("DARK" if is_dark else "LIGHT")
        self.theme_btn.setFont(QFont("Montserrat", 9, QFont.Weight.Bold))
        self.theme_btn.setFixedSize(55, 26)
        self.theme_btn.setObjectName("themeToggleBtn")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self._on_theme_toggle)
        toggle_container_layout.addWidget(self.theme_btn)

        toggle_layout.addWidget(toggle_container)

        # Línea separadora inferior
        self.theme_separator_bottom = QFrame()
        self.theme_separator_bottom.setFrameShape(QFrame.Shape.HLine)
        self.theme_separator_bottom.setFixedHeight(1)
        self.theme_separator_bottom.setObjectName("separator")
        toggle_layout.addWidget(self.theme_separator_bottom)

        self.main_layout.addWidget(self.toggle_frame)

    def _create_footer(self):
        """Crear footer con botón de cerrar sesión"""

        self.footer_frame = QWidget()
        self.footer_frame.setObjectName("footerFrame")
        footer_layout = QVBoxLayout(self.footer_frame)
        footer_layout.setContentsMargins(10, 10, 10, 10)
        footer_layout.setSpacing(10)

        # Línea separadora superior
        self.footer_separator = QFrame()
        self.footer_separator.setFrameShape(QFrame.Shape.HLine)
        self.footer_separator.setFixedHeight(1)
        self.footer_separator.setObjectName("separator")
        footer_layout.addWidget(self.footer_separator)

        # Botón de cerrar sesión
        self.logout_btn = QPushButton("Cerrar Sesión")
        self.logout_btn.setFont(QFont("Montserrat", 12, QFont.Weight.Bold))
        self.logout_btn.setFixedHeight(45)
        self.logout_btn.setObjectName("logoutButton")
        self.logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logout_btn.clicked.connect(self.logout_clicked.emit)
        footer_layout.addWidget(self.logout_btn)

        self.main_layout.addWidget(self.footer_frame)

    def _toggle_collapse(self):
        """Toggle colapso del sidebar"""

        self.is_collapsed = not self.is_collapsed

        if self.is_collapsed:
            # Colapsar
            self.setFixedWidth(self.collapsed_width)

            # Ocultar logo
            self.logo_frame.hide()
            self.header_separator.hide()

            # Actualizar botones para mostrar texto corto
            for key, btn in self.nav_buttons.items():
                short_text = btn.property("shortText")
                btn.setText(short_text)
                btn.setToolTip(btn.property("fullText"))

            # Ocultar elementos del toggle de tema
            self.theme_label.hide()
            self.theme_separator_top.hide()
            self.theme_separator_bottom.hide()

            # Ocultar footer
            self.logout_btn.hide()
            self.footer_separator.hide()

        else:
            # Expandir
            self.setFixedWidth(self.expanded_width)

            # Mostrar logo
            self.logo_frame.show()
            self.header_separator.show()

            # Restaurar texto completo en botones
            for key, btn in self.nav_buttons.items():
                full_text = btn.property("fullText")
                btn.setText(full_text)
                btn.setToolTip("")

            # Mostrar elementos del toggle de tema
            self.theme_label.show()
            self.theme_separator_top.show()
            self.theme_separator_bottom.show()

            # Mostrar footer
            self.logout_btn.show()
            self.footer_separator.show()

        # Forzar actualización
        self.updateGeometry()
        self.update()

    def _on_nav_click(self, key, trigger_callback=True):
        """Manejar click en navegación

        Args:
            key: Identificador del botón
            trigger_callback: Si debe ejecutar el callback (False cuando se llama programáticamente)
        """

        # Actualizar estilos de botones
        for btn_key, btn in self.nav_buttons.items():
            if btn_key == key:
                btn.setProperty("class", "active")
                self.active_button = btn
            else:
                btn.setProperty("class", "")

            # Refrescar estilo
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # Ejecutar callback solo si no es llamada programática
        if trigger_callback and key in self.navigation_callbacks:
            self.navigation_callbacks[key]()

        # Emitir señal
        if trigger_callback:
            self.navigation_clicked.emit(key)

    def set_active(self, key):
        """Establecer botón activo programáticamente SIN triggear navegación"""
        self._on_nav_click(key, trigger_callback=False)

    def _on_theme_toggle(self):
        """Manejar cambio de tema"""

        if self.theme_manager:
            # Toggle theme
            new_theme = self.theme_manager.toggle_theme(self.window())

            # Actualizar UI
            self._update_theme()

    def _update_theme(self):
        """Actualizar colores según tema actual"""

        if not self.theme_manager:
            return

        is_dark = self.theme_manager.is_dark_mode()

        # Actualizar label de tema (sin emojis)
        self.theme_label.setText('Modo Oscuro' if is_dark else 'Modo Claro')
        self.theme_btn.setText("DARK" if is_dark else "LIGHT")

        # Los estilos QSS se manejan a nivel de aplicación
        # Pero podemos actualizar colores específicos aquí si es necesario

        # Actualizar stylesheet del sidebar
        sidebar_bg = "#2d2d2d" if is_dark else "#f5f5f5"
        text_color = "#ffffff"
        border_color = "#383838" if is_dark else "#e0e0e0"
        button_bg = "#003087"  # Navy blue para TODOS los botones
        button_text = "#ffffff"  # Texto blanco
        button_hover = "#004ba0"  # Navy más claro para hover
        button_active = "#002060"  # Navy más oscuro para activo

        self.setStyleSheet(f"""
            #modernSidebar {{
                background-color: {sidebar_bg};
                border-right: 1px solid {border_color};
            }}

            #hamburgerBtn {{
                background-color: transparent;
                color: {'#ffffff' if is_dark else '#003087'};
                border: none;
                border-radius: 5px;
            }}

            #hamburgerBtn:hover {{
                background-color: {border_color};
            }}

            #logoFrame QLabel {{
                color: {'#ffffff' if is_dark else '#003087'};
            }}

            #navButton {{
                background-color: {button_bg};
                color: {button_text};
                border: none;
                border-radius: 8px;
                text-align: center;
                padding: 10px;
            }}

            #navButton:hover {{
                background-color: {button_hover};
            }}

            #navButton[class="active"] {{
                background-color: {button_active};
                color: {text_color};
                font-weight: bold;
            }}

            #separator {{
                background-color: {border_color};
            }}

            #toggleFrame QLabel {{
                color: {'#ffffff' if is_dark else '#003087'};
            }}

            #themeToggleBtn {{
                background-color: {button_bg};
                color: {button_text};
                border: none;
                border-radius: 13px;
            }}

            #themeToggleBtn:hover {{
                background-color: {button_hover};
            }}

            #logoutButton {{
                background-color: #d32f2f;
                color: {text_color};
                border: none;
                border-radius: 8px;
            }}

            #logoutButton:hover {{
                background-color: #b71c1c;
            }}
        """)

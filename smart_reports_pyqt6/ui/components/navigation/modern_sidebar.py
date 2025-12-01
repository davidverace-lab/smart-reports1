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

    # Signal emitido cuando se hace click en navegación
    navigation_clicked = pyqtSignal(str)

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
            ('📊', 'Dashboards', 'dashboard'),
            ('🔍', 'Consulta de Empleados', 'consultas'),
            ('📥', 'Importación de Datos', 'importacion'),
            ('📄', 'Generar Reportes', 'reportes'),
            ('⚙️', 'Configuración', 'configuracion'),
        ]

        for icon, text, key in nav_items:
            btn = QPushButton(f"{icon}  {text}")
            btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))
            btn.setFixedHeight(55)
            btn.setObjectName("navButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, k=key: self._on_nav_click(k))

            # Guardar referencia al texto completo
            btn.setProperty("fullText", f"{icon}  {text}")
            btn.setProperty("icon", icon)
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

        # Label con icono
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else True
        self.theme_label = QLabel('🌙 Modo Oscuro' if is_dark else '☀️ Modo Claro')
        self.theme_label.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        toggle_container_layout.addWidget(self.theme_label)

        toggle_container_layout.addStretch()

        # Botón de toggle (simulado como botón)
        self.theme_btn = QPushButton("⚫" if is_dark else "⚪")
        self.theme_btn.setFont(QFont("Arial", 12))
        self.theme_btn.setFixedSize(50, 24)
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
        """Crear footer con información de versión"""

        self.footer_frame = QWidget()
        self.footer_frame.setObjectName("footerFrame")
        footer_layout = QVBoxLayout(self.footer_frame)
        footer_layout.setContentsMargins(10, 10, 10, 0)
        footer_layout.setSpacing(5)

        # Línea separadora superior
        self.footer_separator = QFrame()
        self.footer_separator.setFrameShape(QFrame.Shape.HLine)
        self.footer_separator.setFixedHeight(1)
        self.footer_separator.setObjectName("separator")
        footer_layout.addWidget(self.footer_separator)

        footer_layout.addSpacing(5)

        # Versión
        self.version_label = QLabel("v3.0.0 PyQt6")
        self.version_label.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(self.version_label)

        # Copyright
        self.copyright_label = QLabel("© 2025 INSTITUTO HP")
        self.copyright_label.setFont(QFont("Montserrat", 10))
        self.copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(self.copyright_label)

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

            # Actualizar botones para mostrar solo iconos
            for key, btn in self.nav_buttons.items():
                icon = btn.property("icon")
                btn.setText(icon)
                btn.setToolTip(btn.property("fullText"))

            # Ocultar elementos del toggle de tema
            self.theme_label.hide()
            self.theme_separator_top.hide()
            self.theme_separator_bottom.hide()

            # Ocultar footer
            self.version_label.hide()
            self.copyright_label.hide()
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
            self.version_label.show()
            self.copyright_label.show()
            self.footer_separator.show()

        # Forzar actualización
        self.updateGeometry()
        self.update()

    def _on_nav_click(self, key):
        """Manejar click en navegación"""

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

        # Ejecutar callback
        if key in self.navigation_callbacks:
            self.navigation_callbacks[key]()

        # Emitir señal
        self.navigation_clicked.emit(key)

    def set_active(self, key):
        """Establecer botón activo programáticamente"""
        self._on_nav_click(key)

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

        # Actualizar label de tema
        self.theme_label.setText('🌙 Modo Oscuro' if is_dark else '☀️ Modo Claro')
        self.theme_btn.setText("⚫" if is_dark else "⚪")

        # Los estilos QSS se manejan a nivel de aplicación
        # Pero podemos actualizar colores específicos aquí si es necesario

        # Actualizar stylesheet del sidebar
        sidebar_bg = "#2d2d2d" if is_dark else "#003087"
        text_color = "#ffffff"
        text_secondary = "#E0E0E0" if not is_dark else "#888888"
        border_color = "#4a5a8a" if not is_dark else "#383838"
        hover_color = "#4a5a8a" if not is_dark else "#2b2b2b"
        active_bg = "#4a5a8a" if not is_dark else "#2b2b2b"

        self.setStyleSheet(f"""
            #modernSidebar {{
                background-color: {sidebar_bg};
                border-right: 1px solid {border_color};
            }}

            #hamburgerBtn {{
                background-color: transparent;
                color: {text_color};
                border: none;
                border-radius: 5px;
            }}

            #hamburgerBtn:hover {{
                background-color: {hover_color};
            }}

            #logoFrame QLabel {{
                color: {text_color};
            }}

            #navButton {{
                background-color: transparent;
                color: {text_secondary};
                border: none;
                border-radius: 10px;
                text-align: left;
                padding-left: 15px;
            }}

            #navButton:hover {{
                background-color: {hover_color};
            }}

            #navButton[class="active"] {{
                background-color: {active_bg};
                color: {text_color};
            }}

            #separator {{
                background-color: {border_color};
            }}

            #toggleFrame QLabel {{
                color: {text_color if not is_dark else text_secondary};
            }}

            #themeToggleBtn {{
                background-color: {hover_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 12px;
            }}

            #themeToggleBtn:hover {{
                background-color: {active_bg};
            }}

            #footerFrame QLabel {{
                color: {text_secondary};
            }}
        """)

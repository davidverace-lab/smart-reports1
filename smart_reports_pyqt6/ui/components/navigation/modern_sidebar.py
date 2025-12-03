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
        self.expanded_width = 280  # Más ancho - de 240 a 280
        self.collapsed_width = 75

        # Configurar sidebar
        self.setFixedWidth(self.expanded_width)
        self.setObjectName("modernSidebar")

        # Crear UI
        self._create_ui()

        # Aplicar tema inicial
        self._update_theme()

        # Conectar signal de cambio de tema
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(lambda new_theme: self._update_theme())

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

        # Botón hamburguesa - MÁS GRANDE
        self.collapse_btn = QPushButton("☰")
        self.collapse_btn.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        self.collapse_btn.setFixedSize(55, 45)
        self.collapse_btn.setObjectName("hamburgerBtn")
        self.collapse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.collapse_btn.clicked.connect(self._toggle_collapse)
        header_layout.addWidget(self.collapse_btn, alignment=Qt.AlignmentFlag.AlignTop)

        # Frame del logo (colapsable) - MÁS ALTO
        self.logo_frame = QWidget()
        self.logo_frame.setObjectName("logoFrame")
        self.logo_frame.setFixedHeight(110)
        logo_layout = QVBoxLayout(self.logo_frame)
        logo_layout.setContentsMargins(10, 15, 10, 10)
        logo_layout.setSpacing(5)

        # Título principal - MÁS GRANDE (30pt)
        self.logo_label = QLabel("SMART\nREPORTS")
        self.logo_label.setFont(QFont("Montserrat", 30, QFont.Weight.Bold))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setWordWrap(True)
        logo_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Subtítulo - MÁS GRANDE (12pt)
        self.subtitle = QLabel("Instituto Hutchison Ports")
        self.subtitle.setFont(QFont("Montserrat", 12))
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setWordWrap(True)
        logo_layout.addWidget(self.subtitle, alignment=Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(self.logo_frame)

        # Línea separadora
        self.header_separator = QFrame()
        self.header_separator.setFrameShape(QFrame.Shape.HLine)
        self.header_separator.setFixedHeight(1)
        self.header_separator.setObjectName("separator")
        header_layout.addWidget(self.header_separator)

        self.main_layout.addWidget(header_container)

    def _create_navigation(self):
        """Crear botones de navegación con iconos - MÁS GRANDES"""

        nav_items = [
            ('▣  Dashboards', 'dashboard', '▣'),
            ('⚲  Consulta de Empleados', 'consultas', '⚲'),
            ('⬇  Importación de Datos', 'importacion', '⬇'),
            ('☰  Generar Reportes', 'reportes', '☰'),
            ('⚙  Configuración', 'configuracion', '⚙'),
        ]

        for text, key, icon in nav_items:
            btn = QPushButton(text)
            btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))  # Aumentado de 13 a 15
            btn.setFixedHeight(55)  # Aumentado de 50 a 55
            btn.setObjectName("navButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, k=key: self._on_nav_click(k))

            # Guardar referencia al texto completo e icono
            btn.setProperty("fullText", text)
            btn.setProperty("iconOnly", icon)
            btn.setProperty("navKey", key)

            self.nav_buttons[key] = btn
            self.main_layout.addWidget(btn)

    def _create_theme_toggle(self):
        """Crear toggle para modo claro/oscuro con switch animado"""

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
        toggle_container_layout.setContentsMargins(10, 5, 10, 5)
        toggle_container_layout.setSpacing(10)

        # Label con texto dinámico e icono - MÁS GRANDE (símbolos simples)
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else True
        mode_icon = "☾  " if is_dark else "☀  "
        mode_text = mode_icon + ("Modo Oscuro" if is_dark else "Modo Claro")
        self.theme_label = QLabel(mode_text)
        self.theme_label.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))  # Aumentado de 11 a 15
        toggle_container_layout.addWidget(self.theme_label)

        toggle_container_layout.addStretch()

        # Botón de toggle estilo iOS switch animado - MÁS GRANDE
        self.theme_btn = QPushButton()
        self.theme_btn.setFixedSize(65, 32)
        self.theme_btn.setObjectName("themeToggleSwitch")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self._on_theme_toggle)
        self.theme_btn.setProperty("isDark", is_dark)
        self.theme_btn.setCheckable(True)
        self.theme_btn.setChecked(is_dark)
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
        """Crear footer con información de versión - BASADO EN CUSTOMTKINTER"""

        self.footer_frame = QWidget()
        self.footer_frame.setObjectName("footerFrame")
        footer_layout = QVBoxLayout(self.footer_frame)
        footer_layout.setContentsMargins(20, 20, 20, 20)
        footer_layout.setSpacing(10)

        # Línea separadora superior
        self.footer_separator = QFrame()
        self.footer_separator.setFrameShape(QFrame.Shape.HLine)
        self.footer_separator.setFixedHeight(1)
        self.footer_separator.setObjectName("separator")
        footer_layout.addWidget(self.footer_separator)

        # Versión - MÁS GRANDE (12pt)
        self.version_label = QLabel("v2.0.0")
        self.version_label.setFont(QFont("Montserrat", 12, QFont.Weight.Bold))
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version_label.setObjectName("versionLabel")
        footer_layout.addWidget(self.version_label)

        # Copyright - MÁS GRANDE (11pt)
        self.copyright_label = QLabel("© 2025 INSTITUTO HP")
        self.copyright_label.setFont(QFont("Montserrat", 11))
        self.copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyright_label.setObjectName("copyrightLabel")
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
                icon_only = btn.property("iconOnly")
                btn.setText(icon_only)
                btn.setToolTip(btn.property("fullText"))
                btn.setFont(QFont("Arial", 24))  # Hacer iconos más grandes

            # Mostrar solo icono del toggle de tema
            self.theme_label.hide()
            self.theme_btn.setFixedSize(50, 50)  # Hacer el botón más grande y cuadrado
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
                btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))  # Restaurar fuente correcta

            # Mostrar elementos del toggle de tema
            self.theme_label.show()
            self.theme_btn.setFixedSize(50, 28)  # Restaurar tamaño normal
            self.theme_separator_top.show()
            self.theme_separator_bottom.show()

            # Mostrar footer
            self.version_label.show()
            self.copyright_label.show()
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

        # Actualizar label de tema con texto dinámico e icono (símbolos simples)
        mode_icon = "☾  " if is_dark else "☀  "
        mode_text = mode_icon + ("Modo Oscuro" if is_dark else "Modo Claro")
        self.theme_label.setText(mode_text)
        self.theme_btn.setChecked(is_dark)
        self.theme_btn.setProperty("isDark", is_dark)

        # ====== COLORES BASADOS EN CUSTOMTKINTER ======
        # Modo claro: Fondo azul navy (#002E6D), texto blanco, botones sin color (solo hover)
        # Modo oscuro: Fondo gris oscuro (#2d2d2d), texto blanco también

        sidebar_bg = "#2d2d2d" if is_dark else "#002E6D"  # Navy corporativo en modo claro!
        text_color = "#FFFFFF"  # Blanco en ambos modos
        text_secondary = "#E0E0E0" if not is_dark else "#A0A0A0"
        border_color = "#383838" if is_dark else "#4a5a8a"  # Tonalidad navy más clara
        hover_color = "#383838" if is_dark else "#003D82"  # Navy más claro para hover
        active_bg = "#383838" if is_dark else "#004C97"  # Navy más claro para activo

        self.setStyleSheet(f"""
            #modernSidebar {{
                background-color: {sidebar_bg} !important;
                border-right: 2px solid {border_color};
            }}

            #hamburgerBtn {{
                background-color: transparent !important;
                color: {text_color} !important;
                border: none;
                border-radius: 8px;
            }}

            #hamburgerBtn:hover {{
                background-color: {hover_color} !important;
            }}

            #logoFrame QLabel {{
                color: {text_color} !important;
                background: transparent !important;
            }}

            #navButton {{
                background-color: transparent !important;
                color: {text_color} !important;
                border: none;
                border-radius: 10px;
                text-align: left;
                padding: 12px 18px;
            }}

            #navButton:hover {{
                background-color: {hover_color} !important;
                color: {text_color} !important;
            }}

            #navButton[class="active"] {{
                background-color: {active_bg} !important;
                color: {text_color} !important;
                font-weight: bold;
            }}

            #separator {{
                background-color: {border_color} !important;
            }}

            #toggleFrame {{
                background-color: transparent !important;
            }}

            #toggleFrame QLabel {{
                color: {text_color} !important;
                background: transparent !important;
            }}

            #themeToggleSwitch {{
                background-color: {'#5a6a90' if not is_dark else '#404040'} !important;
                border: none;
                border-radius: 15px;
                text-align: left;
                padding: 3px;
            }}

            #themeToggleSwitch:checked {{
                background-color: {'#003D82' if not is_dark else '#002E6D'} !important;
            }}

            #themeToggleSwitch:!checked {{
                background-color: {'#6a7aa0' if not is_dark else '#505050'} !important;
            }}

            #themeToggleSwitch:hover {{
                background-color: {'#4a5a80' if not is_dark else '#505050'} !important;
            }}

            #themeToggleSwitch:checked:hover {{
                background-color: {'#003570' if not is_dark else '#002a60'} !important;
            }}

            #headerContainer, #footerFrame {{
                background-color: transparent !important;
            }}

            #versionLabel {{
                color: {text_secondary} !important;
                background: transparent !important;
            }}

            #copyrightLabel {{
                color: {text_secondary} !important;
                background: transparent !important;
            }}
        """)

        # Forzar actualización visual de todos los widgets
        self.update()
        self.repaint()

        # Forzar actualización de los botones de navegación
        for btn in self.nav_buttons.values():
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

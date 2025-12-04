import sys
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QPoint, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QBrush

# ===================================================================
# 1. SWITCH ANIMADO ROBUSTO
# ===================================================================
class AnimatedToggle(QCheckBox):
    def __init__(self, width=60, height=32, parent=None):
        super().__init__(parent)
        self._w = width
        self._h = height
        self.setFixedSize(self._w, self._h)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Colores
        self.bar_color = QColor("#777")
        self.circle_color = QColor("#FFF")
        self.active_color = QColor("#002E6D")

        # Animación
        self._circle_x = 3
        self.animation = QPropertyAnimation(self, b"circle_x", self)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setDuration(300)

        self.stateChanged.connect(self.start_transition)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @pyqtProperty(float)
    def circle_x(self):
        return self._circle_x

    @circle_x.setter
    def circle_x(self, pos):
        self._circle_x = pos
        self.update()

    def start_transition(self, state):
        self.animation.stop()
        padding = 3
        if state: # ON (Derecha)
            target = self.width() - self.height() + padding
        else:     # OFF (Izquierda)
            target = padding
        self.animation.setEndValue(target)
        self.animation.start()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)

        if self.isChecked():
            p.setBrush(self.active_color)
        else:
            p.setBrush(self.bar_color)
        p.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)

        p.setBrush(self.circle_color)
        padding = 3
        radius = int((self.height() - (padding * 2)) / 2)
        center_y = int(self.height() / 2)
        center_x = int(self._circle_x + radius)

        if center_x > self.width() - radius:
            center_x = self.width() - radius - padding

        p.drawEllipse(QPoint(center_x, center_y), radius, radius)
        p.end()

    def resize_animated(self, w, h):
        self.setFixedSize(w, h)
        if self.isChecked():
            self._circle_x = w - h + 3
        else:
            self._circle_x = 3
        self.update()


# ===================================================================
# 2. BARRA LATERAL (ModernSidebar) - CORREGIDA (FIX CRASH)
# ===================================================================
class ModernSidebar(QFrame):

    navigation_clicked = pyqtSignal(str)
    logout_clicked = pyqtSignal()

    def __init__(self, parent=None, navigation_callbacks=None, theme_manager=None):
        super().__init__(parent)
        self.navigation_callbacks = navigation_callbacks or {}
        self.theme_manager = theme_manager
        self.nav_buttons = {}

        self.is_collapsed = False
        self.expanded_width = 300
        self.collapsed_width = 90

        self.setFixedWidth(self.expanded_width)
        self.setObjectName("modernSidebar")

        self._create_ui()
        self._update_theme()

        if self.theme_manager:
            self.theme_manager.theme_changed.connect(lambda: self._update_theme())

    def _create_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 20, 10, 20)
        self.main_layout.setSpacing(15)

        self._create_header()
        self._create_navigation()
        self.main_layout.addStretch()
        self._create_theme_toggle()
        self._create_footer()

    def _create_header(self):
        container = QWidget()
        container.setObjectName("headerContainer")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(5)

        # Botón Hamburguesa
        self.collapse_btn = QPushButton("☰")
        self.collapse_btn.setStyleSheet("""
            font-family: 'Montserrat';
            font-size: 32px;
            font-weight: bold;
            border: none;
            background: transparent;
        """)
        self.collapse_btn.setFixedSize(60, 50)
        self.collapse_btn.setObjectName("hamburgerBtn")
        self.collapse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.collapse_btn.clicked.connect(self._toggle_collapse)
        layout.addWidget(self.collapse_btn, alignment=Qt.AlignmentFlag.AlignTop)

        # Logo Frame (AUMENTADO DE 120 A 160 PARA QUE QUEPA EL TEXTO)
        self.logo_frame = QWidget()
        self.logo_frame.setObjectName("logoFrame")
        self.logo_frame.setFixedHeight(160)
        logo_layout = QVBoxLayout(self.logo_frame)
        logo_layout.setContentsMargins(0,10,0,0)

        # --- TEXTO GIGANTE CON STYLESHEET EN LUGAR DE SETFONT ---
        self.logo_label = QLabel("SMART\nREPORTS")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setStyleSheet("""
            font-family: 'Montserrat';
            font-size: 32px;
            font-weight: bold;
            border: none;
            background: transparent;
        """)
        logo_layout.addWidget(self.logo_label)

        # Subtítulo
        self.subtitle = QLabel("Instituto Hutchison Ports")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setWordWrap(True)
        self.subtitle.setStyleSheet("""
            font-family: 'Montserrat';
            font-size: 12px;
            font-weight: normal;
            border: none;
            background: transparent;
        """)
        logo_layout.addWidget(self.subtitle)

        layout.addWidget(self.logo_frame)

        # Separador
        self.header_separator = QFrame()
        self.header_separator.setFrameShape(QFrame.Shape.HLine)
        self.header_separator.setFixedHeight(2)
        self.header_separator.setObjectName("separator")
        layout.addWidget(self.header_separator)

        self.main_layout.addWidget(container)

    def _create_navigation(self):
        # Aseguramos que TODAS las claves coincidan con MainWindow
        items = [
            ('📊  Dashboards', 'dashboard', '📊'),
            ('🔍  Consulta de Empleados', 'consultas', '🔍'),
            ('📥  Importación de Datos', 'importacion', '📥'),
            ('📄  Generar Reportes', 'reportes', '📄'),
            ('⚙️  Configuración', 'configuracion', '⚙️'),
        ]

        for text, key, icon in items:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                font-family: 'Montserrat';
                font-size: 18px;
                font-weight: bold;
                text-align: left;
                padding-left: 20px;
                border: none;
                background: transparent;
            """)
            btn.setFixedHeight(60)
            btn.setObjectName("navButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            # FIX 1: Pasamos el evento normalmente
            btn.clicked.connect(lambda ch, k=key: self._on_nav_click(k))

            btn.setProperty("fullText", text)
            btn.setProperty("iconOnly", icon)

            self.nav_buttons[key] = btn
            self.main_layout.addWidget(btn)

    def _create_theme_toggle(self):
        self.toggle_frame = QWidget()
        self.toggle_frame.setObjectName("toggleFrame")
        v_layout = QVBoxLayout(self.toggle_frame)
        v_layout.setContentsMargins(0, 5, 0, 5)

        self.sep_top = QFrame()
        self.sep_top.setFrameShape(QFrame.Shape.HLine)
        self.sep_top.setFixedHeight(1)
        self.sep_top.setObjectName("separator")
        v_layout.addWidget(self.sep_top)

        self.toggle_container_h = QWidget()
        self.h_layout = QHBoxLayout(self.toggle_container_h)
        self.h_layout.setContentsMargins(5, 5, 5, 5)

        self.theme_label = QLabel("Modo")
        self.theme_label.setStyleSheet("""
            font-family: 'Montserrat';
            font-size: 16px;
            font-weight: bold;
            border: none;
            background: transparent;
        """)
        self.h_layout.addWidget(self.theme_label)

        self.h_layout.addStretch()

        self.theme_switch = AnimatedToggle(width=60, height=32)
        self.theme_switch.clicked.connect(self._on_theme_toggle)
        self.h_layout.addWidget(self.theme_switch)

        v_layout.addWidget(self.toggle_container_h)

        self.sep_bot = QFrame()
        self.sep_bot.setFrameShape(QFrame.Shape.HLine)
        self.sep_bot.setFixedHeight(1)
        self.sep_bot.setObjectName("separator")
        v_layout.addWidget(self.sep_bot)

        self.main_layout.addWidget(self.toggle_frame)

    def _create_footer(self):
        self.footer_frame = QWidget()
        self.footer_frame.setObjectName("footerFrame")
        layout = QVBoxLayout(self.footer_frame)
        layout.setSpacing(5)

        self.version_label = QLabel("v2.0.0")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version_label.setObjectName("versionLabel")
        self.version_label.setStyleSheet("""
            font-family: 'Montserrat';
            font-size: 12px;
            font-weight: bold;
            border: none;
            background: transparent;
        """)
        layout.addWidget(self.version_label)

        self.copyright_label = QLabel("© 2025 INSTITUTO HP")
        self.copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyright_label.setObjectName("copyrightLabel")
        self.copyright_label.setStyleSheet("""
            font-family: 'Montserrat';
            font-size: 11px;
            font-weight: normal;
            border: none;
            background: transparent;
        """)
        layout.addWidget(self.copyright_label)

        self.main_layout.addWidget(self.footer_frame)

    def _toggle_collapse(self):
        self.is_collapsed = not self.is_collapsed

        if self.is_collapsed:
            self.setFixedWidth(self.collapsed_width)
            self.logo_frame.hide()
            self.header_separator.hide()
            self.theme_label.hide()
            self.footer_frame.hide()
            self.sep_top.hide()
            self.sep_bot.hide()

            for btn in self.nav_buttons.values():
                btn.setText(btn.property("iconOnly"))
                btn.setStyleSheet("""
                    font-family: 'Segoe UI Emoji';
                    font-size: 26px;
                    font-weight: normal;
                    text-align: center;
                    padding: 0px;
                    border: none;
                    background: transparent;
                """)
                btn.setToolTip(btn.property("fullText"))

            self.h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.h_layout.setContentsMargins(0, 5, 0, 5)
            self.theme_switch.resize_animated(40, 24)

        else:
            self.setFixedWidth(self.expanded_width)
            self.logo_frame.show()
            self.header_separator.show()
            self.theme_label.show()
            self.footer_frame.show()
            self.sep_top.show()
            self.sep_bot.show()

            for btn in self.nav_buttons.values():
                btn.setText(btn.property("fullText"))
                btn.setStyleSheet("""
                    font-family: 'Montserrat';
                    font-size: 18px;
                    font-weight: bold;
                    text-align: left;
                    padding-left: 20px;
                    border: none;
                    background: transparent;
                """)
                btn.setToolTip("")

            self.h_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.h_layout.setContentsMargins(5, 5, 5, 5)
            self.theme_switch.resize_animated(60, 32)

        # Forzar actualización de tema después de colapsar/expandir
        self._update_theme()

    # ==========================================================
    # FIX PRINCIPAL: Evitar bucle infinito y agregar set_active
    # ==========================================================

    def _on_nav_click(self, key, trigger_callback=True):
        """
        Maneja el clic en un botón.
        Args:
            key: ID del botón
            trigger_callback: Si es True, avisa a MainWindow. Si es False, solo actualiza visualmente.
        """
        # 1. Actualizar visualmente (poner clase 'active' al botón correcto)
        for k, btn in self.nav_buttons.items():
            btn.setProperty("class", "active" if k == key else "")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # 2. Solo ejecutar callbacks si trigger_callback es True
        # Esto previene el bucle infinito cuando MainWindow llama de vuelta a set_active
        if trigger_callback:
            if key in self.navigation_callbacks:
                self.navigation_callbacks[key]() # <--- Esto causaba el crash si se llamaba recursivamente
            self.navigation_clicked.emit(key)

    def set_active(self, key):
        """
        Método público llamado por MainWindow para marcar un botón como activo.
        IMPORTANTE: Llama a _on_nav_click con trigger_callback=False
        """
        if key in self.nav_buttons:
            self._on_nav_click(key, trigger_callback=False)

    def _on_theme_toggle(self):
        if self.theme_manager:
            self.theme_manager.toggle_theme(self.window())
            self._update_theme()

    def _update_theme(self):
        if not self.theme_manager: return
        is_dark = self.theme_manager.is_dark_mode()

        icon = "☾ " if is_dark else "☀ "
        text = "Modo Oscuro" if is_dark else "Modo Claro"
        self.theme_label.setText(f"{icon} {text}")

        self.theme_switch.blockSignals(True)
        self.theme_switch.setChecked(is_dark)
        self.theme_switch.blockSignals(False)

        bg = "#2d2d2d" if is_dark else "#002E6D"
        text_c = "#FFFFFF"
        sec_c = "#A0A0A0" if is_dark else "#E0E0E0"
        border_c = "#383838" if is_dark else "#4a5a8a"
        hover_c = "#383838" if is_dark else "#003D82"
        active_c = "#404040" if is_dark else "#004C97"

        self.theme_switch.active_color = QColor("#004C97") if not is_dark else QColor("#002E6D")
        self.theme_switch.bar_color = QColor("#6a7aa0") if not is_dark else QColor("#505050")
        self.theme_switch.update()

        self.setStyleSheet(f"""
            #modernSidebar {{
                background-color: {bg} !important;
                border-right: 1px solid {border_c};
            }}
            QWidget {{
                background: transparent !important;
                border: none !important;
            }}
            QLabel {{
                color: {text_c};
                border: none !important;
                background: transparent !important;
            }}
            QPushButton {{
                color: {text_c};
                border: none !important;
                background: transparent !important;
            }}

            #copyrightLabel, #versionLabel {{
                color: {sec_c};
                border: none !important;
                background: transparent !important;
            }}

            #separator {{
                background-color: {border_c};
                max-height: 2px;
                border: none !important;
            }}

            #navButton {{
                border-radius: 10px;
                border: none !important;
            }}
            #navButton:hover {{
                background-color: {hover_c} !important;
            }}

            #navButton[class="active"] {{
                background-color: {active_c} !important;
                font-weight: bold;
                border-left: 5px solid #FFFFFF !important;
            }}

            #hamburgerBtn:hover {{
                background-color: {hover_c} !important;
                border-radius: 5px;
            }}

            #logoFrame QLabel, #toggleFrame QLabel, #footerFrame QLabel {{
                border: none !important;
                background: transparent !important;
            }}
        """)

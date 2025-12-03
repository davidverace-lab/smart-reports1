"""
Barra Superior - PyQt6
Basado en el diseño de CustomTkinter
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class BarraSuperior(QFrame):
    """Barra superior con bienvenida al usuario y branding Hutchison Ports"""

    def __init__(self, username="Usuario", user_role="Administrador", theme_manager=None, parent=None):
        """
        Args:
            parent: Widget padre
            username: Nombre del usuario autenticado
            user_role: Rol del usuario (Administrador, Operador, etc.)
            theme_manager: Gestor de temas
        """
        super().__init__(parent)

        self.username = username
        self.user_role = user_role
        self.theme_manager = theme_manager

        self.setObjectName("barraSuperior")
        self.setFixedHeight(80)  # Igual que CustomTkinter

        self._create_ui()

        # Conectar signal de cambio de tema
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(lambda new_theme: self._update_theme())

        # Aplicar tema inicial
        self._update_theme()

    def _create_ui(self):
        """Crear interfaz de la barra superior - SIMPLE Y LIMPIA"""

        # Layout principal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 0, 30, 0)
        layout.setSpacing(20)

        # === LADO IZQUIERDO: Bienvenida ===
        self.greeting_label = QLabel(f"¡Bienvenido, {self.username}!")
        self.greeting_label.setObjectName("greetingLabel")
        # Usar setStyleSheet para la fuente en lugar de setFont
        self.greeting_label.setStyleSheet("""
            font-family: 'Montserrat';
            font-size: 18px;
            font-weight: bold;
            border: none;
            background: transparent;
        """)
        layout.addWidget(self.greeting_label, alignment=Qt.AlignmentFlag.AlignVCenter)

        # Spacer para empujar a los lados
        layout.addStretch()

        # === LADO DERECHO: Branding ===
        self.brand_label = QLabel("HUTCHISON PORTS")
        self.brand_label.setObjectName("brandLabel")
        # Usar setStyleSheet para la fuente en lugar de setFont
        self.brand_label.setStyleSheet("""
            font-family: 'Montserrat';
            font-size: 22px;
            font-weight: bold;
            border: none;
            background: transparent;
        """)
        layout.addWidget(self.brand_label, alignment=Qt.AlignmentFlag.AlignVCenter)

    def set_title(self, title):
        """Establecer título de la sección actual (no usado en este diseño)"""
        pass

    def update_user(self, username, user_role):
        """
        Actualizar información del usuario

        Args:
            username: Nuevo nombre de usuario
            user_role: Nuevo rol
        """
        self.username = username
        self.user_role = user_role
        self.greeting_label.setText(f"¡Bienvenido, {username}!")

    def _update_theme(self):
        """Actualizar colores según tema actual - BASADO EN CUSTOMTKINTER"""

        if not self.theme_manager:
            return

        is_dark = self.theme_manager.is_dark_mode()

        # Colores basados en CustomTkinter
        # Modo claro: Card background, texto oscuro, branding navy
        # Modo oscuro: Card background oscuro, texto blanco, branding blanco

        bg_color = "#2d2d2d" if is_dark else "#f5f5f5"  # Card background
        text_color = "#ffffff" if is_dark else "#333333"  # Texto normal
        brand_color = "#ffffff" if is_dark else "#002E6D"  # Branding: blanco en oscuro, navy en claro
        border_color = "#383838" if is_dark else "#002E6D"  # Borde: gris en oscuro, navy corporativo en claro

        # Actualizar estilos del frame principal y labels
        self.setStyleSheet(f"""
            #barraSuperior {{
                background-color: {bg_color} !important;
                border: none !important;
                border-bottom: 2px solid {border_color} !important;
            }}
            QWidget {{
                background: transparent !important;
                border: none !important;
            }}
            QLabel {{
                border: none !important;
                background: transparent !important;
            }}
        """)

        # Actualizar colores de los labels manteniendo las fuentes definidas
        self.greeting_label.setStyleSheet(f"""
            font-family: 'Montserrat';
            font-size: 18px;
            font-weight: bold;
            color: {text_color};
            border: none;
            background: transparent;
        """)

        self.brand_label.setStyleSheet(f"""
            font-family: 'Montserrat';
            font-size: 22px;
            font-weight: bold;
            color: {brand_color};
            border: none;
            background: transparent;
        """)

        # Forzar actualización visual
        self.update()
        self.repaint()

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
        self.setFixedHeight(70)  # Reducido de 100 a 70
        # Borde inferior Navy
        self.setStyleSheet("border-bottom: 2px solid #002E6D;")

        self._create_ui()

        # Conectar signal de cambio de tema
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(self._on_theme_changed)

        # Aplicar tema inicial
        self._on_theme_changed(self.theme_manager.current_theme if self.theme_manager else 'dark')

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
            font-size: 20px;
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

    def _on_theme_changed(self, new_theme: str):
        """Actualizar colores según tema actual"""
        is_dark = (new_theme == 'dark')

        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        text_color = "#ffffff" if is_dark else "#002E6D"
        brand_color = "#ffffff" if is_dark else "#002E6D"
        border_color = "#002E6D"  # Navy corporativo siempre

        # Actualizar estilo del frame
        self.setStyleSheet(f"""
            #barraSuperior {{
                background-color: {bg_color};
                border-bottom: 3px solid {border_color};
            }}
        """)

        # Actualizar labels
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
            font-size: 20px;
            font-weight: bold;
            color: {brand_color};
            border: none;
            background: transparent;
        """)

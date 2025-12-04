"""
Widget de contenedor personalizado tipo GitHub Actions
Diseño con esquinas redondeadas, borde sutil y layout específico
Soporte completo para temas claro/oscuro con iconos que cambian de color
"""

from PyQt6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor
from PyQt6.QtSvgWidgets import QSvgWidget
from io import BytesIO


class IconWidget(QLabel):
    """Widget para mostrar iconos SVG que cambian de color según el tema"""

    def __init__(self, icon_name: str = "report", parent=None):
        super().__init__(parent)
        self.icon_name = icon_name
        self.current_color = "#FFFFFF"
        self._icon_size = 32

        self.setFixedSize(self._icon_size, self._icon_size)
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_color(self, color: str):
        """Cambiar el color del icono"""
        self.current_color = color
        self._render_icon()

    def _render_icon(self):
        """Renderizar el icono con el color actual"""
        svg_content = self._get_svg_content()

        # Crear QPixmap desde SVG
        from PyQt6.QtSvg import QSvgRenderer
        renderer = QSvgRenderer(svg_content.encode('utf-8'))

        pixmap = QPixmap(self._icon_size, self._icon_size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()

        self.setPixmap(pixmap)

    def _get_svg_content(self) -> str:
        """Obtener el contenido SVG del icono según el nombre"""

        # Icono de reporte (documento con gráfico de barras)
        if self.icon_name == "report":
            return f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{self.current_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="8" y1="13" x2="8" y2="17"/>
                <line x1="12" y1="11" x2="12" y2="17"/>
                <line x1="16" y1="15" x2="16" y2="17"/>
            </svg>
            '''

        # Icono de documento PDF
        elif self.icon_name == "pdf":
            return f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{self.current_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <text x="7" y="16" font-size="5" fill="{self.current_color}" font-weight="bold">PDF</text>
            </svg>
            '''

        # Icono de impresora
        elif self.icon_name == "printer":
            return f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{self.current_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 6 2 18 2 18 9"/>
                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
                <rect x="6" y="14" width="12" height="8"/>
            </svg>
            '''

        # Icono de análisis/gráfico
        elif self.icon_name == "analytics":
            return f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{self.current_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"/>
                <line x1="12" y1="20" x2="12" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="14"/>
            </svg>
            '''

        # Icono de calendario
        elif self.icon_name == "calendar":
            return f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{self.current_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            '''

        # Icono por defecto (documento)
        else:
            return f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{self.current_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
            </svg>
            '''


class ReportCardGitHub(QFrame):
    """
    Widget de contenedor personalizado estilo GitHub Actions
    Réplica exacta del diseño de las tarjetas de selección de GitHub Actions

    Características:
    - Esquinas redondeadas (8px)
    - Borde delgado y sutil
    - Layout de 3 filas:
      * Superior: Título (izquierda) + Icono circular (derecha)
      * Central: Descripción
      * Inferior: Botón (izquierda) + Etiqueta formato (derecha)
    - Soporte temas claro/oscuro
    - Icono que cambia de color automáticamente
    """

    # Señales
    action_clicked = pyqtSignal()

    def __init__(
        self,
        title: str = "Reporte de Ventas Mensual",
        description: str = "Genera un PDF detallado con gráficos de rendimiento.",
        button_text: str = "Generar",
        format_label: str = "Formato: PDF",
        icon_name: str = "report",
        theme: str = "dark",
        parent=None
    ):
        super().__init__(parent)

        self.title_text = title
        self.description_text = description
        self.button_text = button_text
        self.format_text = format_label
        self.icon_name = icon_name
        self.current_theme = theme

        # Configurar frame
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Tamaño recomendado
        self.setMinimumWidth(320)
        self.setMinimumHeight(180)
        self.setMaximumWidth(400)

        # Política de tamaño
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Crear UI
        self._create_ui()

        # Aplicar tema inicial
        self.set_theme(theme)

    def _create_ui(self):
        """Crear la interfaz del widget"""

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(12)

        # === FILA SUPERIOR: Título + Icono ===
        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        # Título (negrita, izquierda)
        self.title_label = QLabel(self.title_text)
        self.title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.title_label.setWordWrap(True)
        self.title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        top_row.addWidget(self.title_label)

        # Icono circular (derecha)
        icon_container = QFrame()
        icon_container.setFixedSize(40, 40)
        icon_container.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: 2px solid rgba(128, 128, 128, 0.3);
                border-radius: 20px;
            }
        """)

        icon_layout = QHBoxLayout(icon_container)
        icon_layout.setContentsMargins(4, 4, 4, 4)

        self.icon_widget = IconWidget(self.icon_name)
        icon_layout.addWidget(self.icon_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        top_row.addWidget(icon_container)

        main_layout.addLayout(top_row)

        # === FILA CENTRAL: Descripción ===
        self.description_label = QLabel(self.description_text)
        self.description_label.setFont(QFont("Segoe UI", 10))
        self.description_label.setWordWrap(True)
        self.description_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        main_layout.addWidget(self.description_label)

        # Espaciador flexible
        main_layout.addStretch()

        # === FILA INFERIOR: Botón + Etiqueta ===
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(10)

        # Botón de acción (izquierda)
        self.action_button = QPushButton(self.button_text)
        self.action_button.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.action_button.setFixedHeight(32)
        self.action_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.action_button.clicked.connect(self.action_clicked.emit)
        bottom_row.addWidget(self.action_button)

        # Espaciador
        bottom_row.addStretch()

        # Punto indicador + Etiqueta de formato (derecha)
        format_container = QHBoxLayout()
        format_container.setSpacing(6)

        # Punto indicador
        self.indicator_dot = QLabel("●")
        self.indicator_dot.setFont(QFont("Segoe UI", 8))
        format_container.addWidget(self.indicator_dot)

        # Etiqueta de formato
        self.format_label = QLabel(self.format_text)
        self.format_label.setFont(QFont("Segoe UI", 9))
        format_container.addWidget(self.format_label)

        bottom_row.addLayout(format_container)

        main_layout.addLayout(bottom_row)

    def set_theme(self, theme: str):
        """
        Cambiar el tema del widget

        Args:
            theme: "dark" o "light"
        """
        self.current_theme = theme
        is_dark = (theme == "dark")

        # Colores según especificación del usuario
        if is_dark:
            # MODO OSCURO
            bg_color = "#21262d"
            border_color = "#30363d"
            title_color = "#ffffff"
            desc_color = "#8b949e"
            icon_color = "#FFFFFF"  # BLANCO PURO
            button_bg = "#238636"
            button_hover = "#2ea043"
            button_text = "#ffffff"
            format_color = "#8b949e"
            dot_color = "#3fb950"  # Verde como GitHub
        else:
            # MODO CLARO
            bg_color = "#ffffff"
            border_color = "#d0d7de"
            title_color = "#002E6D"  # AZUL NAVY
            desc_color = "#57606a"
            icon_color = "#002E6D"  # AZUL NAVY
            button_bg = "#2da44e"
            button_hover = "#2c974b"
            button_text = "#ffffff"
            format_color = "#57606a"
            dot_color = "#2da44e"

        # Aplicar estilos al frame principal
        self.setStyleSheet(f"""
            ReportCardGitHub {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
            }}
            ReportCardGitHub:hover {{
                border: 1px solid {title_color};
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
            }}
        """)

        # Aplicar colores a los labels
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {title_color};
                background: transparent;
                border: none;
            }}
        """)

        self.description_label.setStyleSheet(f"""
            QLabel {{
                color: {desc_color};
                background: transparent;
                border: none;
            }}
        """)

        self.format_label.setStyleSheet(f"""
            QLabel {{
                color: {format_color};
                background: transparent;
                border: none;
            }}
        """)

        self.indicator_dot.setStyleSheet(f"""
            QLabel {{
                color: {dot_color};
                background: transparent;
                border: none;
            }}
        """)

        # Aplicar estilo al botón
        self.action_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {button_bg};
                color: {button_text};
                border: 1px solid {button_bg};
                border-radius: 6px;
                padding: 5px 16px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {button_hover};
                border-color: {button_hover};
            }}
            QPushButton:pressed {{
                background-color: {button_bg};
                transform: scale(0.98);
            }}
        """)

        # Cambiar color del icono
        self.icon_widget.set_color(icon_color)

    def set_title(self, title: str):
        """Cambiar el título de la tarjeta"""
        self.title_text = title
        self.title_label.setText(title)

    def set_description(self, description: str):
        """Cambiar la descripción de la tarjeta"""
        self.description_text = description
        self.description_label.setText(description)

    def set_button_text(self, text: str):
        """Cambiar el texto del botón"""
        self.button_text = text
        self.action_button.setText(text)

    def set_format_label(self, text: str):
        """Cambiar la etiqueta de formato"""
        self.format_text = text
        self.format_label.setText(text)

    def set_icon(self, icon_name: str):
        """Cambiar el icono de la tarjeta"""
        self.icon_name = icon_name
        self.icon_widget.icon_name = icon_name
        # Reaplicar el color actual
        is_dark = (self.current_theme == "dark")
        icon_color = "#FFFFFF" if is_dark else "#002E6D"
        self.icon_widget.set_color(icon_color)


# Para compatibilidad con importaciones
__all__ = ['ReportCardGitHub', 'IconWidget']

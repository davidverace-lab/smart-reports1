"""
Panel de Matplotlib Interactivo - PyQt6
Integración con Matplotlib para gráficos científicos
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class PanelMatplotlibInteractivo(QWidget):
    """Panel de Matplotlib Interactivo"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("📈 Gráficos Matplotlib")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        generate_btn = QPushButton("🔄 Generar")
        generate_btn.setFixedHeight(40)
        generate_btn.clicked.connect(self._generate_plots)
        header_layout.addWidget(generate_btn)

        layout.addLayout(header_layout)

        # Info card
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(20, 20, 20, 20)

        info_title = QLabel("📊 Integración con Matplotlib")
        info_title.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))
        info_layout.addWidget(info_title)

        info_text = QLabel(
            "Este panel permite crear gráficos científicos y estadísticos "
            "utilizando Matplotlib, la biblioteca de visualización más popular de Python.\n\n"
            "Características:\n"
            "• Gráficos de líneas, barras, scatter, histogramas\n"
            "• Subplots y gráficos múltiples\n"
            "• Personalización completa de estilos\n"
            "• Exportación a PNG, PDF, SVG\n"
            "• Zoom, pan y herramientas interactivas"
        )
        info_text.setFont(QFont("Montserrat", 11))
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)

        layout.addWidget(info_frame)

        # Placeholder para canvas de Matplotlib
        canvas_frame = QFrame()
        canvas_frame.setFrameShape(QFrame.Shape.StyledPanel)
        canvas_frame.setMinimumHeight(400)
        canvas_layout = QVBoxLayout(canvas_frame)
        canvas_layout.setContentsMargins(20, 20, 20, 20)

        placeholder = QLabel("🎨 Área de Matplotlib\n\nAquí se mostrarán los gráficos generados")
        placeholder.setFont(QFont("Montserrat", 14))
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #888888;")
        canvas_layout.addWidget(placeholder)

        layout.addWidget(canvas_frame)

        layout.addStretch()

    def _generate_plots(self):
        """Generar gráficos"""
        print("🔄 Generando gráficos con Matplotlib...")

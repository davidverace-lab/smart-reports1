"""
Tarjeta de Gráfico - PyQt6
Componente reutilizable para mostrar gráficos en tarjetas
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtGui import QFont


class TarjetaGrafico(QFrame):
    """Tarjeta para mostrar gráficos"""

    def __init__(self, titulo, parent=None):
        super().__init__(parent)
        
        self.titulo = titulo
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(250)
        
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        # Título
        title_label = QLabel(self.titulo)
        title_label.setFont(QFont("Montserrat", 12, QFont.Weight.Bold))
        layout.addWidget(title_label)

        # Placeholder para gráfico
        self.chart_container = QWidget()
        layout.addWidget(self.chart_container)

"""
Tarjeta de Métrica - PyQt6
Componente para mostrar métricas y KPIs
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class TarjetaMetrica(QFrame):
    """Tarjeta para mostrar métricas"""

    def __init__(self, label, value, icon="", parent=None):
        super().__init__(parent)
        
        self.label_text = label
        self.value_text = value
        self.icon_text = icon
        
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedHeight(120)
        
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        # Icono
        if self.icon_text:
            icon_label = QLabel(self.icon_text)
            icon_label.setFont(QFont("Arial", 28))
            layout.addWidget(icon_label)

        # Valor
        value_label = QLabel(self.value_text)
        value_label.setFont(QFont("Montserrat", 24, QFont.Weight.Bold))
        layout.addWidget(value_label)

        # Label
        label_label = QLabel(self.label_text)
        label_label.setFont(QFont("Montserrat", 10))
        label_label.setStyleSheet("color: #888888;")
        layout.addWidget(label_label)

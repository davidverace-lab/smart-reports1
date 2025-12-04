"""Chart Options Menu - PyQt6"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame
from PyQt6.QtGui import QFont

class ChartOptionsMenu(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        options = ["Exportar PNG", "Exportar PDF", "Copiar Datos", "Configurar"]
        for opt in options:
            btn = QPushButton(opt)
            btn.setFixedHeight(35)
            layout.addWidget(btn)

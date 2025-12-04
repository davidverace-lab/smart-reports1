"""Interactive Chart Card - PyQt6"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtGui import QFont

class InteractiveChartCard(QFrame):
    def __init__(self, titulo, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self)
        title = QLabel(titulo)
        title.setFont(QFont("Montserrat", 13, QFont.Weight.Bold))
        layout.addWidget(title)

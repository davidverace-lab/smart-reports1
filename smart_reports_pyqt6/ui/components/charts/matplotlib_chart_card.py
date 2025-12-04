"""Matplotlib Chart Card - PyQt6"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtGui import QFont

class MatplotlibChartCard(QFrame):
    def __init__(self, titulo, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(300)
        layout = QVBoxLayout(self)
        title = QLabel(titulo)
        title.setFont(QFont("Montserrat", 12, QFont.Weight.Bold))
        layout.addWidget(title)

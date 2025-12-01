"""Gráfica Expandible - PyQt6"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton
from PyQt6.QtGui import QFont

class GraficaExpandible(QFrame):
    def __init__(self, titulo, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self)
        title = QLabel(titulo)
        title.setFont(QFont("Montserrat", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        expand_btn = QPushButton("🔍 Expandir")
        expand_btn.setFixedHeight(30)
        layout.addWidget(expand_btn)

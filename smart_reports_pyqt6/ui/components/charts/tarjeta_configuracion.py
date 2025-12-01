"""Tarjeta de Configuración - PyQt6"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtGui import QFont

class TarjetaConfiguracion(QFrame):
    def __init__(self, titulo, descripcion, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        title = QLabel(titulo)
        title.setFont(QFont("Montserrat", 13, QFont.Weight.Bold))
        layout.addWidget(title)
        desc = QLabel(descripcion)
        desc.setFont(QFont("Montserrat", 10))
        desc.setWordWrap(True)
        layout.addWidget(desc)

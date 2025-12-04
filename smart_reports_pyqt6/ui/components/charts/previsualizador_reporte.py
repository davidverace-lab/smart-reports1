"""Previsualizador de Reporte - PyQt6"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QTextEdit
from PyQt6.QtGui import QFont

class PrevisualizadorReporte(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self)
        title = QLabel("📄 Vista Previa del Reporte")
        title.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        layout.addWidget(self.preview_text)

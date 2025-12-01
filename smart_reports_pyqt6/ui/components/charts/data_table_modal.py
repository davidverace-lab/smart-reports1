"""Data Table Modal - PyQt6"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QPushButton
from PyQt6.QtGui import QFont

class DataTableModal(QDialog):
    def __init__(self, titulo, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.setMinimumSize(600, 400)
        layout = QVBoxLayout(self)
        title = QLabel(titulo)
        title.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        self.table = QTableWidget(10, 5)
        layout.addWidget(self.table)
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

"""Botón de Pestaña Personalizado - PyQt6"""
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class BotonPestana(QPushButton):
    """Botón personalizado para pestañas"""
    
    def __init__(self, texto, parent=None):
        super().__init__(texto, parent)
        
        self.setFont(QFont("Montserrat", 11))
        self.setFixedHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Estilo base
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-bottom: 2px solid transparent;
                padding: 5px 15px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgba(0, 212, 170, 0.1);
            }
            QPushButton:checked {
                border-bottom: 2px solid #00D4AA;
                font-weight: bold;
            }
        """)
        
        self.setCheckable(True)
